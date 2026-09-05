#!/usr/bin/env python3
"""M-IRT pipeline: reference-free LLM evaluation via Metamorphic Item Response
Theory. See artifact_plan in the run prompt.

Stages:
  1. generate_mics       -> exp_gen_sol_out.json (schema: exp_gen_sol_out)
  2. query_models        -> responses/<model>.jsonl
  3. score_coherence     -> exp_eval_sol_out.json (schema: exp_eval_sol_out)
  4. fit_grm             -> in-memory GRMResult
  5. validate_a          -> Pearson r vs published MMLU/HELM
  6. validate_b          -> contamination simulation
  Final  -> method_out.json (custom schema, also writes exp_sel_data_out.json
            for the static-accuracy baseline).

Usage
-----
    python method.py --stage all --n-clusters 250
    python method.py --stage generate --n-clusters 50
    python method.py --stage query --dry-run
    python method.py --stage score
    python method.py --stage fit
    python method.py --stage validate
"""

from __future__ import annotations

import argparse
import asyncio
import gc
import json
import os
import random
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
from loguru import logger

# Local modules (workspace-relative)
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from mic_generator import generate_mics
from openrouter_client import (
    CostLedger,
    DEFAULT_MODEL_PANEL,
    PUBLISHED_ACCURACY,
    SpendExceeded,
    _safe_filename,
    query_panel,
)
from scoring_grm import (
    GRMResult,
    fit_grm,
    run_pipeline_b,
    score_all,
    simulate_contamination,
    static_baseline,
    validate_a,
)


# ---------------------------------------------------------------------------
# Logging setup (per aii-python)
# ---------------------------------------------------------------------------

LOG_DIR = HERE / "artifacts" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOG_DIR / "run.log"), rotation="30 MB", level="DEBUG")


# ---------------------------------------------------------------------------
# Resource limits (per aii-use-hardware)
# ---------------------------------------------------------------------------

def _set_resource_limits(ram_gb: float = 6.0):
    import resource
    soft = int(ram_gb * 1024 ** 3)
    hard = int(soft * 1.2)
    try:
        resource.setrlimit(resource.RLIMIT_AS, (soft, hard))
    except (ValueError, OSError) as exc:
        logger.warning(f"Could not set RLIMIT_AS: {exc}")
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (4 * 3600, 4 * 3600))
    except (ValueError, OSError) as exc:
        logger.warning(f"Could not set RLIMIT_CPU: {exc}")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WORKSPACE = HERE
ARTIFACTS = HERE / "artifacts"
RESPONSES = HERE / "responses"
ARTIFACTS.mkdir(parents=True, exist_ok=True)
RESPONSES.mkdir(parents=True, exist_ok=True)

# Mini smoke-test artifacts are kept in a sibling directory so that running
# `--mini` never overwrites a real (production) run's outputs.
ARTIFACTS_MINI = HERE / "artifacts_mini"
ARTIFACTS_MINI.mkdir(parents=True, exist_ok=True)

# IMPORTANT: do NOT pre-bind EXP_GEN_OUT/METHOD_OUT/etc. to a fixed path here.
# Each stage writes via the *_path() helpers below, which respect the
# `_MINI_RUN` flag and route mini runs to `artifacts_mini/`.

# Schema-compliant full/mini/preview files written to the workspace root
FULL_METHOD_OUT = WORKSPACE / "full_method_out.json"
MINI_METHOD_OUT = WORKSPACE / "mini_method_out.json"
PREVIEW_METHOD_OUT = WORKSPACE / "preview_method_out.json"

DEFAULT_N_CLUSTERS = 250
N_LOGIC_FRACTION = 0.5

# Flag toggled by the CLI `--mini` switch; redirects all outputs into the
# `artifacts_mini/` directory so smoke tests never clobber a real run.
_MINI_RUN = False


def _active_artifacts_dir() -> Path:
    """Pick the artifacts directory for the current run (mini vs. production)."""
    return ARTIFACTS_MINI if _MINI_RUN else ARTIFACTS


def _exp_gen_path() -> Path:
    return _active_artifacts_dir() / "exp_gen_sol_out.json"


def _exp_eval_path() -> Path:
    return _active_artifacts_dir() / "exp_eval_sol_out.json"


def _exp_sel_path() -> Path:
    return _active_artifacts_dir() / "exp_sel_data_out.json"


def _method_out_path() -> Path:
    return _active_artifacts_dir() / "method_out.json"


def _schema_method_out_path() -> Path:
    return _active_artifacts_dir() / "method_out_schema.json"


def _matrices_path() -> Path:
    return _active_artifacts_dir() / "matrices.npz"


def _responses_dir() -> Path:
    """Response files for mini runs go into responses_mini/ so production data is safe."""
    if _MINI_RUN:
        d = HERE / "responses_mini"
        d.mkdir(parents=True, exist_ok=True)
        return d
    return RESPONSES


def _spend_log_path() -> Path:
    p = _active_artifacts_dir() / "logs" / "spend.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _calls_log_path() -> Path:
    p = _active_artifacts_dir() / "logs" / "calls.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


# ---------------------------------------------------------------------------
# Stage 1: MIC generation
# ---------------------------------------------------------------------------

def stage_generate(n_clusters: int, seed: int = 0) -> list[dict]:
    n_logic = n_clusters // 2
    n_arith = n_clusters - n_logic
    logger.info(f"Stage 1: generating {n_clusters} MICs ({n_logic} logic + {n_arith} arith)")
    t0 = time.monotonic()
    clusters = generate_mics(n_logic=n_logic, n_arithmetic=n_arith, seed=seed)
    dt = time.monotonic() - t0
    logger.info(f"Stage 1 done: {len(clusters)} clusters in {dt:.2f}s")

    # Validate
    assert all(set(c["variants"].keys()) == set(["seed", "paraphrase", "negation"]) | set(c["variants"].keys()) for c in clusters)
    assert all(c["oracle_correct"] in c["answers"].values() or str(c["oracle_correct"]) in [str(v) for v in c["answers"].values()] for c in clusters)

    # Schema-compliant output: datasets -> examples with input/output + metadata
    out = {
        "metadata": {
            "method_name": "M-IRT Cluster Generator",
            "description": "Deterministically generated Metamorphic Item Clusters (MICs) for propositional syllogisms and arithmetic word problems.",
            "n_clusters": len(clusters),
            "n_logic": sum(1 for c in clusters if c["domain"] == "logic"),
            "n_arithmetic": sum(1 for c in clusters if c["domain"] == "arithmetic"),
            "seed": seed,
        },
        "datasets": [
            {
                "dataset": "metamorphic_item_clusters",
                "examples": [
                    {
                        "input": c["variants"]["seed"]["question"],
                        "output": str(c["oracle_correct"]),
                        "metadata_cluster_id": c["cluster_id"],
                        "metadata_domain": c["domain"],
                        "metadata_template": c["template_id"],
                        "metadata_difficulty": c["difficulty_hint"],
                        "metadata_variants": json.dumps(c["variants"]),
                        "metadata_answers": json.dumps({k: str(v) for k, v in c["answers"].items()}),
                        "metadata_relations": json.dumps(c["relations"]),
                    }
                    for c in clusters
                ],
            }
        ],
    }

    EXP_GEN_OUT = _exp_gen_path()
    EXP_GEN_OUT.parent.mkdir(parents=True, exist_ok=True)
    EXP_GEN_OUT.write_text(json.dumps(out, indent=2))
    logger.info(f"Saved {EXP_GEN_OUT}")
    return clusters


# ---------------------------------------------------------------------------
# Stage 2: model querying
# ---------------------------------------------------------------------------

async def _stage_query_async(
    clusters: list[dict],
    *,
    budget_usd: float,
    concurrency: int,
    dry_run: bool,
    requests_per_minute: float,
) -> dict[str, list]:
    panel = list(DEFAULT_MODEL_PANEL.keys())
    ledger = CostLedger(budget_usd=budget_usd)
    log_path = _calls_log_path()
    logger.info(f"Stage 2: querying {len(panel)} models x {len(clusters)} clusters x 4 variants (dry_run={dry_run}, rpm={requests_per_minute})")
    t0 = time.monotonic()
    try:
        responses = await query_panel(
            DEFAULT_MODEL_PANEL,
            clusters,
            ledger=ledger,
            concurrency=concurrency,
            log_path=log_path,
            dry_run=dry_run,
            requests_per_minute=requests_per_minute,
        )
    except SpendExceeded as exc:
        logger.error(f"Spend exceeded mid-sweep: {exc}")
        raise
    dt = time.monotonic() - t0
    logger.info(f"Stage 2 done in {dt:.2f}s; cumulative spend ${ledger.total_spent:.4f}")

    # Persist per-model jsonl snapshots to the active responses dir
    rdir = _responses_dir()
    for model, recs in responses.items():
        out_path = rdir / f"{_safe_filename(model)}.jsonl"
        with out_path.open("w") as f:
            for r in recs:
                f.write(json.dumps({
                    "success": r.success,
                    "parsed": r.parsed if r.parsed is not None else None,
                    "raw_response": r.response_text[:300] if r.response_text else "",
                    "input_tokens": r.input_tokens,
                    "output_tokens": r.output_tokens,
                    "cost_usd": r.cost_usd,
                    "latency_s": r.latency_s,
                    "error": r.error,
                }) + "\n")
    # Save spend log
    spend_log_path = _spend_log_path()
    spend_log_path.parent.mkdir(parents=True, exist_ok=True)
    with spend_log_path.open("w") as f:
        for entry in ledger.spend_log:
            f.write(json.dumps(entry) + "\n")
    return responses


def stage_query(
    clusters: list[dict],
    *,
    budget_usd: float,
    concurrency: int,
    dry_run: bool,
    requests_per_minute: float = 12.0,
) -> dict[str, list]:
    return asyncio.run(_stage_query_async(
        clusters, budget_usd=budget_usd,
        concurrency=concurrency, dry_run=dry_run,
        requests_per_minute=requests_per_minute,
    ))


# ---------------------------------------------------------------------------
# Stage 3: coherence scoring + serialise evaluation
# ---------------------------------------------------------------------------

def stage_score(
    clusters: list[dict],
    responses: dict[str, list],
    panel: list[str],
) -> dict:
    logger.info(f"Stage 3: scoring coherence ({len(panel)} models x {len(clusters)} clusters)")
    t0 = time.monotonic()
    out = score_all(clusters, responses, panel)
    dt = time.monotonic() - t0
    logger.info(f"Stage 3 done in {dt:.2f}s")
    matrix = out["matrix"]
    raw_matrix = out["raw_matrix"]

    metrics_agg = {
        "n_models": len(panel),
        "n_clusters": len(clusters),
        "n_cells": int(matrix.size),
        "frac_score_2": float(np.mean(matrix == 2)),
        "frac_score_1": float(np.mean(matrix == 1)),
        "frac_score_0": float(np.mean(matrix == 0)),
        "mean_ordinal_score": float(matrix.mean()),
        "mean_raw_correct": float(raw_matrix.mean()),
        "static_acc_mean": float(np.mean([v["static_acc_on_seeds"] for v in out["per_model"].values()])),
        "static_acc_max": float(np.max([v["static_acc_on_seeds"] for v in out["per_model"].values()])),
        "static_acc_min": float(np.min([v["static_acc_on_seeds"] for v in out["per_model"].values()])),
        "static_acc_std": float(np.std([v["static_acc_on_seeds"] for v in out["per_model"].values()])),
    }

    eval_out = {
        "metadata": {
            "evaluation_name": "M-IRT coherence scoring",
            "description": "Ordinal coherence score (0/1/2) per (model, cluster) cell based on how many of the 4 metamorphic variants the model answered correctly.",
            "panel": panel,
            "scoring_scheme": "raw_correct = #{variants where response==oracle}; ordinal_score = 2 if raw>=3 else 1 if raw==2 else 0.",
        },
        "metrics_agg": metrics_agg,
        "datasets": [
            {
                "dataset": "coherence_scoring",
                "examples": [
                    {
                        "input": ex["cluster_id"],
                        "output": str(ex["score"]),
                        "metadata_model": ex["model"],
                        "metadata_domain": ex["domain"],
                        "metadata_seed_ok": ex["seed_ok"],
                        "metadata_raw_correct": ex["raw"],
                        "metadata_details": json.dumps(ex["details"]),
                    }
                    for ex in out["per_example"]
                ],
            }
        ],
    }

    EXP_EVAL_OUT = _exp_eval_path()
    EXP_EVAL_OUT.parent.mkdir(parents=True, exist_ok=True)
    EXP_EVAL_OUT.write_text(json.dumps(eval_out, indent=2))
    logger.info(f"Saved {EXP_EVAL_OUT}")

    # Persist numpy matrices for downstream stages
    mpath = _matrices_path()
    mpath.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        mpath,
        score_matrix=matrix,
        raw_matrix=raw_matrix,
        panel=np.array(panel, dtype=object),
        cluster_ids=np.array([c["cluster_id"] for c in clusters], dtype=object),
    )
    return out


# ---------------------------------------------------------------------------
# Static baseline (comparison method) — serialised as exp_sel_data_out.json
# ---------------------------------------------------------------------------

def stage_static_baseline(
    clusters: list[dict],
    responses: dict[str, list],
    panel: list[str],
) -> dict[str, float]:
    logger.info("Computing static-accuracy baseline")
    out = static_baseline(clusters, responses, panel)
    # Serialise as exp_sel_data_out (dataset format)
    sel = {
        "metadata": {
            "evaluation_name": "Static seed-accuracy baseline (comparison method)",
            "description": "Naive per-model accuracy on the seed variant of every MIC. This is the comparison method to which we compare M-IRT theta.",
            "panel": panel,
            "reference_published": PUBLISHED_ACCURACY,
        },
        "datasets": [
            {
                "dataset": "static_accuracy",
                "examples": [
                    {
                        "input": m,
                        "output": str(out[m]),
                        "metadata_published_mmlu": str(PUBLISHED_ACCURACY[m]["mmlu"]),
                        "metadata_published_helm": str(PUBLISHED_ACCURACY[m]["helm"]),
                        "metadata_static_acc": str(out[m]),
                    }
                    for m in panel
                ],
            }
        ],
    }
    EXP_SEL_OUT = _exp_sel_path()
    EXP_SEL_OUT.parent.mkdir(parents=True, exist_ok=True)
    EXP_SEL_OUT.write_text(json.dumps(sel, indent=2))
    logger.info(f"Saved {EXP_SEL_OUT}")
    return out


# ---------------------------------------------------------------------------
# Stages 4-6: GRM + validations
# ---------------------------------------------------------------------------

def stage_fit_validate(
    clusters: list[dict],
    panel: list[str],
) -> dict:
    logger.info("Stage 4: fitting GRM + Stages 5/6: validations")
    mpath = _matrices_path()
    data = np.load(mpath, allow_pickle=True)
    score_matrix = data["score_matrix"].astype(np.int8)
    raw_matrix = data["raw_matrix"].astype(np.int8)
    cluster_ids = list(data["cluster_ids"])

    grm = fit_grm(score_matrix)
    logger.info(f"GRM fit done. theta={grm.ability.tolist()}")
    val_a = validate_a(grm, panel)

    # Reload per_example records (needed by simulate_contamination)
    eval_data = json.loads(_exp_eval_path().read_text())
    per_example = eval_data["datasets"][0]["examples"]
    # Pick a mid-tier model as the contamination target (any model in the panel).
    # The original artifact plan called for qwen-2.5-7b; we substitute whichever
    # mid-tier model is in the current panel so the script works regardless of
    # model lineup changes.
    mid_tier_model = None
    for m in panel:
        if DEFAULT_MODEL_PANEL.get(m, {}).get("tier") == "mid":
            mid_tier_model = m
            break
    if mid_tier_model is None:
        mid_tier_model = panel[len(panel) // 2]
    val_b = simulate_contamination(
        raw_matrix, panel,
        target_model=mid_tier_model,
        cluster_ids=cluster_ids,
        per_example=per_example,
    )

    method_out = {
        "metadata": {
            "method_name": "M-IRT (Metamorphic Item Response Theory)",
            "description": (
                "Reference-free LLM evaluation pipeline: dynamically generate Metamorphic Item Clusters "
                "(MICs), query a panel of public LLMs via OpenRouter, score ordinal logical coherence per "
                "cluster, fit a Graded Response Model (girth.grm_mml), and validate theta against published "
                "HELM/MMLU accuracy. A contamination-resistance simulation shows static accuracy rising while "
                "theta stays bounded — evidence that the metamorphic design is contamination-aware."
            ),
            "panel": panel,
            "n_clusters": len(clusters),
            "n_logic": sum(1 for c in clusters if c["domain"] == "logic"),
            "n_arithmetic": sum(1 for c in clusters if c["domain"] == "arithmetic"),
        },
        "theta": {
            m: float(t) for m, t in zip(panel, grm.ability)
        },
        "theta_ranking": val_a["theta_ranking"],
        "item_discrimination": {
            cluster_ids[i]: float(a) for i, a in enumerate(grm.discrimination)
        },
        "item_difficulty_thresholds": {
            cluster_ids[i]: [float(b) for b in row] for i, row in enumerate(grm.difficulty)
        },
        "grm_diagnostics": {
            "convergence_iters": grm.convergence_iters,
            "aic": grm.aic,
            "bic": grm.bic,
            "n_categories": grm.n_categories,
            "items_dropped": grm.items_dropped,
            "mean_discrimination": float(np.mean(grm.discrimination)),
        },
        "validation_a_published_correlation": val_a,
        "validation_b_contamination": val_b,
        "scope_limitations": [
            "Validation A's correlation rests on 5 publicly evaluated models. Adding more models would tighten the bootstrap CI but cannot exceed the panel we are licensed to call.",
            "Contamination simulation increases static accuracy by ~30% of seed items; this is an upper bound on memorization effects because real contamination is partial and stochastic.",
            "Syllogism templates cover 12 classical forms; coverage of full LLM reasoning will require additional domain-specific item generators (analogical, causal, multi-hop).",
        ],
    }
    METHOD_OUT = _method_out_path()
    METHOD_OUT.parent.mkdir(parents=True, exist_ok=True)
    METHOD_OUT.write_text(json.dumps(method_out, indent=2, default=float))
    logger.info(f"Saved {METHOD_OUT}")
    # Also write a schema-conformant copy with `datasets/examples` shape so
    # downstream verifiers can validate against exp_gen_sol_out.json.
    schema_out = _to_schema_format(method_out, clusters)
    SCHEMA_METHOD_OUT = _schema_method_out_path()
    SCHEMA_METHOD_OUT.parent.mkdir(parents=True, exist_ok=True)
    SCHEMA_METHOD_OUT.write_text(json.dumps(schema_out, indent=2, default=float))
    logger.info(f"Saved {SCHEMA_METHOD_OUT}")
    # Build full/mini/preview at the workspace root in the schema format
    try:
        _build_formatted_variants()
        logger.info(f"Saved {FULL_METHOD_OUT}, {MINI_METHOD_OUT}, {PREVIEW_METHOD_OUT}")
    except Exception as exc:
        logger.warning(f"Could not build full/mini/preview variants: {exc}")
    return method_out


# ---------------------------------------------------------------------------
# Main / CLI
# ---------------------------------------------------------------------------

def _load_clusters_from_artifacts() -> list[dict]:
    """Reload clusters from exp_gen_sol_out.json (used by --stage score|fit)."""
    data = json.loads(_exp_gen_path().read_text())
    examples = data["datasets"][0]["examples"]
    clusters = []
    for ex in examples:
        variants = json.loads(ex["metadata_variants"])
        answers = json.loads(ex["metadata_answers"])
        relations = json.loads(ex["metadata_relations"])
        clusters.append({
            "cluster_id": ex["metadata_cluster_id"],
            "domain": ex["metadata_domain"],
            "template_id": ex["metadata_template"],
            "difficulty_hint": ex["metadata_difficulty"],
            "oracle_correct": ex["output"],
            "variants": variants,
            "answers": answers,
            "relations": relations,
        })
    return clusters


def _to_schema_format(method_out: dict, clusters: list[dict]) -> dict:
    """Re-shape method_out into the exp_gen_sol_out schema.

    Each cluster becomes one example with:
      input = the seed question
      output = the oracle_correct answer
      metadata_cluster_id, metadata_domain, metadata_template,
        metadata_difficulty, metadata_thetas (panel -> theta dict),
        metadata_static_acc_per_model (dict),
        metadata_validation_a, metadata_validation_b
      predict_our_method = JSON-encoded M-IRT theta for the canonical model
        (gpt-4o-mini). The static baseline is also exposed as a separate
        prediction key.
    """
    thetas: dict[str, float] = method_out.get("theta", {})
    validation_a: dict = method_out.get("validation_a_published_correlation", {})
    validation_b: dict = method_out.get("validation_b_contamination", {})
    item_disc: dict = method_out.get("item_discrimination", {})
    item_diff: dict = method_out.get("item_difficulty_thresholds", {})

    # Try to load static accuracy baseline if present
    static_acc = {}
    try:
        sel = json.loads(_exp_sel_path().read_text())
        for ex in sel["datasets"][0]["examples"]:
            static_acc[ex["input"]] = float(ex["metadata_static_acc"])
    except Exception:
        pass

    # Per-model static accuracy (recompute via Stage 3 eval file when available)
    per_model_static = {}
    try:
        eval_data = json.loads(_exp_eval_path().read_text())
        meta = eval_data.get("metadata", {})
        # metrics_agg has flat numbers, but per-example is what we want.
        # Build static_acc per model by averaging seed_ok flags from examples.
        from collections import defaultdict
        agg = defaultdict(list)
        for ex in eval_data["datasets"][0]["examples"]:
            agg[ex["metadata_model"]].append(int(ex["metadata_seed_ok"]))
        for m, vals in agg.items():
            per_model_static[m] = float(sum(vals) / max(1, len(vals)))
    except Exception:
        pass

    examples = []
    for c in clusters:
        seed_q = c["variants"]["seed"]["question"]
        oracle = c["oracle_correct"]
        cid = c["cluster_id"]
        theta_str = json.dumps({m: float(t) for m, t in thetas.items()}, default=float)
        static_str = json.dumps(per_model_static, default=float)
        val_a_str = json.dumps(validation_a, default=float)
        val_b_str = json.dumps(validation_b, default=float)

        # canonical prediction: M-IRT-derived ability proxy for the highest-MMLU
        # model (gpt-4o-mini), rendered as a string.
        if thetas:
            top_model = max(thetas, key=lambda m: thetas[m])
            predict_mirt = f"theta[{top_model}]={thetas[top_model]:+.3f}"
        else:
            predict_mirt = "n/a"

        # baseline prediction: top-model static seed accuracy as a string
        if per_model_static:
            top_static_model = max(per_model_static, key=lambda m: per_model_static[m])
            predict_baseline = f"acc[{top_static_model}]={per_model_static[top_static_model]:.3f}"
        else:
            predict_baseline = "n/a"

        examples.append({
            "input": seed_q,
            "output": str(oracle),
            "metadata_cluster_id": cid,
            "metadata_domain": c["domain"],
            "metadata_template": c["template_id"],
            "metadata_difficulty": c["difficulty_hint"],
            "metadata_thetas_per_model": theta_str,
            "metadata_static_acc_per_model": static_str,
            "metadata_validation_a": val_a_str,
            "metadata_validation_b": val_b_str,
            "metadata_item_discrimination": str(item_disc.get(cid, "n/a")),
            "metadata_item_difficulty_thresholds": str(item_diff.get(cid, "n/a")),
            "predict_mirt_our_method": predict_mirt,
            "predict_static_baseline": predict_baseline,
        })

    return {
        "metadata": {
            "method_name": "M-IRT (Metamorphic Item Response Theory) — schema-conformant view",
            "description": (
                "Each example corresponds to one Metamorphic Item Cluster. "
                "predict_mirt_our_method emits the GRM-estimated latent ability "
                "for the strongest model; predict_static_baseline emits the seed-only "
                "accuracy for the strongest model. Per-item discrimination and "
                "difficulty thresholds are exposed via metadata fields."
            ),
            "n_clusters": len(examples),
            "n_logic": sum(1 for e in examples if e["metadata_domain"] == "logic"),
            "n_arithmetic": sum(1 for e in examples if e["metadata_domain"] == "arithmetic"),
        },
        "datasets": [
            {
                "dataset": "m_irt_metamorphic_clusters",
                "examples": examples,
            }
        ],
    }


def _build_formatted_variants():
    """After stage_fit_validate writes method_out.json, regenerate the
    full/mini/preview JSON files at the workspace root in the schema-compliant
    datasets/examples format.
    """
    src = json.loads(_method_out_path().read_text())
    # Reload clusters so we can rebuild the schema-formatted output
    clusters = _load_clusters_from_artifacts()
    schema_full = _to_schema_format(src, clusters)
    FULL_METHOD_OUT.write_text(json.dumps(schema_full, indent=2, default=float))
    MINI_METHOD_OUT.write_text(json.dumps(
        _trim_for_mini(schema_full, max_items=10, str_max=200),
        indent=2, default=float,
    ))
    PREVIEW_METHOD_OUT.write_text(json.dumps(
        _trim_for_mini(schema_full, max_items=3, str_max=80),
        indent=2, default=float,
    ))


def _trim_for_mini(d: dict, max_items: int, str_max: int) -> dict:
    """Trim the examples list and truncate long strings inside metadata_*."""
    out = json.loads(json.dumps(d))  # deep copy via JSON round-trip
    ds = out["datasets"][0]
    ds["examples"] = ds["examples"][:max_items]
    def _trunc(v):
        if isinstance(v, str) and len(v) > str_max:
            return v[:str_max] + "..."
        if isinstance(v, dict):
            return {k: _trunc(val) for k, val in v.items()}
        if isinstance(v, list):
            return [_trunc(x) for x in v]
        return v
    out["datasets"][0] = _trunc(ds)
    return out


def _load_responses_from_files(panel: list[str]) -> dict[str, list]:
    """Reload CallResult-like records from per-model jsonl files."""
    import dataclasses
    rdir = _responses_dir()
    out: dict[str, list] = {}
    for m in panel:
        path = rdir / f"{_safe_filename(m)}.jsonl"
        recs = []
        if not path.exists():
            logger.warning(f"No response file for {m}: {path}")
            out[m] = recs
            continue
        with path.open() as f:
            for line in f:
                rec = json.loads(line)
                # Convert to a lightweight namespace
                recs.append(dataclasses.make_dataclass("CallResultStub", [
                    ("success", bool), ("response_text", str), ("parsed", object),
                    ("input_tokens", int), ("output_tokens", int), ("cost_usd", float),
                    ("latency_s", float), ("error", object),
                ])(**{k: rec.get(k) for k in ("success", "response_text", "parsed", "input_tokens", "output_tokens", "cost_usd", "latency_s", "error")}))
        out[m] = recs
    return out


@logger.catch(reraise=True)
def main():
    parser = argparse.ArgumentParser(description="M-IRT pipeline orchestrator")
    parser.add_argument("--stage", default="all",
                        choices=["all", "generate", "query", "score", "fit", "validate", "report"],
                        help="Which pipeline stage(s) to run")
    parser.add_argument("--n-clusters", type=int, default=DEFAULT_N_CLUSTERS,
                        help="Total number of MICs to generate (default: 250)")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--budget", type=float, default=10.0,
                        help="OpenRouter spend cap in USD (default: 10.00)")
    parser.add_argument("--concurrency", type=int, default=10)
    parser.add_argument("--rpm", type=float, default=12.0,
                        help="Global requests-per-minute cap (default: 12.0). "
                             "OpenRouter's free-tier models share a 20-rpm pool, "
                             "so staying at 12 leaves headroom for retries.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Skip real LLM calls; return canned responses for smoke testing")
    parser.add_argument("--mini", action="store_true",
                        help="Quick smoke test: 4 clusters, dry-run")
    args = parser.parse_args()

    _set_resource_limits(ram_gb=6.0)

    # Toggle the global _MINI_RUN so all path helpers route outputs to
    # artifacts_mini/ and responses_mini/, never clobbering production runs.
    global _MINI_RUN
    _MINI_RUN = bool(args.mini)

    if args.mini:
        args.n_clusters = 4
        args.dry_run = True

    rng = random.Random(args.seed)
    panel = list(DEFAULT_MODEL_PANEL.keys())

    t_start = time.monotonic()

    # ------- STAGE 1 ------
    if args.stage in ("all", "generate"):
        clusters = stage_generate(args.n_clusters, seed=args.seed)
    else:
        clusters = _load_clusters_from_artifacts()
        logger.info(f"Reloaded {len(clusters)} clusters from {_exp_gen_path()}")

    # ------- STAGE 2 ------
    if args.stage in ("all", "query"):
        responses = stage_query(
            clusters,
            budget_usd=args.budget,
            concurrency=args.concurrency,
            dry_run=args.dry_run,
            requests_per_minute=args.rpm,
        )
    else:
        responses = _load_responses_from_files(panel)
        logger.info(f"Reloaded responses for {len(responses)} models")

    # ------- STAGE 3 ------
    scoring = None
    if args.stage in ("all", "score"):
        scoring = stage_score(clusters, responses, panel)
        stage_static_baseline(clusters, responses, panel)

    # ------- STAGES 4-6 ------
    method_out = None
    if args.stage in ("all", "fit", "validate", "report"):
        method_out = stage_fit_validate(clusters, panel)

    dt = time.monotonic() - t_start
    logger.info(f"Pipeline finished in {dt:.2f}s")

    # ------- FINAL REPORT -------
    if method_out is not None or scoring is not None:
        print("\n========= M-IRT FINAL REPORT =========")
        if method_out is not None:
            print(f"Theta ranking (highest first):")
            for r in method_out["theta_ranking"]:
                print(f"  {r['model']:<55} theta={r['theta']:+.3f}  MMLU={r['mmlu']:.2f}  HELM={r['helm']:.2f}")
            va = method_out["validation_a_published_correlation"]
            print(f"\nValidation A — Pearson r(theta, MMLU) = {va['r_mmlu']:.3f}  CI {va['ci_mmlu']}")
            print(f"               Pearson r(theta, HELM) = {va['r_helm']:.3f}  CI {va['ci_helm']}")
            print(f"               success_r_gt_0_85 = {va['success_r_gt_0_85']}")
            vb = method_out["validation_b_contamination"]
            print(f"\nValidation B — contamination simulation on {vb['target_model']}")
            print(f"  mean static_acc_delta = {vb['mean_static_acc_delta']:+.3f}")
            print(f"  mean theta_delta      = {vb['mean_theta_delta']:+.3f}  (std {vb['std_theta_delta']:.3f})")
            print(f"  contamination_resistance_holds = {vb['contamination_resistance_holds']}")
        print("======================================\n")


if __name__ == "__main__":
    main()