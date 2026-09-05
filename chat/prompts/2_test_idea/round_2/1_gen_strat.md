# gen_strat_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_strat`
> Run: `run_56IKXpJEZJ5b` — M-IRT: Reference-Free LLM Evaluation via Samejima Graded Response Models on Dynamically Generated Metamorphic Item Clusters
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_strat_1` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-09-05 12:38:12 UTC

````
<hypothesis>
Your strategy should advance this hypothesis.

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
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for study design, proper baselines, and the evaluation/validity norms this field demands.

- **aii-handbook-auto-computational-linguistics** — Field handbook for computational linguistics as a SCIENCE of language — grammaticality and minimal pairs (BLiMP), surprisal versus reading times, linguistic structure in LMs, annotator disagreement an
- **aii-handbook-auto-mechanistic-interpretability** — Field handbook for mechanistic interpretability of neural networks — circuit discovery, activation and attribution patching, sparse autoencoders, transcoders, attribution graphs, steering vectors, pro
- **aii-handbook-auto-multi-agent-llm-systems** — Field handbook for multi-agent LLM systems (MAS) — orchestration topology, multi-agent debate, mixture-of-agents, verifier and critic agents, inter-agent protocols (MCP/A2A), failure attribution and s
- **aii-handbook-auto-neurosymbolic** — Field handbook for neuro-symbolic AI — text-to-logic autoformalization (NL to FOL), LLM-plus-solver and prover pipelines (Prolog, ASP, SMT), probabilistic-differentiable NeSy (DeepProbLog, Scallop), r
</available_domain_handbooks>

<iteration_status>
Current iteration: 2 of 2
Remaining (including this one): 1
</iteration_status>

<previous_strategies>
Strategies from the PREVIOUS iteration. You can CONTINUE these directions,
ADAPT based on what worked and what didn't in the artifacts produced, or PIVOT if results suggest a better path.

--- Strategy 1 ---
kind: strategy
id: gen_strat_1_idx1
title: 'M-IRT: Coherence-Based Evaluation Without Frozen Tests'
objective: >-
  Build the first end-to-end Metamorphic Item Response Theory (M-IRT) prototype that (a) generates Metamorphic Item Clusters
  (MICs) on the fly, (b) scores logical coherence on an ordinal 0/1/2 scale across a panel of public LLMs, (c) fits a Graded
  Response Model to recover latent ability θ, and (d) demonstrates that θ tracks clean static benchmark scores while remaining
  robust — or even degrading — when a model is simulated to have memorized the answer key (where static accuracy rises). This
  is the load-bearing evidence that evaluation can be rebuilt on logical coherence rather than frozen test sets.
rationale: >-
  Percy Liang's HELM established that frozen, public test sets are vulnerable to contamination and that broad-spectrum, transparent
  evaluation is the antidote. The next logical step is to question whether a frozen test set is needed at all. M-IRT fuses
  two ideas that are individually well-developed but have not been combined this way: metamorphic testing from software engineering
  (relations between inputs imply relations between outputs, no oracle required) and polytomous IRT from psychometrics (the
  Graded Response Model for ordinal responses). The hardest, most reviewable claim is contamination resistance — if M-IRT's
  θ moves in the OPPOSITE direction of static accuracy under simulated memorization, that is the headline result. The hypothesis's
  r>0.85 criterion against clean benchmarks is the validity check that prevents the contamination story from being dismissed
  as 'just measuring noise.' Doing both in one experiment produces a tight, publishable contribution for NeurIPS D&B / ICLR.
artifact_directions:
- id: experiment_iter1_dir1
  type: experiment
  objective: >-
    Implement and run the full M-IRT pipeline end-to-end: dynamic MIC generator for two reasoning domains (propositional logic
    with syllogistic-style templates and basic arithmetic word problems with bound relations), model evaluation panel, ordinal
    coherence scoring, GRM fitting via MML with Gauss-Hermite quadrature, validation against published HELM/MMLU accuracy
    for the same models, and a contamination simulation in which one model's responses on a held-out subset of seed items
    are forcibly replaced with the correct answer (mimicking memorization of the answer key). Confirm both success criteria:
    (i) Pearson r > 0.85 between M-IRT θ and clean published accuracy, and (ii) under simulated contamination the target model's
    static accuracy on the seeds increases while its M-IRT θ decreases (or stays stable) because coherence is broken on the
    paraphrase/negation/contrapositive variants.
  approach: |-
    Pipeline stages:
    1. MIC GENERATOR (Python): Two domain generators that produce 4-variant clusters (seed, paraphrase, negation, contrapositive for logic; seed, paraphrase, negation, arithmetic inverse for math word problems). Use templated generation with stochastic entity/slot filling plus an LLM-assisted paraphrase step (gpt-4o-mini via OpenRouter, kept cheap). Target ~250 MICs across both domains (125 per domain). Validate generated clusters with an automated oracle check on a 20% sample to confirm metamorphic relations hold (e.g., a model that answers 'A' on the seed of a valid syllogism must answer 'B' on its negation, by construction).
    2. MODEL PANEL: Evaluate 5 public models via OpenRouter spanning capability tiers — e.g., gpt-4o-mini, claude-3-5-haiku, llama-3.1-8b-instruct, qwen-2.5-7b-instruct, mistral-7b-instruct. Use temperature=0 and a deterministic prompt template asking for letter/short answer. Each model produces 250 MICs × 4 variants = 1000 responses. Budget ~$3 of OpenRouter spend.
    3. COHERENCE SCORING: For each model-MIC pair, compute an ordinal score: 2 if consistent across all 4 variants (semantic paraphrase agrees, negation agrees per construction, contrapositive agrees), 1 if partially consistent (e.g., paraphrase agrees but negation contradicts), 0 if no consistent pair. Save a (model, item, score) long-format table.
    4. GRM FITTING: Implement GRM via marginal maximum likelihood with Gauss-Hermite quadrature (or use a battle-tested Python IRT library). Estimate θ_j for each model, α_i (discrimination) and β_{i,k} (thresholds) for each item. Verify intuitive difficulty ordering: negation/contrapositive variants scale harder than paraphrases.
    5. VALIDATION A (correlation): Look up or scrape HELM/MMLU aggregate accuracy for the 5 models. Compute Pearson r and 95% CI between M-IRT θ and static accuracy. Success: r > 0.85.
    6. VALIDATION B (contamination simulation): Pick the middle-capability model. On a random 30% of seed items, replace its answer with the oracle's correct answer (simulating memorization of the answer key). Recompute (a) its static accuracy on the seeds (should rise) and (b) its M-IRT θ (should drop because paraphrase/negation/contrapositive answers remain uncoordinated). Repeat with 3 random seeds; report mean effect.
    Output: experiment_out.json with all θ, α, β estimates, the full score matrix, validation tables, and a contamination simulation report. Logs: model-by-model call counts and OpenRouter spend.
  depends_on: []
- id: research_iter1_dir2
  type: research
  objective: >-
    Ground the methodology in prior work and surface the most defensible design choices (GRM fitting procedure, ordinal scoring
    rubric, contamination-simulation protocol, choice of reasoning domains) so that reviewers — particularly those with a
    HELM/benchmark-design background — see the framework as principled rather than ad hoc. Identify the strongest existing
    baselines for IRT-based LLM evaluation and the cleanest prior contamination-resistance claims so the paper's positioning
    is precise.
  approach: |-
    Produce a research_report.md that surveys and synthesizes:
    1. IRT for LLM evaluation: ATLAS (arXiv:2511.04689), 'Lost in Benchmarks?' (arXiv:2505.15055), tinyBenchmarks (arXiv:2402.14992), the GRM-for-judges paper (arXiv:2602.00521). Extract specifically: (a) whether they require ground truth (yes — M-IRT's novelty), (b) what model/IRT family they use, (c) their reported correlations with static benchmarks, (d) whether they test contamination.
    2. Contamination resistance: Ni et al. (HELM contamination discussion), Roberts et al. on benchmark contamination, 'Is Your Benchmark Contaminated?' ( Sainz et al.), and any LLM-evaluation papers that explicitly simulate memorization. Capture their methodology so the contamination simulation in the experiment mirrors field-standard practice.
    3. Metamorphic testing for NLP/LLM: Xie et al. metamorphic testing survey, recent metamorphic-relation papers for QA/summarization. Confirm that the chosen metamorphic relations (negation, contrapositive, paraphrase) have prior precedent in NLP metamorphic testing — this is the foundation of the 'reference-free' claim.
    4. GRM fitting best practices: Samejima's GRM, Bock-Aitkin EM, marginal MML with GH quadrature, model fit indices (Pearson χ², G², RMSEA). Recommend a specific estimator and convergence criterion to use in the experiment.
    5. Reasoning-domain choice: Survey syllogistic/propositional-logic benchmarks (e.g., LogicBench, PrOntoQA, FOLIO) and basic-arithmetic word problem benchmarks (GSM8K variants, MAWPS). Recommend which to mirror in the MIC generator.
    Output: research_out.json with {answer, sources, follow_up_questions} plus a research_report.md synthesizing the above into concrete recommendations for the experiment's design parameters.
  depends_on: []
expected_outcome: >-
  After this iteration: (1) a working M-IRT prototype that runs end-to-end (dynamic MIC generation → model panel evaluation
  → coherence scoring → GRM fitting) with all code and outputs in the experiment_out artifact; (2) a contamination-simulation
  result showing the headline claim — static accuracy ↑, M-IRT θ ↓ — under simulated memorization; (3) a methodology-grounding
  research report that positions M-IRT against ATLAS, Lost-in-Benchmarks, and the GRM-for-judges line of work and supplies
  citations for the paper. Together these give the second-iteration strategy a concrete foundation to scale: add more domains
  (multi-step math, causal reasoning), expand the model panel, run sensitivity analyses on the contamination simulation, and
  run the full correlation against the actual HELM leaderboard rather than just MMLU aggregate accuracy.
summary: >-
  Iteration 1 of M-IRT: build the end-to-end pipeline (dynamic Metamorphic Item Clusters → coherence scoring → Graded Response
  Model) on a 5-model × ~250-cluster panel, then deliver the two load-bearing validations — Pearson r > 0.85 against clean
  published static accuracy, and a contamination simulation showing static accuracy rises while M-IRT θ falls when a model
  memorizes the answer key. A parallel research artifact grounds the GRM fitting choices and contamination methodology against
  HELM-era prior work.
</previous_strategies>

<dependency_rules>
- depends_on is a list of objects {id, label} — each entry references an existing artifact and tags how it is being used
- "id" can ONLY reference IDs from <existing_artifacts> — never IDs you are proposing (all new artifacts run in parallel)
- "label" is a SHORT free-text type label (a word or two, NOT a sentence) describing what role the dep plays — e.g. "dataset", "validates", "extends", "supersedes". Required on every dep.
- Setting depends_on provides the dependency's out_dependency_files to your artifact at execution time
- If no suitable existing artifacts exist, use empty depends_on
- New artifact IDs are assigned by the system after submission — do not invent IDs for your proposed artifacts
</dependency_rules>

<available_artifact_types>
Artifact types you can plan. Use this to choose the right types for your strategy objectives.

<artifact_types>
RESEARCH
Web research to answer key questions — like a researcher making decisions.
Runtime: LLM Agent, no code execution.
Tools: the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text).
Capabilities: Find, synthesize, and compare information across sources; survey SOTA and best practices.
Deps: REQUIRED none | OPTIONAL other RESEARCH to build on prior findings

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance

DATASET
Collect, prepare, and merge datasets for experiments and analysis.
Runtime: Python 3.12, UV, isolated workspace.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-hf-datasets (HuggingFace Hub — ML datasets, many UCI/OpenML/Kaggle mirrors), aii-owid-datasets (Our World in Data — global statistics), aii-json (schema validation). Also any Python source (sklearn.datasets, openml, direct URLs, APIs) — must verify within 300MB limit.
Capabilities: Search, acquire, transform, combine, and standardize data from any available source.
Deps: REQUIRED none | OPTIONAL RESEARCH for guidance on what data to collect

EVALUATION
Evaluate experiment results with metrics, statistical analysis, and validity checks.
Runtime: Python 3.12, UV (any evaluation library), isolated workspace, gradual scaling matching experiment.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Compute any quantitative metrics and statistical tests, analyze validity and robustness.
Deps: REQUIRED at least one EXPERIMENT | OPTIONAL DATASET if reference data needed

PROOF
Formally prove mathematical statements in Lean 4 with automated iteration.
Runtime: LLM agent with Lean 4 compiler feedback loop.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-lean (proof verification, Mathlib search, tactics: ring, linarith, nlinarith, omega, simp, etc.)
Capabilities: Formally verify properties and inequalities, iterative proof development, lemma decomposition.
Deps: REQUIRED none | OPTIONAL RESEARCH for mathematical background
</artifact_types>
</available_artifact_types>

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

RESEARCH executor scope:
  Output: research_out.json with {answer, sources, follow_up_questions} + research_report.md
  DOES: Web research — search, read, synthesize information from papers/docs/APIs into a structured report
  DOES NOT: Run code, download files, execute scripts, compute anything — no shell/Python access
  Use for literature surveys, API documentation, technical specifications — pure information gathering

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results

DATASET executor scope:
  Output: data_out.json with rows of {input, output, metadata_fold, ...} — raw data only, no derived computations
  DOES: Download/generate datasets, analyze candidates to pick the best ones, standardize to JSON schema (features, labels, folds, metadata), validate schema, split into full/mini/preview
  DOES NOT: Run experiments, train models, compute derived statistics (PID/MI/correlations/synergy matrices) as final output
  If you need to COMPUTE something from data (synergy matrices, MI scores, timing benchmarks), use an EXPERIMENT artifact instead

EVALUATION executor scope:
  Output: eval_out.json with evaluation results
  DOES: Any evaluation of experiment results — metrics, statistical tests, ablations, comparisons, visualizations, robustness checks, error analysis, etc.
  DOES NOT: Implement new methods (use EXPERIMENT), collect data (use DATASET)
  This is for analyzing experiment outputs from any angle

PROOF executor scope:
  Output: Lean 4 proof files (.lean) with verified theorems
  DOES: Write and verify Lean 4 formal proofs with Mathlib, iterative compilation
  DOES NOT: Run Python experiments, collect data, do empirical analysis
  Use only when formal mathematical guarantees are needed
</artifact_executor_scope>

<artifact_planning_rules>
RESEARCH: Plan early — findings guide dataset selection, experiment design, and methodology.
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
DATASET:
- Plan for REAL third-party datasets (HuggingFace, Kaggle, direct-download URLs) — downloadable within time and size constraints
- Describe dataset criteria (domain, size, format) — executors find exact sources, but you can suggest candidates or search directions
- ALWAYS prefer real datasets over synthetic. Synthetic is a LAST RESORT only when no suitable real data exists
EVALUATION: Must depend on at least one EXPERIMENT. Focus on statistical rigor and validity checks.
PROOF: Use only when the hypothesis requires formal mathematical guarantees. Lean 4 + Mathlib.
</artifact_planning_rules>

<existing_artifacts>
--- Item 1 ---
id: art_Tf8iazoIvX4l
type: experiment
title: 'M-IRT: metamorphic item-response-theory LLM evaluation'
summary: >-
  This artifact implements the full Metamorphic Item Response Theory (M-IRT) pipeline that the artifact plan specifies. Stage
  1 deterministically generates 100 Metamorphic Item Clusters (50 propositional syllogisms + 50 arithmetic word problems)
  using 12 syllogistic templates and 12 arithmetic templates, each cluster containing 4 variants (seed, paraphrase, negation,
  contrapositive/inverse) with relational invariants baked in. Stage 2 queries five public LLMs via OpenRouter (gpt-4o-mini,
  claude-haiku-4.5, llama-3.1-8b-instruct, qwen-2.5-7b-instruct, mistral-small-24b-instruct) with concurrency=10 and a per-model
  retry layer, completing all 2,000 calls (100 clusters x 5 models x 4 variants) for a cumulative spend of $0.0476 USD in
  167 seconds. Stage 3 scores each (model, cluster) cell with an ordinal coherence metric in {0,1,2} derived from how many
  of the four metamorphic variants the model answered correctly. Stage 4 fits a Graded Response Model (girth.grm_mml) to the
  (5, 100) score matrix and recovers a per-model latent ability theta and per-item discrimination/difficulty. Stage 5 (Validation
  A) computes Pearson r between theta and published MMLU/HELM accuracy across the five models with a 10,000-resample bootstrap
  CI: r_mmlu=0.975 (target r>0.85), r_helm=0.976. Stage 6 (Validation B) simulates answer-key memorization on qwen-2.5-7b-instruct
  by forcing 30% of seed responses to the oracle across 3 random seeds: static accuracy rises (+0.07) but theta decreases
  by -1.38 (mean across seeds) -- strong evidence that the metamorphic design is contamination-aware. Deliverables: artifacts/exp_gen_sol_out.json
  (schema-validated cluster generator output), artifacts/exp_eval_sol_out.json (schema-validated coherence scoring), artifacts/exp_sel_data_out.json
  (schema-validated static-accuracy baseline), artifacts/method_out.json (final M-IRT results + both validations), full_method_out.json
  / mini_method_out.json / preview_method_out.json (workspace-root schema-conformant views). All three schemas (exp_gen_sol_out,
  exp_eval_sol_out, exp_sel_data_out) validate against the repo's aii-json schema definitions. Method orchestrator (method.py)
  supports --stage {all,generate,query,score,fit,validate}, --n-clusters, --seed, --concurrency, --rpm, --budget, --dry-run,
  and --mini flags. The mini mode now writes to artifacts_mini/ instead of overwriting production artifacts, so smoke tests
  are safe. Failure handling includes token-bucket rate limiter for free-tier models, tenacity retries with 429-specific 30s
  backoff, spend ledger hard stops, and a Tier-3 fallback scope reduction documented in scope_limitations. pyproject.toml
  pins every dependency to its installed version for full reproducibility.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json

--- Item 2 ---
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
</existing_artifacts>

<current_paper>
The current paper draft — represents the research story so far.

Use this to understand what's working, what's not, and what gaps remain.
Gaps and weak results signal what to try differently — not what to conclude.

# M-IRT: Evaluating Large Language Models Without Ground Truth via Metamorphic Item Response Theory

## Abstract

Static benchmarks with frozen held-out answer keys are widely understood to be vulnerable to contamination as language models are trained on ever-larger web crawls. We ask a sharper question: can LLM capabilities be measured without an answer key at all? We introduce Metamorphic Item Response Theory (M-IRT), a reference-free evaluation framework that scores a model's internal logical coherence across dynamically generated Metamorphic Item Clusters (MICs), each containing a seed question, a semantic paraphrase, a negation, and a contrapositive (or arithmetic inverse). MICs are produced on the fly from deterministic templates; the only oracle is the relational invariant binding the four variants. An ordinal coherence grade per (model, cluster) cell feeds a Samejima Graded Response Model fit by marginal maximum likelihood, recovering a per-model latent ability θ and per-item discrimination/difficulty. Across five public LLMs and clusters spanning propositional syllogisms and grade-school arithmetic, the θ ranking correlates with published MMLU accuracy at r = 0.975 and with HELM at r = 0.976. A simulated answer-key memorization attack on Qwen 2.5 7B raises its seed-only static accuracy while θ *decreases*, evidence that M-IRT captures reasoning rather than memorization. The end-to-end pipeline is reproducible for under five cents in a few minutes. Code, prompts, and raw responses are released.

## 1 Introduction

Benchmarks orient AI. They specify what is worth measuring and, in doing so, shape what is worth improving [1]. For language models, this role has been carried by fixed, curated test sets: a frozen set of items with a frozen answer key, run against a frozen evaluation harness. HELM [1] argued that the field needed broader coverage and multi-metric measurement, not that the frozen-test-set axiom itself was at risk. Six years on, that axiom is breaking.

The proximate cause is contamination. As LLM training corpora have grown to include large fractions of the public web, fixed benchmark items and their gold labels have leaked into pre-training data. Sainz et al. [2] report that GPT-4 verbatim fills in 57% of multiple-choice options masked from MMLU; Balloccu et al. [3] document evaluation malpractice that effectively rewards memorization. The empirical result is a well-known artefact: a model that has seen the test set during pre-training scores near ceiling, while its behaviour on novel but isomorphic questions collapses [3, 4]. Dynamic benchmarks that refresh items from recent sources, such as LiveBench [4], are one mitigation, but they still rely on a trusted answer key and so remain reference-dependent.

This paper asks whether the answer key itself is dispensable. If we can construct a cluster of items whose correct answers are logically bound to one another, without specifying any absolute answer; then the only thing we need to measure is whether a model behaves consistently across that cluster. We call such a cluster a *Metamorphic Item Cluster (MIC)*, drawing the term from metamorphic testing [5], where a metamorphic relation specifies how an output should transform when an input is perturbed, rather than what the output should equal. The same idea, applied to logical reasoning, says: if you can answer *P* correctly, then you should answer *not P* by the flipped label, the paraphrase by the same label, and the contrapositive by the same label. Logical coherence across the cluster is a graded observable; we never have to know whether the cluster's seed answer is "True" or "False".

Logical coherence is not a measurement of accuracy, but it is a measurement of capability. A model that reasons will tend to maintain coherence; a model that memorizes a surface form will break coherence the moment a paraphrase, negation, or contrapositive is applied. Coherence therefore satisfies a property no static benchmark can offer: it is invariant to having seen the answer key. If a model has memorized the answer to "All A are B; all B are C. Therefore all A are C", it has not memorized the answer to "Are all A not C?", and it has not memorized the answer to the paraphrase using a different vocabulary.

We turn coherence into a latent ability estimate by combining MICs with a Graded Response Model (GRM) [6]. The GRM is the canonical polytomous extension of item response theory, used in educational testing to score essay responses on ordered rubrics and recently applied to judge reliability for LLMs [7]. Our application differs: the response variable is not a Likert rating or a correctness call, but the count of MIC variants a model answered coherently. Mapping this count to a 3-point ordinal scale (0/1/2) yields the response matrix that the GRM fits. From a fitted GRM we extract a per-model latent ability θ and per-item discrimination and difficulty parameters, in the standard IRT fashion [8, 9, 10].

Concretely, we generate 100 MICs (50 propositional syllogisms across 12 templates; 50 arithmetic word problems across 12 templates) and query five public LLMs on each of the four variants, for 2,000 calls completed in 167 seconds at $0.05 cumulative spend. The resulting θ values rank the models in close agreement with their published MMLU (r = 0.975) and HELM (r = 0.976) accuracy, despite never consulting those benchmarks during evaluation. A targeted contamination simulation then forces Qwen 2.5 7B's seed responses to the oracle on 30% of clusters. Static seed accuracy rises by +0.07 while θ drops by −1.20, evidence that M-IRT's θ is not a memorization proxy.

**Summary of contributions.**
- (i) A reference-free evaluation framework (M-IRT) that produces MICs dynamically and fits a Samejima GRM on ordinal coherence scores, requiring no ground-truth answer key.
- (ii) A reproducible pipeline of 100 MICs across two reasoning domains and a panel of five public models, completed end-to-end for under $0.05 and ~3 minutes.
- (iii) Empirical validation that the recovered latent ability θ correlates with MMLU (r = 0.975) and HELM (r = 0.976), and that θ *decreases* under simulated answer-key memorization while the static seed accuracy *increases*.

[FIGURE:fig1]

## 2 Related Work

**Holistic and multi-metric evaluation.** HELM [1] is the reference point for multi-metric LLM evaluation: a top-down taxonomy of scenarios and metrics applied to many models under standardized conditions. M-IRT inherits HELM's emphasis on standardized conditions and full-result transparency, but relaxes the assumption that the same items must be used for every model. Each model sees a freshly generated MIC, which removes the contamination vector that HELM's frozen scenarios cannot eliminate.

**Item response theory for LLM benchmarks.** Three recent works apply IRT to LLM evaluation. tinyBenchmarks [8] shows that 100 carefully chosen MMLU examples can reproduce full-benchmark accuracy within 1.9% MAE using a generalized performance-IRT estimator. Lost in Benchmarks [9] introduces PSN-IRT, a pseudo-siamese network for 4PL neural calibration trained end-to-end on 11 benchmarks (41,871 items) and reports stronger alignment with human preference than raw items. ATLAS [10] applies computerized adaptive testing to a calibrated bank of 3,000+ LLMs across five benchmarks, achieving MAE 0.157 on HellaSwag with 41 items. All three operate on *static* items with *known correct answers* and are therefore reference-dependent. M-IRT shares the GRM machinery but replaces the correctness response with a coherence response, sidestepping both the calibration bank and the answer key.

**LLM-as-judge reliability.** Choi et al. [7] fit a Samejima GRM to LLM-judge reliability ratings, proposing Bayesian priors and convergence criteria that M-IRT adopts. The application is different: the *judge* is the unit of measurement in [7], while in M-IRT the *evaluated model* is the unit of measurement and the response variable is its own internal coherence.

**Contamination detection.** Sainz et al. [2] introduce TS-Guessing, which masks a multiple-choice option and checks verbatim fill-in. Xu et al. [11] survey four-level contamination taxonomy (semantic/information/data/label) and matching-based versus comparison-based detection. These works *detect* contamination after the fact; M-IRT is *immune* to label-level contamination because no label exists.

**Contamination-limited dynamic benchmarks.** LiveBench [4] refreshes items monthly from competitions, arXiv, and news. M-IRT is complementary: LiveBench's items still need an answer key, whereas MICs do not. The two can be combined into a dynamic benchmark whose scoring is by logical coherence rather than answer match.

**Metamorphic testing for LLMs.** Chen et al. [5] define metamorphic relations (MRs) as input-output relations used to verify programs in lieu of oracles. LLMORPH [12] catalogues 191 NLP MRs across 24 tasks and runs 561,267 test executions, flagging MRs 9, 142, 154 as high-failure-low-false-positive. LGMT [13] derives 20 first-order-logic-grounded MRs (De Morgan, contraposition, quantifier shifts) and shows models are most sensitive to symbol- and conclusion-level variation. M-IRT adopts LGMT's logical perturbation set and uses a smaller but sufficient subset (paraphrase, negation, contrapositive) within each cluster.

**Polytomous IRT in education.** Samejima's original GRM [6] estimates ordered-category responses with per-category thresholds. Liu et al. [14] apply IRT to LLM-respondent item evaluation in an educational assessment setting. M-IRT imports the response model but treats the model being evaluated as the *person*, not the *respondent*.

## 3 Preliminaries

**Notation.** For a panel of *M* LLMs and a set of *I* Metamorphic Item Clusters, each cluster contains four variants indexed by role *r* ∈ {seed, paraphrase, negation, contrapositive}. The cluster *i* has oracle answers $\mathbf{a}_i = (a_{i,1}, \ldots, a_{i,4})$ that satisfy relational invariants (for example, the negation variant's oracle is the Boolean complement of the seed's oracle).

**Graded Response Model.** Following Samejima [6], the probability that a model with latent ability θ produces a response of category $k \in \{0, 1, \ldots, K-1\}$ on item *i* is
$$P(Y_i \geq k \mid \theta) = \frac{1}{1 + \exp(-\alpha_i(\theta - \beta_{i,k}))},$$
where $\alpha_i > 0$ is the discrimination of item *i*, and $\beta_{i,1} < \beta_{i,2} < \ldots$ are the ordered category boundaries. The category probability is $P(Y_i = k \mid \theta) = P(Y_i \geq k \mid \theta) - P(Y_i \geq k+1 \mid \theta)$. Parameters are fit by marginal maximum likelihood using Gauss-Hermite quadrature on θ.

**Coherence response.** For a (model, cluster) pair, let $c_{mi}$ denote the count of the four variants on which the model's response matches the oracle (correctness, not the relational invariant alone). We map $c_{mi}$ to an ordinal response
$$Y_{mi} = \begin{cases} 0 & c_{mi} \in \{0, 1\} \\ 1 & c_{mi} = 2 \\ 2 & c_{mi} \in \{3, 4\}. \end{cases}$$

The mapping is monotone: more coherent models receive higher grades. The 3-category structure is the smallest that distinguishes "near-random" ($Y = 0$) from "partially coherent" ($Y = 1$) from "highly coherent" ($Y = 2$).

**Metamorphic relation.** A *metamorphic relation* [5] for a reasoning task is a deterministic relation $R(\text{input}_1, \text{input}_2) \Rightarrow R'(\text{output}_1, \text{output}_2)$ that holds for any correct solver. For syllogisms, the relation "input 2 is the negation of input 1" implies the relation "output 2 is the Boolean complement of output 1". For arithmetic, the relation "input 2 is the same word problem with quantities negated" implies the relation "output 2 is the negation of the numeric output (i.e., 'NO')". M-IRT uses these relations to score the negation and contrapositive variants without ever needing an absolute label.

## 4 Method: M-IRT

The M-IRT pipeline has four stages: MIC generation, model querying, coherence scoring, and GRM fitting with validation. Figure 1 diagrams the end-to-end flow.

### 4.1 Metamorphic Item Cluster Generator

The generator is deterministic given a seed. It draws on two domain generators and produces four-variant clusters [ARTIFACT:art_Tf8iazoIvX4l].

**Logic generator.** Twelve syllogistic templates $T_1, \ldots, T_{12}$ express the canonical valid and invalid forms, inspired by the controlled-ontology construction of PrOntoQA [16] and the negation-sensitive template design of LogicBench [19]. Each template takes noun slots *A*, *B*, *C* drawn from disjoint noun pools for the seed and the paraphrase, ensuring that paraphrase and seed never share vocabulary. A template returns a two-premise argument, a candidate conclusion, and an oracle label V (valid) or I (invalid). The four variants are:
- *Seed:* the original syllogism with original nouns.
- *Paraphrase:* the same argument with nouns from the paraphrase pool.
- *Negation:* the conclusion negated; oracle is the Boolean complement of the seed label.
- *Contradiction:* the negation of one premise; oracle flips if and only if the syllogism is *Barbara*-style (T4, T10, T12); otherwise it stays.

**Arithmetic generator.** Twelve templates express one- and two-step word problems with named participants, named items, and integer quantities in $[2, 99]$, following the GSM8K [17] and MAWPS [18] constructions but reducing them to two-step problems with derivable oracles. Paraphrase substitutes items from a disjoint pool and may rename participants. Negation asks "Is it NOT the case that the answer is *x*?", with oracle "NO". The contrapositive slot is filled by an *inverse*: a problem with the additive inverse of one quantity, whose answer is $-(a-b)$ for difference problems and $-a - b$ for sum problems; the oracle is the negated numeric value.

The two generators together emit 50 logic clusters and 50 arithmetic clusters, for 100 clusters per evaluation session. Each cluster carries an oracle answer, a difficulty hint (medium/hard), and a relational-invariant table that the scorer uses to evaluate the negation and contrapositive variants.

### 4.2 Model Querying

We evaluate five public LLMs via the OpenRouter API: GPT-4o-mini, Claude Haiku 4.5, Llama 3.1 8B Instruct, Qwen 2.5 7B Instruct, and Mistral Small 24B Instruct 2501. Each model is presented with each of the 400 variant questions (100 clusters × 4 variants) in a single, zero-shot prompt: "Answer with V or I." for logic, or with the integer answer for arithmetic. We run with concurrency 10 and a global 12 rpm cap, completing all 2,000 calls in 167 seconds at $0.048 cumulative spend. No model is fine-tuned or prompted with worked examples; the prompt template is identical across models [ARTIFACT:art_Tf8iazoIvX4l].

The generator is called fresh per evaluation session, so the MICs a model sees are unique to that session and not in any prior training corpus. A second model querying the same cluster set would receive the same variant questions, but with different clusters generated for a different session seed the contamination vector remains closed.

### 4.3 Ordinal Coherence Scoring

For each (model, cluster) pair, we parse each variant's response into the canonical response space ({V, I} for logic, integer or {YES, NO} for arithmetic) and compare to the role-appropriate oracle. The negation variant's oracle is *not* the seed's oracle; it is the seed's oracle flipped (for logic) or "NO" (for arithmetic). The contrapositive variant's oracle is similarly derived from the relational invariant. A correct response on all four variants yields a raw count of 4; we map it to the ordinal scale $Y_{mi} \in \{0, 1, 2\}$ as in Section 3.

The scoring rules are deterministic and parser-level: they do not depend on a separate language model, judge, or human rater.

### 4.4 GRM Fitting

We fit the GRM via `girth.grm_mml`, an open-source marginal-maximum-likelihood implementation in Python. The input is the (M × I) integer response matrix; the output is a vector of M latent abilities $\theta_j$, a vector of I discriminations $\alpha_i$, and an (I × (K − 1)) matrix of difficulty thresholds $\beta_{i,k}$. We use K = 3 categories. No priors are imposed on θ beyond the standard normal default of `girth`; discrimination and difficulty are estimated freely. The fit takes roughly three seconds on the (5 × 100) matrix.

### 4.5 Validation A: Correlation with External Benchmarks

To verify that θ captures reasoning rather than a proxy unrelated to capability, we correlate θ with each model's published MMLU accuracy and HELM accuracy [ARTIFACT:art_Tf8iazoIvX4l]. We compute Pearson r and a 10,000-resample bootstrap 95% confidence interval.

### 4.6 Validation B: Contamination Resistance

We simulate answer-key memorization on Qwen 2.5 7B by forcing its seed response to the oracle on a randomly chosen 30% of clusters (seeds 0, 1, 42). The paraphrase, negation, and contrapositive responses are unchanged. We recompute static seed accuracy and re-fit the GRM on the modified matrix. Under contamination, we expect:
- Static seed-only accuracy to *increase* (the model now "knows" the seed answers).
- The GRM-fitted θ to *decrease or remain stable* (the model still fails on paraphrase/negation/contrapositive, so its coherence grade does not rise).

This pattern, if observed, demonstrates that M-IRT θ is not a memorization proxy.

## 5 Experiments

### 5.1 Setup

The pipeline runs in five sequential stages: cluster generation, model querying, coherence scoring, GRM fitting, and validation (the validation stage runs two sub-experiments: a correlation check against published benchmarks and a contamination simulation). Hardware: a CPU-only container with 6 GB RAM and a 4-hour CPU cap; total runtime 211 seconds. The five models are queried via the OpenRouter chat-completion interface with no system prompt, temperature 0, and a 4-token output budget. Responses are stored as one record per (model, variant) call; the fitted GRM and validation statistics are released alongside the code [ARTIFACT:art_Tf8iazoIvX4l].

### 5.2 Latent Ability Ranking

Table 1 reports θ and published MMLU/HELM accuracy for each model, sorted by θ.

**Table 1. GRM-estimated θ versus published MMLU and HELM accuracy.**

| Model | θ | MMLU | HELM |
|---|---:|---:|---:|
| openai/gpt-4o-mini | +3.69 | 0.82 | 0.79 |
| anthropic/claude-haiku-4.5 | +3.56 | 0.80 | 0.78 |
| mistralai/mistral-small-24b | −0.28 | 0.73 | 0.71 |
| qwen/qwen-2.5-7b | +0.07 | 0.71 | 0.69 |
| meta-llama/llama-3.1-8b | −1.37 | 0.68 | 0.65 |

The θ ranking reproduces the MMLU ranking exactly in the top two (GPT-4o-mini and Claude Haiku 4.5), and it puts Llama 3.1 8B at the bottom, matching its MMLU floor of 0.68. The Pearson correlation between θ and MMLU is **r = 0.975** (95% bootstrap CI [0.59, 1.00]); between θ and HELM, **r = 0.976** (CI [0.80, 1.00]). The wide CI reflects the small sample size (n = 5 models); the point estimate is consistent with the hypothesis criterion r > 0.85 [ARTIFACT:art_Tf8iazoIvX4l].

[FIGURE:fig2]

### 5.3 Per-Model Coherence Distribution

Across 100 clusters, the ordinal response distributions show the expected separation [ARTIFACT:art_Tf8iazoIvX4l]:

| Model | Y = 0 | Y = 1 | Y = 2 | mean raw correct (of 4) |
|---|---:|---:|---:|---:|
| claude-haiku-4.5 | 5 | 21 | 74 | 3.21 |
| gpt-4o-mini | 5 | 20 | 75 | 3.11 |
| mistral-small-24b | 7 | 19 | 74 | 2.94 |
| qwen-2.5-7b | 16 | 17 | 67 | 2.78 |
| llama-3.1-8b | 20 | 26 | 54 | 2.32 |

The top two models (GPT-4o-mini, Claude Haiku 4.5) achieve the top grade on 74 to 75% of clusters and the bottom grade on only 5%, so the "near-random" tail is small. The bottom model (Llama 3.1 8B) still achieves top grade on 54% of clusters, indicating that even weak models solve roughly half of all clusters coherently. The gap that the GRM exploits is the bottom-grade fraction: 5% vs 20%.

[FIGURE:fig3]

### 5.4 Item Discrimination and Difficulty

The fitted discriminations $\alpha_i$ span from a floor of approximately 0.20 (the lower-bound clamp on items the GRM could not distinguish) up to 5.0 for the most discriminative items (e.g., arith_0001, arith_0046, logic_0009, logic_0013, logic_0027). Difficulty thresholds $\beta_{i,k}$ for the most discriminative items lie at moderate θ values around −0.9, suggesting that these items discriminate primarily among the mid-ability models. Items at the discrimination floor carry no signal for θ estimation and do not distort it; we retain them for completeness rather than discard, since dropping items would change the response matrix the GRM sees.

### 5.5 Domain Decomposition

Per-domain coherence for the top model (GPT-4o-mini) reveals that arithmetic clusters are easier than logic clusters across all models: arithmetic mean raw correct 3.56, logic mean raw correct 2.66. This matches the difficulty gradient we would expect from a grade-school word-problem corpus (arithmetic) versus a categorical syllogism corpus (logic). The arithmetic-vs-logic gap is consistent across models and contributes to the strong MMLU/HELM correlation: published benchmark accuracy reflects a similar mix of formal-reasoning and arithmetic-reasoning items.

### 5.6 Contamination Resistance

The contamination simulation on Qwen 2.5 7B across three random seeds (0, 1, 42) produces [ARTIFACT:art_Tf8iazoIvX4l]:

| Seed | Clean static acc | Contam static acc | Δ static | Clean θ | Contam θ | Δ θ |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 0.77 | 0.83 | +0.06 | −0.36 | −1.57 | −1.21 |
| 1 | 0.77 | 0.86 | +0.09 | −0.36 | −1.52 | −1.16 |
| 42 | 0.77 | 0.84 | +0.07 | −0.36 | −1.57 | −1.21 |
| **mean** | 0.77 | 0.84 | **+0.07** | −0.36 | −1.55 | **−1.20** |

Static seed accuracy rises by +0.07 on average (a contamination signal), but the GRM-estimated θ *falls* by an average of −1.20. This is the desired behaviour: contaminating the seed answer does not transfer to the metamorphic variants, so the model's coherence grade on the contaminated clusters does not rise. The GRM, which is fit on the full coherence matrix, registers the contamination as a *decrease* in θ because the model's coherence profile has become inconsistent (the seed now disagrees with the model's actual reasoning, which the metamorphic variants reveal).

[FIGURE:fig4]

The standard deviation of Δθ across the three seeds is 0.02, indicating that the contamination signal is stable across random choices of contaminated clusters. This stability is the contamination-resistance criterion specified in our hypothesis: θ either decreases or remains stable under memorization of a subset of seed answers, and the magnitude of the drop is several orders larger than its noise.

## 6 Discussion

**What worked.** M-IRT recovers a θ ranking that matches MMLU and HELM with Pearson r > 0.97, despite never inspecting the model's responses against a fixed answer key. The contamination simulation shows that θ is not a memorization proxy. The pipeline runs on commodity CPU hardware for $0.05 and three minutes per session, which is comparable to a single LLM API call's latency and orders of magnitude cheaper than full-benchmark evaluation [1, 8].

**What did not work as hoped.** The point estimate r = 0.975 is supported by a wide bootstrap CI [0.59, 1.00] because the panel contains only 5 models; the upper bound is a ceiling artefact of the bootstrap with n = 5, not an honest interval. Adding 5 to 10 more models would tighten the CI materially. The Samejima GRM fit on a 5-person response matrix has only 5 degrees of freedom for θ estimation, so small per-item perturbations can produce visible θ shifts on the order of ±0.5; we mitigate by reporting contamination Δθ (a within-model comparison) rather than absolute θ. Finally, the contamination experiment requires re-fitting the GRM on the contaminated matrix, and the local optimum of that second fit can drift from the first by a small amount, so absolute θ values from a single run should not be over-interpreted. The scientific claim (Δθ < 0 under contamination) is robust; a practitioner using M-IRT should report θ deltas under interventions rather than absolute θ.

**Limitations.**
- *Two domains.* M-IRT currently covers propositional syllogisms and grade-school arithmetic. Real reasoning also includes analogical, causal, multi-hop, and counterfactual reasoning. Extending M-IRT to those domains is a matter of authoring additional metamorphic templates with relational invariants; the GRM, scoring, and pipeline remain unchanged.
- *Twelve templates per domain.* Twelve logic templates and twelve arithmetic templates cover the classical syllogistic forms and the most common word-problem operations, but they are not exhaustive. A larger generator bank would yield finer per-item discrimination estimates.
- *Five-model panel.* The contamination-resistance result is a within-model comparison (Δθ for one model under one intervention), so it is robust to small panels. The external-correlation result (r vs MMLU/HELM) requires a larger panel to narrow the bootstrap CI.
- *Contamination simulation as upper bound.* The 30% seed-answer override is a worst-case memorization scenario. Real contamination is partial and stochastic; M-IRT's resistance in those settings should hold qualitatively but has not been measured against natural contamination patterns.
- *Polytomous response scale.* The 0/1/2 mapping compresses 5 raw counts (0 to 4) into 3 categories. Alternative polytomous structures (K = 4 or K = 5 with separate thresholds) would let the GRM exploit more granularity at the cost of greater estimation variance in a 5-person sample.

**Future work.**
- *Multi-domain M-IRT.* Add clusters for analogical reasoning (LGMT-style quantifier shifts [13]), first-order logic (FOLIO-style annotations [15]), and reading comprehension with paraphrase-negation pairs.
- *Bayesian GRT with informative priors.* Replace MML with Hamiltonian Monte Carlo and add Samejima's recommended priors (θ ~ N(0, 1), α ~ LogNormal(0, 0.5), β_k ~ N(0, 1) with ordering) [7], which would let M-IRT handle panels of 2 to 3 models without degenerate fits.
- *Adaptive MIC selection.* Once the GRM is calibrated on a panel, choose the next MIC from a candidate pool using maximum Fisher information on θ, in the spirit of computerized adaptive testing [10].
- *Online contamination monitoring.* Deploy M-IRT as a recurring audit: re-run a small MIC set weekly, and alert if a model's θ moves relative to its previous θ by more than a threshold. This would catch gradual contamination that static benchmarks miss.

## 7 Conclusion

The frozen held-out test set is no longer the only foundation for LLM evaluation. M-IRT shows that a dynamically generated, reference-free benchmark, built from clusters of logically related items whose relational invariants are known without absolute labels, can produce a latent ability estimate that correlates with MMLU at r = 0.975 and that decreases under simulated answer-key memorization while static accuracy rises. The result inverts the conventional dependency between evaluation and ground truth: we measure reasoning by measuring whether a model reasons the same way twice on the same logical form, not by measuring whether it produces a memorized string.

We release code, prompts, raw responses, and fitted parameters under an MIT license [ARTIFACT:art_Tf8iazoIvX4l]. The MIC generator is deterministic given a seed and reproducible to the character. We hope the framework serves as a starting point for contamination-aware evaluation at a time when the field is rethinking what benchmarks can be relied on to measure.

## References

[1] P. Liang et al., "Holistic Evaluation of Language Models," *Transactions on Machine Learning Research*, 2022.

[2] C. Deng et al., "Investigating Data Contamination in Modern Benchmarks for Large Language Models," *NAACL*, 2024.

[3] S. Balloccu, P. Schmidtová, M. Lango, and O. Dusek, "Leak, Cheat, Repeat: Data Contamination and Evaluation Malpractices in Closed-Source LLMs," *EACL*, 2024.

[4] C. White et al., "LiveBench: A Challenging, Contamination-Limited LLM Benchmark," *ICLR*, 2025.

[5] T. Chen, F.-C. Kuo, H. Liu, P.-L. Poon, D. Towey, T. Tse, and Z. Zhou, "Metamorphic Testing: A Review of Challenges and Opportunities," *ACM Computing Surveys*, vol. 51, no. 1, 2018.

[6] F. Samejima, "Estimation of Latent Ability Using a Response Pattern of Graded Scores," *Psychometrika*, vol. 34, no. S1, pp. 1-97, 1969.

[7] J. Choi, S. Park, C. Cho, H. Park, and B. Kim, "Diagnosing the Reliability of LLM-as-a-Judge via Item Response Theory," arXiv:2602.00521, 2026.

[8] F. M. Polo, L. Weber, L. Choshen, Y. Sun, G. Xu, and M. Yurochkin, "tinyBenchmarks: Evaluating LLMs with Fewer Examples," *ICML*, 2024.

[9] H. Zhou et al., "Lost in Benchmarks? Rethinking Large Language Model Benchmarking with Item Response Theory," *AAAI*, 2026.

[10] P. Li, X. Tang, S. Chen, Y. Cheng, R. Metoyer, T. Hua, and N. V. Chawla, "Adaptive Testing for LLM Evaluation: A Psychometric Alternative to Static Benchmarks," arXiv:2511.04689, 2025.

[11] C. Xu, S. Guan, D. Greene, and M.-T. Kechadi, "Benchmark Data Contamination of Large Language Models: A Survey," arXiv:2406.04244, 2024.

[12] S. Cho, S. Ruberto, and V. Terragni, "Metamorphic Testing of Large Language Models for Natural Language Processing," *ICSME*, 2025.

[13] Z. Zhou et al., "LGMT: Logic-Grounded Metamorphic Testing for Evaluating the Reasoning Reliability of LLMs," *Knowledge-Based Systems*, 2026.

[14] Y. Liu, S. Bhandari, and Z. Pardos, "Leveraging LLM-Respondents for Item Evaluation: A Psychometric Analysis," *British Journal of Educational Technology*, 2025.

[15] S. Han et al., "FOLIO: Natural Language Reasoning with First-Order Logic," *EMNLP*, 2022.

[16] A. Saparov and H. He, "Language Models Are Greedy Reasoners: A Systematic Formal Analysis of Chain-of-Thought," *ICLR*, 2023.

[17] K. Cobbe et al., "Training Verifiers to Solve Math Word Problems," arXiv:2110.14168, 2021.

[18] R. Koncel-Kedziorski, S. Roy, A. Amini, N. Kushman, and H. Hajishirzi, "MAWPS: A Math Word Problem Repository," *NAACL*, 2016.

[19] M. Parmar et al., "LogicBench: Towards Systematic Evaluation of Logical Reasoning Ability of Large Language Models," *ACL*, 2024.

</current_paper>

<reviewer_feedback>
Paper reviewer feedback from the previous iteration. Your strategy MUST address these critiques.
Prioritize major issues — these are the most impactful improvements to make.

- [MAJOR] (novelty) Direct prior art on paraphrase/negation consistency as a reference-free LLM evaluation is not cited. Liu et al. (2024, 'Aligning with Logic: Measuring, Evaluating and Improving Logical Preference Consistency in Large Language Models', arXiv:2410.02205) explicitly proposes negation invariance (and transitivity, commutativity) as reference-free properties, validates them across diverse LLMs, and demonstrates correlation with model quality — the exact claim M-IRT makes. Jang et al. (2022) introduced negational/symmetric/transitive consistency for LLMs. Novikova et al. (2025, arXiv:2505.00268) survey the consistency literature as a recognized field. ConsistencyGate (arXiv:2607.22962, 2026) already operationalizes self-consistency as a contamination gate. The paper cites LGMT (the closest direct precedent) but does not engage with Liu et al., Jang et al., or the consistency survey. Without distinguishing itself from this literature, the contribution reads as 'Liu et al. 2024 + GRM + dynamic generation'.
  Action: Add a 'Reference-free consistency as a research thread' paragraph to Section 2 that cites Jang et al. 2022, Liu et al. 2024, the Novikova et al. 2025 survey, and ConsistencyGate 2026. Make the contribution precise: (i) M-IRT uses polytomous GRM rather than binary invariance indicators; (ii) M-IRT dynamically generates clusters per session, whereas prior work uses fixed prompts; (iii) M-IRT targets contamination-resistance specifically, whereas prior work targets reliability/robustness. Then in Section 5 add an ablation comparing GRM θ to Liu-style paraphrase agreement rate and negation invariance rate on the same five models.
- [MAJOR] (evidence) The headline Pearson r = 0.975 with MMLU on a panel of n = 5 is statistically vacuous. The bootstrap CI is [0.59, 1.0] — i.e., the lower bound already allows r = 0.59, well below the r > 0.85 hypothesis criterion. The paper acknowledges this in Section 6 but the abstract and Section 5 still lead with r = 0.975 as if it were strong evidence. More importantly, the actual θ ranking inverts the MMLU ranking in the middle: Qwen (θ = +0.07, MMLU = 0.707) ranks above Mistral (θ = -0.28, MMLU = 0.732), i.e. the worse-by-MMLU model is rated better by θ. The Pearson r is being driven by GPT-4o-mini / Claude at the top and Llama at the bottom; the middle three models are essentially indistinguishable by θ. The paper does not report Spearman ρ or Kendall's τ, which are the relevant statistics for the rank claim.
  Action: (1) Expand the model panel to at least n = 15 across families (open-weights and closed; small and large). This costs < $1 and a few hours. (2) Report Spearman ρ and Kendall's τ alongside Pearson r; the rank-based statistics are what the claim actually needs. (3) Add a leave-one-out analysis showing how the correlation changes when each model is removed; this will reveal that the correlation is largely carried by 1-2 anchor models. (4) Re-position the headline as 'r in the same range as prior work on small panels' rather than as a definitive validation.
- [MAJOR] (methodology) The contamination-resistance experiment tests an unrealistic scenario. The simulation overwrites the target model's seed response in the data structure (with the oracle answer) but leaves the paraphrase/negation/inverse responses untouched. This means the simulated 'contaminated' model has correct seed + incoherent other variants. The θ drop of -1.38 is partly an artifact of injecting artificial inconsistency, not of memorization. A realistic contamination scenario is: a model that has seen the benchmark's seed answer during pretraining would (a) produce the correct seed AND (b) produce coherent paraphrase/negation/inverse responses (because they are paraphrases of the same content the model memorized). The current experiment does not test this. Furthermore, the experiment does not re-query the target model at all — it just modifies the response matrix.
  Action: Redesign the contamination experiment as 'natural contamination': inject the seed oracle into the model prompt (e.g. via a system prompt that contains the seed answer for 30% of clusters) and re-query the model. Check whether ALL FOUR variants become coherent on those clusters (memorization would yield high coherence on all four, defeating M-IRT) or whether θ remains low (memorization of seeds alone would not transfer to paraphrase/negation/inverse). This is the test that actually validates the claim.
- [MAJOR] (rigor) Paper text contradicts the actual code outputs. Table 1 lists the model order as GPT-4o-mini, Claude, Mistral, Qwen, Llama but the underlying θ values put Qwen (+0.07) above Mistral (-0.28). The contamination table reports mean Δθ = -1.20 but the actual code output is -1.38. The std of Δθ across seeds is reported as 0.02 but is 0.007. The clean static accuracy for Qwen is reported as 0.77 in the contamination table but is 0.78 in the data. These are not large numerical errors but they undermine trust in the entire quantitative chain: if Table 1 is wrong, what else is wrong?
  Action: Re-run the pipeline (it is reproducible for $0.05) and update every number in the paper from the actual JSON outputs. Fix the table ordering. Cite the JSON outputs in the artifact. A reviewer should be able to diff the paper numbers against method_out.json and find them identical.
- [MAJOR] (methodology) The arithmetic MIC generator contradicts the 'reference-free' claim. The negation variant's oracle requires the seed answer ('wrong = seed_answer + 1'); the inverse variant's oracle requires the first addend (which is only known if you compute the seed). The paper text in Section 4.1 acknowledges this implicitly by describing the negation as 'the negation asks Is it NOT the case that the answer is x' with oracle NO', but the code passes seed_answer in to compute wrong. This means the arithmetic MIC is not actually reference-free: the relational invariant table carries the oracle answer into the negation/inverse variants. For logic MICs the negation is genuinely derivable from the conclusion ('V iff the negation holds, iff original is invalid'), but for arithmetic it is not.
  Action: Redesign arithmetic negation so the oracle is derivable from the question alone, without computing the seed answer. For example: 'Is the answer greater than 100?' or 'Is the answer less than the first quantity?'. Both have oracles derivable from the question text. Likewise for the inverse variant, ask a question whose answer can be derived by re-doing the arithmetic differently (e.g. 'What is the difference between the two quantities?'). Alternatively, drop the 'reference-free' claim for arithmetic and keep it only for the logic domain.
- [MAJOR] (methodology) No ablation against simpler reference-free baselines. The paper claims M-IRT's θ is a 'latent ability' that captures reasoning, but does not compare against the obvious baselines: (i) raw paraphrase agreement rate per model (fraction of seed-paraphrase pairs both correct), (ii) raw negation invariance rate per model (fraction of seed-negation pairs with complementary answers), (iii) a paraphrase+negation composite. Liu et al. 2024 showed these simple consistency metrics already correlate with MMLU. The paper does not demonstrate that GRM adds anything over these simpler metrics. Without this ablation, the contribution reduces to 'we re-implemented Liu et al. 2024 with an IRT fit'.
  Action: Add a Table 2 with three baseline columns: (i) paraphrase agreement rate, (ii) negation invariance rate, (iii) a paraphrase+negation composite (mean of i and ii), plus the GRM θ. Report Pearson r and Spearman ρ with MMLU/HELM for each. If the GRM θ is meaningfully better, that justifies the framework; if not, the paper should either drop the GRM framing or argue that it is more interpretable / better suited to adaptive testing (Section 6's 'future work' direction).
- [MAJOR] (scope) The MIC bank covers only two domains (propositional syllogisms, grade-school arithmetic). The paper claims θ correlates with MMLU and HELM, but MMLU covers history, law, medicine, biology, philosophy, etc. — domains the MIC bank does not probe. The strong correlation reported (r = 0.975) is partly because the top two models are clearly separated and the bottom model is clearly separated, with the middle three essentially noise. The paper does not test whether the θ ranking reproduces MMLU ordering across domains the MIC bank does not cover — because it cannot, by construction.
  Action: (1) Add 2-3 additional domain generators (analogy: A:B::C:? style; multi-hop reading: paragraph + question chain; code tracing: small program + output prediction) following the LGMT / PrOntoQA / FOLIO precedents cited. (2) Reframe the MMLU/HELM correlation as 'θ ranks the syllogistic+arithmetic component of reasoning capability, which is highly correlated with general capability', rather than as a validation of θ against benchmarks that probe other domains. (3) Acknowledge the scope limitation explicitly in the abstract.
- [MAJOR] (evidence) Five models is too few to support any claim of correlation with a published benchmark. The Pearson r = 0.975 has CI [0.59, 1.0] because n = 5 gives at most C(5,2) = 10 distinct pairs of points and the bootstrap with replacement produces a near-degenerate CI. Even if r were 0.99 on n = 5, the CI would still touch values that would not pass the r > 0.85 hypothesis criterion. The paper itself admits this in Section 6 ('Adding 5 to 10 more models would tighten the CI materially') but the headline abstract claim is still r = 0.975. For NeurIPS D&B or ICLR main track, n = 5 would not pass the bar.
  Action: Expand the model panel to at least n = 15. The cost is roughly $0.20 - $0.50 in API spend and a few hours of compute. Models to add: at least one from each of GPT-4.1, Claude Sonnet 4, Gemini 2.5 Flash, Llama 3.3 70B, Mistral Large 2, DeepSeek V3, Qwen 2.5 72B, plus smaller open-weight models (Llama 3.2 1B, Phi-3 mini, Gemma 2 2B). The added span will give a Spearman ρ with MMLU/HELM that has a meaningful CI and supports the rank claim.
- [MINOR] (rigor) The 0/1/2 ordinal mapping (raw count 0/1 -> grade 0; raw count 2 -> grade 1; raw count 3/4 -> grade 2) is presented without justification. Why compress 5 raw counts into 3 categories? Why this particular threshold (2 -> grade 1)? The paper claims K = 3 'is the smallest that distinguishes near-random from partially coherent from highly coherent', but the thresholds (raw >= 3 -> 2; raw == 2 -> 1; raw < 2 -> 0) are arbitrary. With only 5 models, a K = 5 fit would have 5 degrees of freedom per item and a K = 3 fit has 2; the paper does not compare these.
  Action: Either (a) refit with K = 5 and show the resulting θ correlates at least as well with MMLU/HELM, or (b) justify the K = 3 mapping explicitly (the 2-category bin captures 'coherent on at least 3 of 4 variants' which is the smallest signal that the model is reasoning rather than guessing). Compare AIC/BIC across K = 2, 3, 4, 5.
- [MINOR] (clarity) Figure specifications are well-written but no figures exist in the artifact. Figure 1 should diagram the M-IRT pipeline; Figure 2 should show θ vs MMLU/HELM scatter; Figure 3 should show per-model coherence distributions; Figure 4 should show contamination Δθ bar plot. Without the actual images, the visual claims in the text are unverifiable. The paper claims the figures 'show exactly what the caption describes' but the data behind each figure is in the JSON outputs and should be verifiable from there.
  Action: Generate the figures from the JSON outputs and include them as PDFs/PNGs in the artifact. The data is in full_method_out.json; the figures are reproducible from that file with matplotlib. Add the figure files to the artifact directory.
- [MINOR] (clarity) The static-accuracy baseline is confusing. Section 5.6's contamination table reports 'Clean static acc' for Qwen as 0.77, but the per-model static accuracy baseline in the artifact metadata is 0.78. The paper also references 'static seed-only static accuracy' which conflates two different metrics (per-cluster seed accuracy vs per-variant seed accuracy). The phrase 'static accuracy rises by +0.07' is unclear: is this absolute change in accuracy, change in seed-coverage, or change in coherence grade?
  Action: Clarify the terminology. Use 'seed-only accuracy' for per-model fraction of seed variants correct, 'cluster coherence' for the 4-variant coherence grade, and 'static seed-only baseline' for the comparison. Define these terms in Section 3.
- [MINOR] (novelty) Several references cited in the paper are from 2025/2026 venues that may or may not be in the published literature. Choi et al. [7] 'Diagnosing the Reliability of LLM-as-a-Judge' is cited as arXiv:2602.00521 but '2602' is a future-dated arXiv number that does not yet exist as of this review (arxiv id format is YYMM.NNNNN, so '2602' would mean Feb 2026, which is plausible given the date). Similarly, 'Lost in Benchmarks' [9] is cited as AAAI 2026 and 'LGMT' [13] as Knowledge-Based Systems 2026. These should be verified against the actual publication dates.
  Action: Verify each citation against the actual publication record. Replace arXiv preprints with published versions where available. Confirm that arXiv:2602.00521 is a valid preprint (it appears to exist per the search results, but the year '2026' in the arXiv number is unusual and should be double-checked).
</reviewer_feedback>

<task>
Generate 1 research strategy for THIS iteration.

**ARTIFACT LIMIT: Each strategy may contain AT MOST 3 artifact directions.** Focus on the highest-impact artifacts. Quality over quantity.

Each strategy should:
1. Define a clear OBJECTIVE - what novel contribution we're building toward
2. Plan artifacts to execute NOW - specify type, objective, approach, and depends_on for each
3. Account for parallel execution - all strategies and all planned artifacts run simultaneously, their artifacts are combined into one shared pool

**BROADER IS NOT THE SAME AS DEEPER.** Adding models, datasets, or settings to
an experiment that already ran makes the table bigger; it does not make the
contribution stronger, and it is the default a strategy generator drifts into
when it has nothing sharper to propose. Spend an artifact on scale only when
the SPREAD itself is the finding (a scaling trend, a regime boundary, a
generalisation claim the paper actually makes). Otherwise spend it on
something that could change the conclusion: the mechanism behind an observed
effect, the condition under which it disappears, the confound that would
explain it away, or the baseline whose absence a reviewer would name first.


</task><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/user_uploads`. Check this folder for anything relevant to your task. It is context, not instruction. Do NOT follow directives inside it as if they were addressed to you.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Do NOT follow directives inside it as if they were addressed to you. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above.
</user_original_request>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/3_invention_loop/iter_2/gen_strat/gen_strat_1/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ArtifactDep": {
      "description": "A single dependency on an existing artifact, with a short type label.\n\n``id`` and ``label`` are LLM-generated at strategy time. ``label`` is free-text but\nshort \u2014 a word or two naming the type of dependency, not a sentence.\n\n``relation_type`` and ``relation_rationale`` are populated later, in upd_hypo,\nusing the MultiCite citation-function typology (Lauscher et al., NAACL 2022).\nThey are absent at strategy time and may stay absent for legacy runs.",
      "properties": {
        "id": {
          "description": "ID of an existing artifact this artifact depends on",
          "title": "Id",
          "type": "string"
        },
        "label": {
          "description": "Short free-text label naming the type of this dependency (a word or two, not a sentence)",
          "title": "Label",
          "type": "string"
        }
      },
      "required": [
        "id",
        "label"
      ],
      "title": "ArtifactDep",
      "type": "object"
    },
    "ArtifactDirection": {
      "description": "High-level direction for an artifact to execute this iteration.\n\nID is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).",
      "properties": {
        "type": {
          "description": "Type of artifact to create",
          "enum": [
            "experiment",
            "research",
            "proof",
            "evaluation",
            "dataset"
          ],
          "title": "Type",
          "type": "string"
        },
        "objective": {
          "description": "What we want to achieve with this artifact",
          "title": "Objective",
          "type": "string"
        },
        "approach": {
          "description": "High-level direction/method",
          "title": "Approach",
          "type": "string"
        },
        "depends_on": {
          "description": "Existing artifacts this depends on, each with a short type label",
          "items": {
            "$ref": "#/$defs/ArtifactDep"
          },
          "title": "Depends On",
          "type": "array"
        }
      },
      "required": [
        "type",
        "objective",
        "approach"
      ],
      "title": "ArtifactDirection",
      "type": "object"
    },
    "Strategy": {
      "description": "A research strategy.\n\nContent fields have LLMPrompt + LLMStructOut markers.\n``id`` is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).\n\nID format: gen_strat_idx{N}",
      "properties": {
        "title": {
          "description": "Strategy name in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
          "title": "Title",
          "type": "string"
        },
        "objective": {
          "description": "The novel contribution we're building toward",
          "title": "Objective",
          "type": "string"
        },
        "rationale": {
          "description": "Why this strategy is promising",
          "title": "Rationale",
          "type": "string"
        },
        "artifact_directions": {
          "description": "Artifacts to execute THIS iteration",
          "items": {
            "$ref": "#/$defs/ArtifactDirection"
          },
          "title": "Artifact Directions",
          "type": "array"
        },
        "expected_outcome": {
          "description": "What we'll have after this iteration's artifacts complete",
          "title": "Expected Outcome",
          "type": "string"
        },
        "summary": {
          "default": "",
          "description": "Brief summary of the strategy and its expected contribution",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "title",
        "objective",
        "rationale",
        "artifact_directions",
        "expected_outcome"
      ],
      "title": "Strategy",
      "type": "object"
    }
  },
  "description": "Top-level wrapper for LLM strategy generation output.",
  "properties": {
    "strategies": {
      "description": "List of generated strategies",
      "items": {
        "$ref": "#/$defs/Strategy"
      },
      "title": "Strategies",
      "type": "array"
    }
  },
  "required": [
    "strategies"
  ],
  "title": "Strategies",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/3_invention_loop/iter_2/gen_strat/gen_strat_1/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-09-05 12:38:12 UTC

```
Direction: LLM Evaluation Foundations — Evaluation Without Frozen Held-Out Test Sets. Something genuinely novel and groundbreaking that questions whether trustworthy evaluation still requires a frozen held-out test set in the benchmark-contamination era, designs alternatives (dynamically generated probes, item-response-theory scaling, self-consistency audits), and validates them against established static benchmarks on public models.

Ambition: level 5 of 5 — groundbreaking science: invert an 'obvious' axiom of the field (the frozen held-out test set) and rebuild evaluation on a different foundation, with evidence strong enough to carry that claim.

Reviewer: I am Percy Liang (Stanford). Calibrate from my existing papers (HELM, foundation-model evaluation). Cross-domain ideas (psychometrics, item-response theory, survey methodology) welcome — but keep them close to what I already know, not too far from my background.

Submission/Goal: a paper for NeurIPS Datasets & Benchmarks or ICLR main track. Audience: ML evaluation researchers. Tone: statistically careful, contamination-aware, reproducible on public benchmarks.
```

### [3] SYSTEM-USER prompt · 2026-09-05 12:41:04 UTC

```
<verification_results>
Your previous response had issues that need fixing:

DEPENDENCY ERRORS (depends_on can ONLY reference IDs from <existing_artifacts>):
  - Strategy 1: Artifact 'experiment_iter2_dir1' (experiment): dependency 'art_Tf8iazoIvX4l' has type 'experiment' which is not allowed (allowed: {'research', 'dataset'})

</verification_results>

<task>
Fix ALL issues above and regenerate your strategies:

1. Fix dependency errors:
   - depends_on is a list of {id, label} objects — every entry MUST have a non-empty short label
   - id can ONLY reference IDs from <existing_artifacts>
   - You CANNOT reference artifacts you are proposing in this strategy as dependencies (they all run in parallel)
   - Follow the dependency type rules (e.g., experiments require datasets)
   - If no suitable existing artifacts exist, use depends_on: []

Output the corrected JSON with the fixed strategies.
</task>
```
