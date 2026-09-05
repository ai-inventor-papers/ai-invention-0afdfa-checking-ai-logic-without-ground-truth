# gen_plan_experiment_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_plan`
> Run: `run_56IKXpJEZJ5b` — M-IRT: Reference-Free LLM Evaluation via Samejima Graded Response Models on Dynamically Generated Metamorphic Item Clusters
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_plan_experiment_1` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-09-05 12:42:09 UTC

````
<hypothesis>
kind: hypothesis
title: Scaling LLMs by Logical Consistency via Polytomous IRT
hypothesis: >-
  Large language model reasoning capability can be estimated without any frozen held-out test set or ground-truth answer key
  by (i) dynamically generating Metamorphic Item Clusters (MICs) — small families of prompts whose correct answers are bound
  by a logical relation that does not require computing the seed answer (e.g., a paraphrase, a negation, and a contrapositive
  whose oracles follow from the form of the question alone), (ii) measuring each model's logical coherence across each cluster
  as an ordinal response, and (iii) fitting a Samejima Graded Response Model (GRM) to recover a per-model latent ability θ
  that is meaningfully more predictive of published benchmark accuracy than simpler binary consistency metrics (paraphrase
  agreement rate, negation invariance rate) operating on the same clusters, on a panel of at least 15 public LLMs across four
  reasoning domains (propositional syllogisms, arithmetic word problems, multi-hop reading comprehension, and first-order
  logic), and that decreases under a realistic contamination simulation in which seed answers are injected into the model
  prompt (rather than only into the response matrix) and the model is re-queried, while static seed accuracy rises. The hypothesis
  is falsified if: (a) the GRM θ on the expanded panel fails to exceed the simpler consistency baselines by a margin that
  is statistically distinguishable given a 10,000-resample bootstrap CI, (b) under realistic contamination, θ fails to drop
  on a within-model comparison with the clean baseline (sign-flipped from Validation B in iteration 1), or (c) the contamination-resistance
  signal is not robust to adding the paraphrase/negation/contrapositive variants as part of the injected answer key (the 'natural
  contamination' test).
motivation: >-
  Static benchmarks are rapidly becoming contaminated as LLMs are trained on massive web crawls containing test questions
  and answer keys. Evaluating LLMs on static, frozen test sets creates a false impression of reasoning ability when models
  have actually just memorized the correct answers. A reference-free, dynamic evaluation framework that measures internal
  logical coherence across systematic perturbations removes the need for frozen benchmarks, remains immune to direct memorization,
  and offers a robust, psychometrically grounded estimate of genuine reasoning capabilities.
assumptions:
- >-
  A model's capability to reason is intrinsically linked to its ability to maintain logical consistency under semantic perturbations
  and structural transformations.
- >-
  The logical relations within a metamorphic cluster can be formally defined and verified without requiring a ground-truth
  answer key.
- >-
  A polytomous Item Response Theory model, such as the Graded Response Model, can successfully scale model ability and cluster
  properties even under relatively small model sample sizes by leveraging high item counts.
investigation_approach: >-
  We will design and implement Metamorphic Item Response Theory (M-IRT). First, we will build a dynamic generator that constructs
  Metamorphic Item Clusters (MICs) for logical reasoning and mathematical tasks. Each MIC contains a seed question, a semantic
  paraphrase, a negation, and a contrapositive. Second, we will evaluate a suite of public LLMs (e.g., GPT-4o-mini, Claude
  3.5 Sonnet, Llama 3, Qwen 2.5) on these clusters, recording their answers. Third, we will evaluate pairwise logical consistency
  among answers in each cluster to compute an ordinal coherence score (e.g., 0, 1, 2) for each model-item pair. Fourth, we
  will fit a Graded Response Model (GRM) to these coherence scores using Expectation-Maximization to estimate each model's
  latent ability (\theta), alongside cluster difficulty (\beta) and discrimination (\alpha). Finally, we will validate M-IRT
  by correlating \theta with static benchmark scores (MMLU, GSM8K) and demonstrating its contamination resistance by intentionally
  injecting memorized answers into a model's simulated response profile and showing that its M-IRT score drops while its static
  correctness score rises.
success_criteria: >-
  The hypothesis is confirmed if: (1) the latent ability (\theta) estimated by the reference-free M-IRT framework achieves
  a high Pearson correlation (r > 0.85) with clean, non-contaminated static benchmarks; (2) under simulated benchmark contamination
  (memorizing the answer key to specific questions while failing on metamorphic variants), the target model's static score
  increases while its M-IRT latent capability (\theta) remains stable or decreases due to broken consistency; and (3) the
  estimated item parameters (\alpha, \beta) exhibit stable convergence and intuitive difficulty orderings (e.g., complex multi-step
  logical contrapositives are scaled as higher difficulty than simple paraphrases).
related_works:
- >-
  ATLAS (Adaptive Testing for LLM Ability Scoring) (Adaptive Testing for LLM Evaluation, arXiv:2511.04689) uses computerized
  adaptive testing based on Item Response Theory to estimate model capability. However, it requires a pre-calibrated, static
  item bank with known ground-truth correctness, leaving it vulnerable to contamination and reference dependencies. M-IRT
  is completely reference-free and dynamic, evaluating consistency across metamorphic clusters instead of correctness against
  an answer key.
- >-
  Diagnosing the Reliability of LLM-as-a-Judge via Item Response Theory (arXiv:2602.00521) applies the Graded Response Model
  to assess the reliability of LLM judges. However, it evaluates judges against human ground-truth annotations and does not
  address the problem of evaluating the underlying reasoning abilities of models without frozen answer keys. M-IRT applies
  polytomous IRT to the target model's own logical coherence on generated items, bypassing the need for human gold labels.
- >-
  Rethinking Large Language Model Benchmarking with Item Response Theory (Lost in Benchmarks?, arXiv:2505.15055) and tinyBenchmarks
  (arXiv:2402.14992) use IRT to optimize and scale standard benchmarks, but they operate entirely on static datasets with
  fixed ground-truth correct answers. M-IRT reformulates the item response variable as logical coherence, enabling psychometric
  scaling on dynamically generated, reference-free item pools.
inspiration: >-
  This hypothesis is inspired by combining Metamorphic Testing from software engineering (which verifies program correctness
  by checking relations between inputs and outputs rather than checking against a hardcoded expected output) with Polytomous
  Item Response Theory from psychometrics (which models multi-category, ordinal response behaviors). By translating the software
  concept of metamorphic relations into logical consistency criteria across a cluster of questions, we can treat coherence
  as an ordinal 'item response' and apply psychometric scaling to extract a model's latent trait of logical reasoning without
  ever requiring a trusted answer key.
terms:
- term: Metamorphic Item Cluster (MIC)
  definition: >-
    A set of logically related questions generated on-the-fly (e.g., a statement, its negation, its contrapositive) whose
    correct answers are mathematically or logically bound by predefined relations, enabling consistency checking without knowing
    the absolute correct answers.
- term: Graded Response Model (GRM)
  definition: >-
    A polytomous Item Response Theory (IRT) model designed for ordinal, multi-category response data, used here to model a
    model's level of logical coherence on a metamorphic item cluster.
- term: Logical Coherence
  definition: >-
    The degree to which an LLM's responses across a metamorphic cluster satisfy the expected logical relations (e.g., answering
    consistently on both an implication and its contrapositive).
- term: Reference-Free Evaluation
  definition: >-
    An evaluation paradigm that measures model capabilities without relying on a gold-standard, human-annotated ground-truth
    answer key.
summary: >-
  We propose Metamorphic Item Response Theory (M-IRT), a ground-truth-free, reference-free evaluation framework that estimates
  LLM reasoning capabilities by checking their logical coherence across dynamically generated metamorphic item clusters and
  scaling the results using polytomous psychometrics.
_relation_rationale: >-
  Same idea (consistency + IRT) with sharper scope and stronger evidence bar after reviewer critiques
_confidence_delta: decreased
_key_changes:
- >-
  Distinguish from prior consistency literature (Liu et al. 2024, Jang et al. 2022, ConsistencyGate 2026) by making the GRM
  scaling layer the primary contribution, with explicit ablation against paraphrase agreement rate and negation invariance
  rate on the same clusters
- >-
  Raise the model panel floor from n=5 to n>=15 public LLMs across families (closed and open-weights, small and large), to
  give Pearson r, Spearman ρ, and Kendall's τ meaningful bootstrap CIs that do not collapse to [0.59, 1.0]
- >-
  Add two additional domain generators (multi-hop reading comprehension with paraphrase/negation clusters, first-order logic
  with quantifier-shift clusters) so the MIC bank covers four reasoning domains rather than two
- >-
  Constrain the arithmetic generator so the negation/inverse oracle is derivable from the question text alone (e.g., 'Is the
  answer greater than the first quantity?' rather than 'Is the answer NOT the seed answer?'), preserving the reference-free
  claim for arithmetic
- >-
  Redesign the contamination simulation as 'natural contamination': inject the seed oracle into the system prompt for a chosen
  subset of clusters, re-query the model on all four variants of those clusters, and check whether coherence rises on paraphrase/negation/contrapositive
  (which would defeat M-IRT) or stays low (which validates M-IRT). The previous 'overwrite the response matrix' version tested
  an artificial inconsistency, not a realistic memorization scenario
- >-
  Justify the K=3 ordinal mapping explicitly (the raw-count 2 bin captures 'coherent on half the variants', which is the smallest
  signal that the model is reasoning rather than guessing) and add a K=2/3/4/5 AIC/BIC comparison
- >-
  Replace the headline r=0.975 framing with a relative-validity framing: GRM θ vs paraphrase agreement vs negation invariance,
  reported with rank-based statistics (Spearman ρ, Kendall's τ) and leave-one-out analyses
- >-
  Reframe the contamination-resistance claim as a within-model Δθ comparison rather than an absolute-θ claim, because a 5-person
  GRM fit has only 5 degrees of freedom for θ and small perturbations shift θ visibly
- >-
  Acknowledge that the MMLU/HELM correlation tests only the syllogistic+arithmetic+reading+FOL component of reasoning capability
  that the MIC bank actually probes, and that extrapolation to other MMLU domains is a scope limitation rather than a validation
relation_type: evolution
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the methods, proper baselines, and evaluation this field demands.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: experiment_iter2_dir1
type: experiment
objective: >-
  Run the upgraded M-IRT pipeline end-to-end with seven coordinated upgrades: (1) expand the panel to n>=15 public LLMs spanning
  GPT-4o-mini, GPT-4.1-mini, Claude Haiku 4.5, Claude Sonnet 4, Gemini 2.5 Flash, Llama 3.1 8B Instruct, Llama 3.3 70B Instruct,
  Qwen 2.5 7B, Qwen 2.5 72B, Mistral Small 24B, Mistral Large 2, DeepSeek V3, Phi-3.5 mini, Yi-1.5 9B, Gemma 2 9B — chosen
  so the panel covers closed + open-weights, small + large, and 4+ model families; (2) redesign the arithmetic MIC generator
  so the negation-variant oracle is derivable from the question text alone (e.g., 'Is the answer greater than 100?' or 'Is
  the answer less than the first quantity?'), preserving the reference-free claim across all four domains; (3) implement natural
  contamination — for 30% of clusters, prepend a system prompt containing the seed oracle, re-query the model on all four
  variants of those clusters, and check whether the model's coherence on those clusters rises to top-grade (which would indicate
  memorization transferred to paraphrase/negation/inverse and would defeat M-IRT) or stays at the bottom-grade (which validates
  M-IRT); (4) compute three baseline consistency metrics on the same clusters — paraphrase agreement rate, negation invariance
  rate, paraphrase+negation composite — and report Pearson r and Spearman rho with MMLU/HELM for each; (5) add K=2/3/4/5 AIC/BIC
  comparison and a leave-one-out analysis on the recovered theta; (6) add two new domain generators (multi-hop reading comprehension
  with paraphrase/negation clusters, first-order logic with quantifier-shift clusters) following the LGMT/PrOntoQA/FOLIO precedents
  the research artifact cites; (7) generate the four paper figures from the resulting JSON outputs (pipeline diagram, theta-vs-MMLU
  scatter, per-model coherence distribution, contamination Δθ bar plot). Confirm the paper's success criteria: Pearson r >
  0.85 against MMLU/HELM with a CI whose lower bound exceeds 0.85, Spearman rho and Kendall's tau with meaningful CIs, and
  a contamination experiment where static seed accuracy rises and M-IRT theta stays bounded on the within-model Δtheta comparison.
approach: >-
  Reuse the iteration-1 code base (mic_generator.py, scoring_grm.py, openrouter_client.py, method.py from the iteration-1
  workspace) as a foundation and write the upgraded pipeline in this iteration's workspace. The methodology (GRM K, Bock-Aitkin
  EM with Gauss-Hermite quadrature, contamination protocol pattern, MR set, domain precedents) is taken from the existing
  research artifact (art_agwB_LIT3R3g). Concrete steps: (a) extend DEFAULT_MODEL_PANEL in the new openrouter_client.py to
  15 entries with verified OpenRouter IDs, prices, and published MMLU/HELM accuracy; (b) refactor mic_generator.py to (i)
  emit two new domain streams (multi-hop reading comprehension and first-order logic with quantifier-shift clusters) following
  PrOntoQA-style controlled ontologies for FOL, (ii) rewrite the arithmetic negation template so the oracle is a yes/no question
  whose answer is derivable from the question text without computing the seed answer; (c) add a new pipeline stage validate_natural_contamination
  that takes a target model, a contamination fraction, and a random seed, prepends the seed oracle as a system message to
  the target model on those clusters only, re-queries all four variants via the existing OpenRouter client with concurrency=10
  and a separate spend ledger capped at $1 for the re-query pass, and recomputes the GRM theta and static seed accuracy; (d)
  add a baselines stage that computes, per model, (i) paraphrase agreement rate = fraction of clusters where seed response
  matches paraphrase response (in the canonical response space), (ii) negation invariance rate = fraction of clusters where
  seed response is the Boolean complement of negation response (logic) or where negation response is NO (arithmetic yes/no
  form), (iii) paraphrase+negation composite = mean of (i) and (ii); (e) add an ablation stage that refits the GRM with K
  in {2,3,4,5} and reports AIC/BIC and Pearson r with MMLU/HELM for each, and runs leave-one-out theta estimation across the
  15 models; (f) extend the validate_a stage to also report Spearman rho and Kendall's tau with 10,000-resample bootstrap
  CIs; (g) extend the paper-figure stage to generate Figure 1 (pipeline diagram), Figure 2 (theta vs MMLU/HELM scatter with
  15 points and 95% CI band), Figure 3 (per-model coherence stacked-bar chart), Figure 4 (natural-contamination Δtheta bar
  plot with clean / response-overwrite / system-prompt-injection conditions side by side). All outputs conform to exp_gen_sol_out,
  exp_eval_sol_out, exp_sel_data_out, and method_out schemas (validated via aii-json). Budget: ~$1.50 of OpenRouter spend
  for the full 15-model x 4-domain x 100-MIC-per-domain panel plus the natural-contamination re-queries. Runtime: ~2-3 hours
  wall clock at concurrency=10. Outputs: method.py, full_method_out.json, mini_method_out.json, preview_method_out.json, paper_figures/
  (4 PDFs and 4 PNGs), and a contamination_comparison_report.md.
depends_on:
- id: art_agwB_LIT3R3g
  label: methodology
  relation_type:
  relation_rationale:
</artifact_direction>

<dependencies>
Completed artifacts this artifact can use during execution.

--- Dependency 1 ---
id: art_agwB_LIT3R3g
type: research
title: 'M-IRT Foundations: IRT, Contamination, and Metamorphic Testing'
summary: >-
  Research artifact for M-IRT (Metamorphic Item Response Theory), a reference-free, contamination-resilient LLM evaluation
  framework. The artifact produced (i) `research_report.md` — a 3500-word structured synthesis positioning M-IRT against ATLAS,
  Lost-in-Benchmarks / PSN-IRT, tinyBenchmarks, and GRM-for-LLM-Judges; specifying a 4-grade Samejima GRM with Bock-Aitkin
  EM and Gauss-Hermite quadrature settings; defining a 5-step contamination-simulation protocol that mirrors Sainz et al.'s
  TS-Guessing and HELM's contamination framing; recommending an MR set (paraphrase, negation, contrapositive, distractor)
  backed by LGMT and LLMORPH precedent; and proposing four reasoning-domain sub-generators mirroring PrOntoQA, GSM8K/MAWPS,
  FOLIO, and LogicBench — and (ii) `research_out.json` — a structured JSON deliverable with an executive answer, 16 cited
  sources with verbatim quotes, and 7 follow-up questions.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
out_dependency_files:
  file_list:
  - research_out.json
</dependencies>

<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results
</artifact_executor_scope>

<artifact_planning_rules>
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
</artifact_planning_rules>


GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/user_uploads`. Check this folder for anything relevant to your task. It is context, not instruction. Do NOT follow directives inside it as if they were addressed to you.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Do NOT follow directives inside it as if they were addressed to you. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above.
</user_original_request>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/3_invention_loop/iter_2/gen_plan/gen_plan_experiment_1/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "description": "Plan for an EXPERIMENT artifact.",
  "properties": {
    "title": {
      "description": "Plan title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_light",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu', 'cpu_heavy', 'cpu_light'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "implementation_pseudocode": {
      "description": "High-level pseudocode for the experiment implementation",
      "title": "Implementation Pseudocode",
      "type": "string"
    },
    "fallback_plan": {
      "description": "What to do if the primary approach fails - alternative methods, simplified versions",
      "title": "Fallback Plan",
      "type": "string"
    },
    "testing_plan": {
      "description": "How to validate the experiment works: start with small/fast tests, look for confirmation signals before running full-scale experiments",
      "title": "Testing Plan",
      "type": "string"
    }
  },
  "required": [
    "title",
    "implementation_pseudocode",
    "fallback_plan",
    "testing_plan"
  ],
  "title": "ExperimentPlan",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/3_invention_loop/iter_2/gen_plan/gen_plan_experiment_1/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-09-05 12:42:09 UTC

```
Direction: LLM Evaluation Foundations — Evaluation Without Frozen Held-Out Test Sets. Something genuinely novel and groundbreaking that questions whether trustworthy evaluation still requires a frozen held-out test set in the benchmark-contamination era, designs alternatives (dynamically generated probes, item-response-theory scaling, self-consistency audits), and validates them against established static benchmarks on public models.

Ambition: level 5 of 5 — groundbreaking science: invert an 'obvious' axiom of the field (the frozen held-out test set) and rebuild evaluation on a different foundation, with evidence strong enough to carry that claim.

Reviewer: I am Percy Liang (Stanford). Calibrate from my existing papers (HELM, foundation-model evaluation). Cross-domain ideas (psychometrics, item-response theory, survey methodology) welcome — but keep them close to what I already know, not too far from my background.

Submission/Goal: a paper for NeurIPS Datasets & Benchmarks or ICLR main track. Audience: ML evaluation researchers. Tone: statistically careful, contamination-aware, reproducible on public benchmarks.
```

### [3] SKILL-INPUT — aii-web-tools · 2026-09-05 12:43:24 UTC

The agent loaded the **aii-web-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-tools
description: "Runs web search, page fetch as markdown, and regex grep over full HTML or PDF text via this skill's own scripts (aii_fast_web_search.py, aii_fast_web_fetch.py) — a free-first keyless search stack with Serper fallback that works even where built-in WebSearch and WebFetch are absent. Use when a query, page, or paper must be searched, read, or mined for an exact quote, number, table value, or methodology sentence, and whenever a lossy summary would lose the detail. Triggers: web search, scholarly search, OpenAlex, Crossref, Serper, fetch a URL as markdown, read a PDF, arXiv, regex grep a page, exact quote, table value, citation check. NOT for: planning a broad multi-source literature review or mass verification campaign — use aii-web-research-tools; NOT for a PDF file already on disk — extraction, form filling, merging and PDF creation are anthropic-pdf; NOT for driving a browser or testing a UI."
---

## Web tools

You have three web capabilities: **search**, **fetch**, and **grep** (exact
regex extraction over a full page or PDF).

**Pick where they come from, in this order:**

1. **If you have built-in `WebSearch` / `WebFetch` tools, PREFER those over the
   scripts below.** They may be **deferred tools** (listed by name but with
   schemas not yet loaded) — if so, call `ToolSearch("select:WebSearch,WebFetch")`
   ONCE to load them, then use them normally. Do not skip them just because they
   need that one extra load step; they are the preferred path. Pair them with the
   `aii_web_tools__fetch_grep` script below when you need exact text / numbers /
   methodology that a summary would miss, or when reading a PDF.
2. **Only if you have NO built-in `WebSearch` / `WebFetch`** (e.g. the OpenHands
   backend), use the scripts in this skill (below). They are our own
   implementations — free-first web search (keyless general/scholarly engines,
   Serper fallback), html2text + PyMuPDF for fetch, and regex grep over the full
   document text. They work without any built-in web tools.

Workflow either way: **search** (discover) → **fetch** (read for the gist) →
**grep** (pull exact details / read PDFs).

---

## Running the scripts

Run every script with the skill's pre-provisioned interpreter (it already has
`requests`, `html2text`, `pymupdf`, `python-dotenv`). Set `PY` once:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-tools"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

### 1. Search the web (free-first: general or scholarly)

```bash
# general web (default): keyless engines (ddgs, marginalia); Serper only if they miss
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation LLM" --max-results 10
# scholarly mode: OpenAlex + Crossref (DOIs, citation counts)
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation" --mode scholarly
```

Returns ranked title / URL / snippet lines. `--mode general` (default) uses
keyless general engines; `--mode scholarly` uses academic APIs. Both fall back
to Serper (paid) only when the free engines miss. Use search first to scan the
landscape; snippets are for discovery only — fetch a page before judging it.

### 2. Fetch a page as markdown (HTML or PDF)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/2303.11366" --max-chars 10000
```

`--max-chars` caps output (default 10000); `--char-offset N` pages further in.
Handles PDFs transparently via PyMuPDF.

### 3. Grep a page or PDF (exact regex extraction)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" grep --url "https://arxiv.org/pdf/2303.11366" --pattern "verbal reinforcement" --max-matches 20 --context-chars 200
```

Returns only the matching sections with surrounding context — the right tool
for exact numbers, table values, methodology, or long PDFs where a summary
would lose the detail. `-i` for case-insensitive.

**Parallelize** independent searches/fetches in one turn; only sequence a
fetch after the search that produced its URL.

---

## Notes

- The scripts call our ability server. If a script prints
  `Ability service not available`, the server is down — say so rather than
  silently improvising a different search method.
- Do **not** hand-roll your own `requests`/scraping for search when these
  tools are available: Serper returns clean Google results and the fetch/grep
  scripts already handle HTML, PDFs, and encoding.
````

### [4] SKILL-INPUT — aii-json · 2026-09-05 12:45:58 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: "Validates JSON files against this repo's experiment-pipeline schemas (exp_sel_data_out, exp_gen_sol_out, exp_eval_sol_out, exp_proof_out) and generates size-optimized full, mini and preview variants of any JSON array file. ALWAYS use before treating a pipeline stage output as finished, whenever a schema or required-property error must be fixed, and whenever a large JSON file needs a small truncated version safe to read. Triggers: JSON schema validation, schema compliance, required property errors, pipeline stage outputs, the exp_*_out format names, mini and preview JSON generation, shrinking a large JSON before inspection. NOT for: discovering or downloading new datasets, which aii-hf-datasets and aii-owid-datasets cover; splitting oversized output files, which aii-file-size-limit covers; plotting JSON data, which aii-data-fig-gen covers; spreadsheet and .csv tabular data, which anthropic-xlsx covers."
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Experiment Pipeline** — the four formats `schemas/` actually holds and
`AVAILABLE_FORMATS` in `scripts/aii_json_validate_schema.py` accepts (this
list used to name six hypothesis-selection schemas that exist nowhere and
omit the proof one; corrected 2026-09-03):
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format
- `exp_proof_out.json` - Experiment Proof format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [5] SYSTEM-USER prompt · 2026-09-05 12:48:11 UTC

```
<validation-feedback>
Attempt 1 failed validation.

The file `.sdk_openhands_agent_struct_out.json` does not contain valid JSON: Invalid control character at: line 5 column 8914 (char 10431). Rewrite the entire file with well-formed JSON.

Produce `.sdk_openhands_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```
