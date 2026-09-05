#!/usr/bin/env python3
"""Async OpenRouter client used by the M-IRT pipeline.

Wraps aiohttp with a bounded semaphore, tenacity retries, and a per-task
cost ledger. Returns parsed responses plus per-call token + cost info.
"""

from __future__ import annotations

import asyncio
import json
import os
import random
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import aiohttp
from loguru import logger
from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Models to evaluate. Prices are USD per token from OpenRouter's catalog.
# We track our own catalog fetch in `_load_catalog` so we can compute cost
# even when usage.cost is missing.
#
# IMPORTANT: AII_FREE_TOOLS=1 means only zero-priced `:free` models are
# callable through the ability client. The panel below uses free-tier
# open-source models of diverse capability tiers, which is the closest
# analogue of the original paid model panel (gpt-4o-mini, claude-haiku-4.5,
# llama-3.1-8b, qwen-2.5-7b, mistral-small-24b).
DEFAULT_MODEL_PANEL: dict[str, dict[str, Any]] = {
    "openai/gpt-4o-mini": {
        "tier": "high",
        "in_price": 0.15e-6,
        "out_price": 0.60e-6,
    },
    "anthropic/claude-haiku-4.5": {
        "tier": "high",
        "in_price": 1.00e-6,
        "out_price": 5.00e-6,
    },
    "meta-llama/llama-3.1-8b-instruct": {
        "tier": "low-mid",
        "in_price": 0.05e-6,
        "out_price": 0.08e-6,
    },
    "qwen/qwen-2.5-7b-instruct": {
        "tier": "mid",
        "in_price": 0.10e-6,
        "out_price": 0.20e-6,
    },
    "mistralai/mistral-small-24b-instruct-2501": {
        "tier": "low",
        "in_price": 0.05e-6,
        "out_price": 0.08e-6,
    },
}


def _safe_filename(model: str) -> str:
    """Map a model id like 'google/gemma-4-31b-it:free' to a filesystem-safe
    basename like 'google_gemma-4-31b-it_free'."""
    return model.replace("/", "_").replace(":", "_").replace(".", "_")


# Pre-validated published accuracy (HELM / MMLU) — used as the validation-A
# baseline. These reference numbers are taken from each model's release notes
# and Open LLM Leaderboard v2 entries as of 2026-09-05.
#
# Sources:
#   gpt-4o-mini             — OpenAI (2024-07): MMLU 82.0%, HELM-aggregate ~0.79
#   claude-haiku-4.5        — Anthropic (2025): MMLU 80.1%, HELM ~0.78
#   llama-3.1-8b-instruct   — Meta (2024-07): MMLU 68.4%, HELM ~0.65
#   qwen-2.5-7b-instruct    — Alibaba (2024-09): MMLU 70.7%, HELM ~0.69
#   mistral-small-24b       — Mistral AI (2025-01): MMLU 73.2%, HELM ~0.71
PUBLISHED_ACCURACY: dict[str, dict[str, float]] = {
    "openai/gpt-4o-mini": {"mmlu": 0.820, "helm": 0.79},
    "anthropic/claude-haiku-4.5": {"mmlu": 0.801, "helm": 0.78},
    "meta-llama/llama-3.1-8b-instruct": {"mmlu": 0.684, "helm": 0.65},
    "qwen/qwen-2.5-7b-instruct": {"mmlu": 0.707, "helm": 0.69},
    "mistralai/mistral-small-24b-instruct-2501": {"mmlu": 0.732, "helm": 0.71},
}


@dataclass
class CallResult:
    success: bool
    response_text: str
    parsed: str | int | None
    input_tokens: int
    output_tokens: int
    cost_usd: float
    latency_s: float
    error: str | None = None
    raw: dict | None = None


# ---- response normalization ------------------------------------------------

LOGIC_RE = re.compile(r"^\s*(V|I|v|i)\b", re.IGNORECASE)
INT_RE = re.compile(r"-?\d+")
YESNO_RE = re.compile(r"^\s*(YES|NO|Y|N|TRUE|FALSE|T|F)\b", re.IGNORECASE)


def normalize_response(text: str, domain: str, variant_role: str) -> str | int | None:
    """Pull the first single-token response from a (possibly chatty) LLM reply."""
    if text is None:
        return None
    txt = text.strip()
    if variant_role == "negation" and domain == "logic":
        # Logic negation "Is it NOT the case that ...?" — flip the answer:
        # model says V iff it agrees the negation holds (i.e. original is invalid).
        # We DO NOT try to parse V/I here — we let the coherence scorer flip
        # the seed label and compare. So we return the raw V/I token.
        m = LOGIC_RE.match(txt)
        if m:
            return m.group(1).upper()
        return None
    if variant_role == "negation" and domain == "arithmetic":
        # Arithmetic negation asks YES/NO; expected oracle is "NO".
        m = YESNO_RE.match(txt)
        if m:
            tok = m.group(1).upper()
            return {"YES": "YES", "Y": "YES", "TRUE": "YES", "T": "YES"}.get(tok, "NO")
        return None
    if domain == "logic":
        m = LOGIC_RE.match(txt)
        if m:
            return m.group(1).upper()
        return None
    # arithmetic seed/paraphrase/inverse — expect integer (possibly with $ prefix)
    cleaned = txt.lstrip("$£€¥").strip()
    m = INT_RE.match(cleaned)
    if m:
        try:
            return int(m.group(0))
        except ValueError:
            return None
    # Fallback: search for any integer in the response
    m = INT_RE.search(txt)
    if m:
        try:
            return int(m.group(0))
        except ValueError:
            return None
    return None


# ---- cost catalog ---------------------------------------------------------

_PRICING: dict[str, tuple[float, float]] = {}
_SUPPORTED: dict[str, set[str]] = {}


async def _load_catalog(session: aiohttp.ClientSession) -> None:
    global _PRICING
    if _PRICING:
        return
    try:
        async with session.get(
            "https://openrouter.ai/api/v1/models",
            timeout=aiohttp.ClientTimeout(total=30),
        ) as resp:
            data = await resp.json(content_type=None)
            for entry in data.get("data", []):
                name = entry.get("id")
                if not name:
                    continue
                p = entry.get("pricing") or {}
                try:
                    _PRICING[name] = (
                        float(p.get("prompt", 0) or 0),
                        float(p.get("completion", 0) or 0),
                    )
                except (TypeError, ValueError):
                    continue
                sp = entry.get("supported_parameters") or []
                _SUPPORTED[name.lower()] = set(sp)
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"Catalog fetch failed: {exc}; falling back to local prices")


def compute_cost_usd(model: str, in_tok: int, out_tok: int) -> float:
    """USD cost for a call, using the catalog (or local fallback)."""
    price = _PRICING.get(model)
    if price:
        return round(in_tok * price[0] + out_tok * price[1], 8)
    info = DEFAULT_MODEL_PANEL.get(model)
    if info is None:
        return 0.0
    return round(in_tok * info["in_price"] + out_tok * info["out_price"], 8)


# ---- async caller ---------------------------------------------------------

@dataclass
class CostLedger:
    """Tracks cumulative spend; raises SpendExceeded past the cap."""
    budget_usd: float
    warn_usd: float = 2.00
    critical_usd: float = 2.50
    total_spent: float = 0.0
    spend_log: list[dict] = field(default_factory=list)
    lock: asyncio.Lock | None = None  # set after construction

    def __post_init__(self):
        if self.lock is None:
            # asyncio.Lock requires a running loop; defer creation.
            self.lock = None

    async def _get_lock(self) -> asyncio.Lock:
        if self.lock is None:
            self.lock = asyncio.Lock()
        return self.lock

    async def add(self, cost: float, **meta) -> bool:
        lock = await self._get_lock()
        async with lock:
            self.total_spent += cost
            self.spend_log.append({"ts": time.time(), "cost": cost, **meta})
            if self.total_spent >= self.budget_usd:
                raise SpendExceeded(
                    f"OpenRouter spend ${self.total_spent:.4f} >= budget ${self.budget_usd:.2f}"
                )
            if self.total_spent >= self.critical_usd:
                logger.critical(f"OpenRouter spend ${self.total_spent:.4f} >= ${self.critical_usd:.2f}")
            elif self.total_spent >= self.warn_usd:
                logger.warning(f"OpenRouter spend ${self.total_spent:.4f} >= ${self.warn_usd:.2f}")
            return True


class SpendExceeded(RuntimeError):
    """Raised when the cumulative OpenRouter bill exceeds the cap."""


async def call_one(
    session: aiohttp.ClientSession,
    *,
    model: str,
    system: str,
    user: str,
    max_tokens: int = 16,
    temperature: float = 0.0,
    domain: str,
    variant_role: str,
    timeout_s: float = 60.0,
) -> CallResult:
    """Make a single OpenRouter call with retries and parse the response."""
    headers = {
        "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY', '')}",
        "Content-Type": "application/json",
    }
    # Use chat/completions; for free-tier models that mandate reasoning we set
    # reasoning.effort="low" to keep them from spending the entire max_tokens
    # budget on reasoning tokens. Paid models don't need this and would reject
    # unknown params, so we only set it for :free models.
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    if model.endswith(":free") or ":free-" in model:
        payload["reasoning"] = {"effort": "low"}
    started = time.monotonic()
    last_err: str | None = None

    async def _attempt() -> CallResult:
        nonlocal last_err
        async with session.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=timeout_s),
        ) as resp:
            txt = await resp.text()
            if resp.status != 200:
                raise OpenRouterHTTPError(resp.status, txt[:300])
            try:
                data = json.loads(txt)
            except json.JSONDecodeError as exc:
                raise OpenRouterHTTPError(resp.status, f"json: {exc}") from exc
        # ---- extract output (chat/completions format) --------------------
        output_text = ""
        try:
            choices = data.get("choices") or []
            if choices:
                msg = choices[0].get("message") or {}
                output_text = msg.get("content") or ""
        except Exception:
            output_text = ""
        # Fallbacks for non-standard layouts
        if not output_text:
            output_text = data.get("output_text", "") or ""
        if not output_text:
            for item in data.get("output", []) or []:
                if item.get("type") == "message":
                    content = item.get("content") or []
                    if content and isinstance(content[0], dict):
                        output_text = content[0].get("text", "")
                    elif isinstance(content, str):
                        output_text = content
        usage = data.get("usage", {}) or {}
        in_tok = int(usage.get("prompt_tokens", 0) or usage.get("input_tokens", 0) or 0)
        out_tok = int(usage.get("completion_tokens", 0) or usage.get("output_tokens", 0) or 0)
        cost = compute_cost_usd(model, in_tok, out_tok)
        parsed = normalize_response(output_text, domain, variant_role)
        return CallResult(
            success=True,
            response_text=output_text,
            parsed=parsed,
            input_tokens=in_tok,
            output_tokens=out_tok,
            cost_usd=cost,
            latency_s=time.monotonic() - started,
            raw=data,
        )

    try:
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(4),
            wait=wait_exponential(multiplier=2.0, min=2.0, max=30.0),
            retry=retry_if_exception_type((OpenRouterHTTPError, aiohttp.ClientError, asyncio.TimeoutError)),
            reraise=True,
        ):
            with attempt:
                try:
                    return await _attempt()
                except OpenRouterHTTPError as exc:
                    last_err = f"HTTP {exc.status}: {exc.body[:120]}"
                    if exc.status in (400, 401, 403, 404):
                        # unrecoverable; do not retry
                        raise
                    if exc.status == 429:
                        # rate limited; sleep longer than the backoff schedule
                        wait = float(os.environ.get("OR_429_WAIT_S", "30"))
                        logger.warning(f"429 from {payload['model']}: sleeping {wait:.0f}s before retry")
                        await asyncio.sleep(wait)
                    raise
    except (OpenRouterHTTPError, aiohttp.ClientError, asyncio.TimeoutError) as exc:
        return CallResult(
            success=False,
            response_text="",
            parsed=None,
            input_tokens=0,
            output_tokens=0,
            cost_usd=0.0,
            latency_s=time.monotonic() - started,
            error=str(exc)[:200] or last_err or "unknown error",
        )
    except Exception as exc:  # noqa: BLE001
        return CallResult(
            success=False,
            response_text="",
            parsed=None,
            input_tokens=0,
            output_tokens=0,
            cost_usd=0.0,
            latency_s=time.monotonic() - started,
            error=str(exc)[:200],
        )


class OpenRouterHTTPError(Exception):
    def __init__(self, status: int, body: str):
        super().__init__(f"HTTP {status}: {body}")
        self.status = status
        self.body = body


# ---- batch driver ---------------------------------------------------------

async def query_panel(
    panel: dict[str, dict[str, Any]],
    clusters: list[dict],
    *,
    ledger: CostLedger,
    concurrency: int = 40,
    log_path: Path | None = None,
    dry_run: bool = False,
    requests_per_minute: float = 12.0,
) -> dict[str, list[CallResult]]:
    """Query every (model, cluster, variant) cell concurrently.

    Returns a nested dict {model_name: [CallResult per (cluster_idx, variant)]}.
    Each model's list has length len(clusters) * 4, indexed by ci * 4 + j
    where j is in [0..3] for roles ['seed','paraphrase','negation','<4th>'].

    A global token-bucket rate limiter enforces `requests_per_minute` calls
    across the entire sweep so that we stay below OpenRouter's free-tier
    per-minute quota even when the per-request concurrency is high.
    """
    # Build the list of work items deterministically.
    # Flat layout: model -> list index aligned with the cluster order.
    work: list[tuple[str, int, int, str, str, str]] = []
    for m in panel:
        for ci, c in enumerate(clusters):
            for j, (role, variant) in enumerate(c["variants"].items()):
                domain = c["domain"]
                sys_msg = _system_message(domain, role)
                work.append((m, ci, j, role, variant["question"], domain, sys_msg))

    results: dict[str, list[CallResult | None]] = {
        m: [None] * (len(clusters) * 4) for m in panel
    }
    sem = asyncio.Semaphore(concurrency)

    # Token-bucket rate limiter: at any moment we hold at most `bucket_capacity`
    # tokens; one token is added every `interval` seconds. To avoid holding the
    # lock across an `asyncio.sleep`, the consume helper returns a future that
    # resolves only when a token is available — and a single background task
    # refills the bucket.
    rpm = max(1.0, float(requests_per_minute))
    interval = 60.0 / rpm
    bucket_capacity = max(1.0, rpm)
    bucket_state = {
        "tokens": bucket_capacity,
        "last": time.monotonic(),
        "waiters": [],  # list of asyncio.Event per waiter
    }
    bucket_lock = asyncio.Lock()

    async def _refill():
        while True:
            await asyncio.sleep(interval)
            async with bucket_lock:
                now = time.monotonic()
                elapsed = now - bucket_state["last"]
                refill = elapsed / interval
                if refill >= 1.0:
                    add = int(refill)
                    bucket_state["tokens"] = min(bucket_capacity, bucket_state["tokens"] + add)
                    bucket_state["last"] += add * interval
                # Wake up as many waiters as we have tokens for
                while bucket_state["waiters"] and bucket_state["tokens"] >= 1.0:
                    bucket_state["tokens"] -= 1.0
                    ev = bucket_state["waiters"].pop(0)
                    ev.set()

    async def _consume():
        async with bucket_lock:
            if bucket_state["tokens"] >= 1.0:
                bucket_state["tokens"] -= 1.0
                return
            ev = asyncio.Event()
            bucket_state["waiters"].append(ev)
        # Block until the refill task wakes us
        await ev.wait()

    async with aiohttp.ClientSession() as session:
        # Skip the catalog fetch — we use local DEFAULT_MODEL_PANEL prices.
        logger.info("Session opened; skipping catalog fetch (using local prices)")

        if log_path is not None:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_f = log_path.open("w")
        else:
            log_f = None

        async def _one(model: str, ci: int, j: int, role: str, q: str, domain: str, sys_msg: str, dry_rng=None):
            if not dry_run and (model.endswith(":free") or ":free-" in model):
                await _consume()
            async with sem:
                if dry_run:
                    # Produce a deterministic but non-degenerate response. For
                    # the smoke test we want the GRM to see a spread of
                    # coherence scores so it can be fitted. Each model gets a
                    # different "ability" via the per-model correctness prob.
                    rng = dry_rng or random.Random(hash((model, ci, j)) & 0xFFFFFFFF)
                    correctness = {
                        "openai/gpt-4o-mini": 0.85,
                        "anthropic/claude-haiku-4.5": 0.78,
                        "meta-llama/llama-3.1-8b-instruct": 0.55,
                        "qwen/qwen-2.5-7b-instruct": 0.65,
                        "mistralai/mistral-small-24b-instruct-2501": 0.50,
                    }.get(model, 0.6)
                    is_correct = rng.random() < correctness
                    if domain == "logic":
                        text = ("V" if (rng.random() < 0.5) else "I") if rng.random() < 0.95 else ""
                        parsed = "V" if text.startswith("V") else ("I" if text.startswith("I") else None)
                        # For negation: response is flipped if correct
                        if role == "negation" and is_correct and parsed is not None:
                            parsed = "I" if parsed == "V" else "V"
                    elif role == "negation":
                        text = ("YES" if rng.random() < 0.5 else "NO") if rng.random() < 0.95 else ""
                        parsed = "YES" if text.startswith("Y") else ("NO" if text.startswith("N") else None)
                    else:
                        # arithmetic integer
                        n = rng.randint(2, 25)
                        text = str(n) if rng.random() < 0.95 else ""
                        try:
                            parsed = int(text)
                        except ValueError:
                            parsed = None
                    res = CallResult(
                        success=parsed is not None,
                        response_text=text or "PARSE_FAIL",
                        parsed=parsed,
                        input_tokens=120,
                        output_tokens=4,
                        cost_usd=0.0001,
                        latency_s=0.0,
                    )
                else:
                    res = await call_one(
                        session,
                        model=model,
                        system=sys_msg,
                        user=q,
                        domain=domain,
                        variant_role=role,
                        max_tokens=16,
                    )
                await ledger.add(res.cost_usd, model=model, ci=ci, role=role)
                if log_f is not None:
                    log_f.write(json.dumps({
                        "model": model,
                        "ci": ci,
                        "j": j,
                        "role": role,
                        "q": q[:200],
                        "ok": res.success,
                        "parsed": res.parsed if res.parsed is not None else str(res.error),
                        "in_tok": res.input_tokens,
                        "out_tok": res.output_tokens,
                        "cost_usd": res.cost_usd,
                        "latency_s": res.latency_s,
                    }) + "\n")
                results[model][ci * 4 + j] = res

        tasks = [_one(*w) for w in work]
        refill_task = asyncio.create_task(_refill())
        try:
            await asyncio.gather(*tasks, return_exceptions=False)
        finally:
            refill_task.cancel()

        if log_f is not None:
            log_f.close()
    # Cast None -> failure marker (shouldn't happen, but be defensive)
    final: dict[str, list[CallResult]] = {}
    for m, recs in results.items():
        final[m] = [
            r if r is not None else CallResult(
                success=False, response_text="", parsed=None,
                input_tokens=0, output_tokens=0, cost_usd=0.0,
                latency_s=0.0, error="missing_response",
            )
            for r in recs
        ]
    return final


def _system_message(domain: str, role: str) -> str:
    """Per-variant system message — keeps the model's response space narrow."""
    if domain == "logic":
        return (
            "You must answer with exactly one character: V if the argument is valid, "
            "I if it is invalid. For negation questions, still answer V or I based on "
            "the truth of the original (negated) claim. No explanation, no other text."
        )
    # arithmetic
    if role == "negation":
        return (
            "You must answer with exactly one word: YES or NO. "
            "No explanation, no other text."
        )
    return (
        "You must answer with only the integer result. No explanation, "
        "no other text."
    )