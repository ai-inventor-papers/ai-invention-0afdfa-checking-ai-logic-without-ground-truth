# gen_full_paper — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `run_56IKXpJEZJ5b` — M-IRT: Reference-Free LLM Evaluation via Samejima Graded Response Models on Dynamically Generated Metamorphic Item Clusters
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_full_paper` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-09-05 17:03:36 UTC

````
<task>
Create a publication-ready top-conference LaTeX paper with BibTeX from <paper_text> and <available_figures>, compile to PDF.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<paper_text>
title: >-
  M-IRT: Reference-Free LLM Evaluation via Samejima Graded Response Models on Dynamically Generated Metamorphic Item Clusters
abstract: >-
  Static LLM benchmarks with frozen held-out answer keys have become suspect as language models are trained on increasingly
  large fractions of the public web [2, 3, 18]. We ask a sharper question: can reasoning capability be measured when no answer
  key is trusted to be free of contamination? We introduce Metamorphic Item Response Theory (M-IRT), a reference-free framework
  that scores an LLM's internal logical coherence across dynamically generated Metamorphic Item Clusters (MICs). Each cluster
  carries four variants (seed, paraphrase, negation, and inverse or contrapositive) bound by a relational invariant whose
  oracle is derivable from the question text alone, so no absolute label exists. An ordinal coherence grade per (model, cluster)
  cell feeds a Samejima Graded Response Model (GRM) [6] fit by marginal maximum likelihood, recovering a per-model latent
  ability θ and per-item discrimination/difficulty. Across five public LLMs and 100 MICs spanning propositional syllogisms
  and grade-school arithmetic, the θ ranking correlates with published MMLU accuracy at Pearson r = 0.975 and exceeds three
  simpler binary consistency metrics computed on the same clusters. A stress test in which a model's seed response is forced
  to the oracle on 30% of clusters confirms that coherence grading penalises internally inconsistent response profiles. The
  pipeline is reproducible for under $0.05 in three minutes. The headline is methodological: the GRM scaling layer, the dynamic
  cluster generator, and a clearly scoped protocol for the natural-contamination experiment (system-prompt injection plus
  re-query) that the framework's hypothesis requires.
paper_text: |+
  ## 1 Introduction

  Benchmarks orient AI. They specify what is worth measuring and, in doing so, shape what is worth improving [1]. For language models, this role has been carried by fixed, curated test sets: a frozen set of items with a frozen answer key, run against a frozen evaluation harness. HELM [1] argued that the field needed broader coverage and multi-metric measurement, not that the frozen-test-set axiom itself was at risk. Six years on, that axiom is breaking.

  The proximate cause is contamination. As LLM training corpora have grown to include large fractions of the public web, fixed benchmark items and their gold labels have leaked into pre-training data. Deng et al. [2] report that GPT-4 verbatim fills in 57% of multiple-choice options masked from MMLU and ChatGPT 52%; the same pattern holds across HELM, GSM8K, and HumanEval. Balloccu et al. [3] document evaluation malpractice that effectively rewards memorisation, and Xu et al. [18] survey a four-level taxonomy of contamination (semantic, information, data, label) and matching-based versus comparison-based detection. Dynamic benchmarks that refresh items from recent sources, such as LiveBench [4], are one mitigation, but they still rely on a trusted answer key and so remain reference-dependent.

  This paper asks whether the answer key itself is dispensable. If we can construct a cluster of items whose correct answers are logically bound to one another, without specifying any absolute answer, then the only thing we need to measure is whether a model behaves consistently across that cluster. We call such a cluster a *Metamorphic Item Cluster (MIC)*, drawing the term from metamorphic testing [5, 22], where a metamorphic relation specifies how an output should transform when an input is perturbed, rather than what the output should equal. The same idea, applied to logical reasoning, says: if you can answer *P* correctly, then you should answer *not P* by the flipped label, the paraphrase by the same label, and the inverse (or contrapositive) by the same label. Logical coherence across the cluster is a graded observable; we never have to know whether the cluster's seed answer is "True" or "False" or "24".

  Logical coherence is not a measurement of accuracy, but it is a measurement of capability. A model that reasons tends to maintain coherence; a model that memorises a surface form breaks coherence the moment a paraphrase, negation, or inverse is applied. Coherence therefore satisfies a property no static benchmark can offer: it is invariant to having seen the answer key, because no answer key exists. If a model has memorised the answer to "All A are B; all B are C. Therefore all A are C", it has not memorised the answer to "Is it NOT the case that all A are C?" and it has not memorised the answer to the paraphrase using a different vocabulary.

  We turn coherence into a latent ability estimate by combining MICs with a Graded Response Model (GRM) [6]. The GRM is the canonical polytomous extension of item response theory, used in educational testing to score essay responses on ordered rubrics and recently applied to LLM-judge reliability [7]. Our application differs: the response variable is not a Likert rating or a correctness call, but the count of MIC variants a model answered coherently. Mapping this count to a 3-point ordinal scale (0/1/2) yields the response matrix that the GRM fits. From a fitted GRM we extract a per-model latent ability θ and per-item discrimination and difficulty parameters, in the standard IRT fashion [6, 8, 9, 10].

  A parallel literature (Elazar et al. [11], BECEL [13], Liu et al. [14], Novikova et al. [15], ConsistencyGate [16], Musawi and Lu [17]) uses logical consistency of an LLM's outputs as a reference-free evaluation signal, without IRT. M-IRT is distinct from this thread in three concrete ways. *First*, the response variable is polytomous: a 3-point ordinal grade driven by how many of the four variants a model answered coherently, rather than a binary invariance indicator. The polytomous GRM produces an interval-scaled θ whose Pearson correlation with MMLU (r = 0.975) exceeds the binary consistency metrics computed on the same clusters (paraphrase agreement: r = 0.905; negation invariance: r = 0.826). *Second*, the clusters are generated dynamically per evaluation session, so no cluster member can appear in any prior training corpus; the consistency literature operates on fixed prompt sets. *Third*, the target of evaluation is contamination-resistance as a property of the *response profile*: M-IRT measures whether a model's seed-only accuracy can rise while θ stays within its posterior standard error when the seed oracle is injected, which distinguishes a memorisation event from a capability gain. The consistency literature targets robustness, which is the same property under a different name and a different statistical instrument.

  Concretely, we generate 100 MICs (50 propositional syllogisms across 12 templates; 50 arithmetic word problems across 12 templates) and query five public LLMs on each of the four variants, for 2,000 calls completed in 167 seconds at $0.05 cumulative spend. The resulting θ values rank the models in close agreement with their published MMLU (Spearman ρ = 0.90; Kendall τ = 0.80) and HELM (ρ = 0.90; τ = 0.80) accuracy, despite never consulting those benchmarks during evaluation. We compare θ against simpler binary consistency metrics on the same clusters and find the metrics tie on rank statistics at this sample size (Spearman ρ = 0.90 across all of θ, paraphrase agreement, seed accuracy, and a composite) but separate on Pearson r, where θ (0.975) exceeds paraphrase agreement (0.905), seed accuracy (0.900), negation invariance (0.826), and the composite (0.855). An artificial stress test in which a model's seed response is forced to the oracle on 30% of clusters while the metamorphic variants are left untouched raises static seed accuracy by +0.07 and drops θ by −1.38, confirming that coherence grading penalises internal inconsistency but not establishing robustness to realistic memorisation. The natural-contamination protocol (system-prompt injection of the seed oracle followed by re-query on all four variants) is laid out in Section 6 as the test that would establish memorisation-resistance.

  **Summary of contributions.**

  - (i) A reference-free evaluation framework (M-IRT) that produces MICs dynamically, derives ordinal coherence grades from relational invariants, and fits a Samejima GRM to recover a per-model latent ability θ with no ground-truth answer key in the loop.
  - (ii) A reproducible pipeline of 100 MICs across two reasoning domains and a panel of five public models, completed end-to-end for under $0.05 and ~3 minutes, with an explicit ablation showing that θ's Pearson r with MMLU (0.975) exceeds three binary consistency metrics on the same clusters and that the metrics tie on Spearman ρ and Kendall τ at this sample size.
  - (iii) An artificial stress test that confirms coherence grading penalises internal inconsistency (Δstatic = +0.07, Δθ = −1.38), and a clearly scoped protocol (system-prompt injection of the seed oracle followed by re-query on all four variants) for the natural-contamination experiment the framework's hypothesis demands.

  [FIGURE:fig1]

  ## 2 Related Work

  **Holistic and multi-metric evaluation.** HELM [1] is the reference point for multi-metric LLM evaluation: a top-down taxonomy of scenarios and metrics applied to many models under standardised conditions. M-IRT inherits HELM's emphasis on standardised conditions and full-result transparency, but relaxes the assumption that the same items must be used for every model. Each model sees a freshly generated MIC, which removes the contamination vector HELM's frozen scenarios cannot eliminate.

  **Item response theory for LLM benchmarks.** Three recent works apply IRT to LLM evaluation. tinyBenchmarks [8] shows that 100 carefully chosen MMLU examples can reproduce full-benchmark accuracy within 1.9% MAE using a generalised performance-IRT estimator. Lost in Benchmarks [9] introduces PSN-IRT, a pseudo-siamese network for 4PL neural calibration trained end-to-end on 11 benchmarks (41,871 items) and reports stronger alignment with human preference than raw items. ATLAS [10] applies computerized adaptive testing to a calibrated bank of 3,000+ LLMs across five benchmarks, achieving MAE 0.157 on HellaSwag with 41 items. All three operate on *static* items with *known correct answers* and are therefore reference-dependent. M-IRT shares the GRM machinery with the LLM-judge reliability line [7] but replaces the correctness response with a coherence response, sidestepping both the calibration bank and the answer key.

  **Consistency as a research thread.** A parallel literature proposes logical consistency of an LLM's outputs as a reference-free evaluation signal, without using IRT. Elazar et al. [11] introduced the foundational definition: "the invariance of [a model's] behaviour under meaning-preserving alternations in its input", instantiated in ParaRel (328 paraphrases × 38 relations) and shown to be low across pretrained LMs. Jang, Kim, Lee, and Lukasiewicz [12] operationalised negational, symmetric, transitive, and additive consistency in BECEL across six transformer LMs and 21 tasks. Jang and Lukasiewicz [13] extended the framework to ChatGPT and GPT-4. Liu et al. [14] study logical preference consistency (negation, transitivity, commutativity) and report Spearman ρ = 0.98 (p = 0.000) between transitivity and self-agreement on NovelEval. Novikova et al. [15] survey the consistency literature and classify the twelve categories that have appeared. ConsistencyGate [16] applies self-consistency as a write-time admission gate to suppress memory contamination in LLM agents. Musawi and Lu [17] propose "contamination resistance" as an evaluation paradigm and instantiate it with a Caesar-cipher benchmark whose shift varies per instance.

  M-IRT is distinct from this thread in three concrete ways. *First*, the response variable is polytomous: a 3-point ordinal grade driven by how many of the four variants a model answered coherently, rather than a binary invariance indicator. The polytomous GRM produces an interval-scaled θ whose Pearson correlation with MMLU (0.975) exceeds the binary consistency metrics computed on the same clusters (paraphrase agreement: 0.905; negation invariance: 0.826), and a posterior standard error on θ that the binary indicators do not provide. *Second*, the clusters are generated dynamically per evaluation session, so no cluster member can appear in any prior training corpus; the consistency literature operates on fixed prompt sets. *Third*, the target of evaluation is contamination-resistance as a property of the *response profile*: M-IRT measures whether a contaminated model's seed-only accuracy can rise while θ stays within its posterior standard error when the seed oracle is injected, which distinguishes a memorisation event from a capability gain. The consistency literature targets robustness, namely whether paraphrase and negation invariance is preserved across perturbations, which is the same property under a different name and a different statistical instrument.

  **Contamination detection.** Deng et al. [2] introduce TS-Guessing, which masks a multiple-choice option and checks verbatim fill-in. Xu et al. [18] survey a four-level contamination taxonomy (semantic / information / data / label) and matching-based versus comparison-based detection. These works *detect* contamination after the fact; M-IRT is *immune* to label-level contamination because no label exists. The framework is not, however, immune to all contamination: a model that memorises the underlying *logical form* (e.g., the de Morgan identity) would still answer all four variants coherently and would receive a high θ, which is the correct outcome (the model has internalised a logical rule) but not a contamination-resistance result. The natural-contamination protocol in Section 4.6 is the test that distinguishes these cases.

  **Contamination-limited dynamic benchmarks.** LiveBench [4] refreshes items monthly from competitions, arXiv, and news. M-IRT is complementary: LiveBench's items still need an answer key, whereas MICs do not. The two can be combined into a dynamic benchmark whose scoring is by logical coherence rather than answer match.

  **Metamorphic testing for LLMs.** Chen et al. [5] define metamorphic relations (MRs) as input-output relations used to verify programs in lieu of oracles. LLMORPH [19] catalogues 191 NLP MRs across 24 tasks and runs 561,267 test executions, flagging MRs 9, 142, 154 as high-failure-low-false-positive. LGMT [20] derives 20 first-order-logic-grounded MRs (De Morgan, contraposition, quantifier shifts) and shows models are most sensitive to symbol- and conclusion-level variation. M-IRT adopts LGMT's logical perturbation set and uses a smaller but sufficient subset (paraphrase, negation, inverse / contrapositive) within each cluster.

  **Polytomous IRT in education.** Samejima's original GRM [6] estimates ordered-category responses with per-category thresholds, and is the foundation of M-IRT's response model. Choi et al. [7] apply the GRM to LLM-judge reliability and recommend priors (θ ~ N(0, 1), α ~ LogNormal(0, 0.5), β_k ~ N(0, 1) with ordering) that we adopt in our Bayesian-GRM future work.

  ## 3 Preliminaries

  **Notation.** For a panel of *M* LLMs and a set of *I* Metamorphic Item Clusters, each cluster contains four variants indexed by role *r* ∈ {seed, paraphrase, negation, inverse / contrapositive}. The cluster *i* carries relational invariants that bind the four oracle answers $\mathbf{a}_i = (a_{i,1}, \ldots, a_{i,4})$ without specifying an absolute label for any item. For logic, the negation variant's oracle is the Boolean complement of the seed's; for arithmetic, the negation variant's oracle is the fixed label "NO" (derived from the question text alone, without computing the seed's numeric answer), and the inverse variant's oracle is a quantity that appears explicitly in the seed's question text.

  **Graded Response Model.** Following Samejima [6], the probability that a model with latent ability θ produces a response of category $k \in \{0, 1, \ldots, K-1\}$ on item *i* is
  $$P(Y_i \geq k \mid \theta) = \frac{1}{1 + \exp(-\alpha_i(\theta - \beta_{i,k}))},$$
  where $\alpha_i > 0$ is the discrimination of item *i*, and $\beta_{i,1} < \beta_{i,2} < \ldots$ are the ordered category boundaries. The category probability is $P(Y_i = k \mid \theta) = P(Y_i \geq k \mid \theta) - P(Y_i \geq k+1 \mid \theta)$. Parameters are fit by marginal maximum likelihood using Gauss-Hermite quadrature on θ.

  **Coherence response.** For a (model, cluster) pair, let $c_{mi}$ denote the count of the four variants on which the model's response matches the role-appropriate oracle. We map $c_{mi}$ to an ordinal response
  $$Y_{mi} = \begin{cases} 0 & c_{mi} \in \{0, 1\} \\ 1 & c_{mi} = 2 \\ 2 & c_{mi} \in \{3, 4\}. \end{cases}$$

  The mapping is monotone: more coherent models receive higher grades. The 3-category structure is the smallest K that distinguishes "near-random" ($Y = 0$) from "partially coherent" ($Y = 1$) from "highly coherent" ($Y = 2$). The $c = 2$ bin captures "coherent on half the variants", the smallest signal that the model is reasoning rather than guessing; the $c \geq 3$ bin captures near-full coherence; the $c \leq 1$ bin captures chance-level performance. With 5 models and 100 items we cannot stably fit a K = 4 or K = 5 model; this is a sample-size limitation, not a principled choice.

  **Metamorphic relation.** A *metamorphic relation* [5] for a reasoning task is a deterministic relation $R(\text{input}_1, \text{input}_2) \Rightarrow R'(\text{output}_1, \text{output}_2)$ that holds for any correct solver. For syllogisms, the relation "input 2 is the negation of input 1" implies the relation "output 2 is the Boolean complement of output 1". For arithmetic, the relation "input 2 asks whether the answer equals an arbitrary non-answer integer" implies the relation "output 2 is the fixed label NO", derivable from the question text alone, not from the seed's value.


  ## 4 Method: M-IRT

  The M-IRT pipeline has four stages: MIC generation, model querying, coherence scoring, and GRM fitting with validation. Figure 1 diagrams the end-to-end flow.

  ### 4.1 Metamorphic Item Cluster Generator

  The generator is deterministic given a seed. It draws on two domain generators and produces four-variant clusters \footnote{Code: \url{https://github.com/ai-inventor-papers/ai-invention-0afdfa-checking-ai-logic-without-ground-truth/tree/main/round-1/experiment-1}}.

  **Logic generator.** Twelve syllogistic templates $T_1, \ldots, T_{12}$ express the canonical valid and invalid forms, inspired by the controlled-ontology construction of PrOntoQA [21] and the negation-sensitive template design of LogicBench [22]. Each template takes noun slots *A*, *B*, *C* drawn from disjoint noun pools for the seed and the paraphrase, ensuring that paraphrase and seed never share vocabulary. A template returns a two-premise argument, a candidate conclusion, and an oracle label V (valid) or I (invalid). The four variants are:
  - *Seed:* the original syllogism with original nouns.
  - *Paraphrase:* the same argument with nouns from a disjoint pool.
  - *Negation:* the conclusion negated; oracle is the Boolean complement of the seed label, derivable from the question text alone.
  - *Contradiction* (the logic-domain equivalent of the arithmetic inverse): one premise negated; oracle flips if and only if the syllogism is *Barbara*-style (T4, T10, T12); otherwise it stays.

  **Arithmetic generator.** Twelve templates express one- and two-step word problems with named participants, named items, and integer quantities in $[2, 99]$, following the GSM8K [23] and MAWPS [24] constructions. Paraphrase substitutes items from a disjoint pool and may rename participants. The negation variant asks "Is the answer to this problem equal to *wrong*?", where *wrong* is an arbitrary non-answer integer (a different *wrong* per cluster); the oracle is the fixed label "NO", derivable from the question text alone without solving the seed. The inverse variant asks "What was the original starting quantity (the first number mentioned)?"; the oracle is a quantity that appears explicitly in the seed's question text, also derivable without solving the seed.

  The two generators together emit 50 logic clusters and 50 arithmetic clusters, for 100 clusters per evaluation session . Each cluster carries an oracle answer, a difficulty hint (medium / hard), and a relational-invariant table that the scorer uses to evaluate the negation and inverse variants. Two evaluation sessions run with different seeds produce disjoint clusters, so the contamination surface for any single MIC is the single session that ran it.

  ### 4.2 Model Querying

  We evaluate five public LLMs via the OpenRouter chat-completion API: GPT-4o-mini, Claude Haiku 4.5, Llama 3.1 8B Instruct, Qwen 2.5 7B Instruct, and Mistral Small 24B Instruct 2501. Each model is presented with each of the 400 variant questions (100 clusters × 4 variants) in a single, zero-shot prompt: "Answer with V or I." for logic, or with the integer answer for arithmetic. We run with concurrency 10 and a global 12 rpm cap, completing all 2,000 calls in 167 seconds at $0.048 cumulative spend . No model is fine-tuned or prompted with worked examples; the prompt template is identical across models.

  ### 4.3 Ordinal Coherence Scoring

  For each (model, cluster) pair, we parse each variant's response into the canonical response space ({V, I} for logic, integer or {YES, NO} for arithmetic) and compare to the role-appropriate oracle. The negation variant's oracle is *not* the seed's oracle; for logic it is the Boolean complement, for arithmetic it is the fixed label "NO". The inverse variant's oracle is a quantity that appears explicitly in the seed's question text, also derivable without computing the seed. A correct response on all four variants yields a raw count of 4; we map it to the ordinal scale $Y_{mi} \in \{0, 1, 2\}$ as in Section 3. The scoring rules are deterministic and parser-level: they do not depend on a separate language model, judge, or human rater.

  ### 4.4 GRM Fitting

  We fit the GRM via `girth.grm_mml`, an open-source marginal-maximum-likelihood implementation in Python. The input is the (M × I) integer response matrix; the output is a vector of M latent abilities $\theta_j$, a vector of I discriminations $\alpha_i$, and an (I × (K − 1)) matrix of difficulty thresholds $\beta_{i,k}$. We use K = 3 categories. No priors are imposed on θ beyond the standard normal default of `girth`; discrimination and difficulty are estimated freely. The fit takes roughly three seconds on the (5 × 100) matrix .

  ### 4.5 Validation A: External-Benchmark Correlation

  To verify that θ captures reasoning rather than a proxy unrelated to capability, we correlate θ with each model's published MMLU accuracy and HELM accuracy . We report Pearson r with a 10,000-resample bootstrap 95% confidence interval, Spearman ρ, and Kendall τ. We also compute three binary consistency baselines on the same clusters (seed-only accuracy, paraphrase agreement rate, negation invariance rate, and their composite) and report the same correlations for each. The five-model panel limits the statistical resolution of all of these correlations; we treat them as point-estimate diagnostics rather than as confirmatory evidence.

  ### 4.6 Validation B: Stress Test of Coherence Scoring

  We probe the behaviour of coherence grading under a deliberately constructed internal inconsistency on Qwen 2.5 7B. On 30% of clusters (chosen by a random subset), the model's seed response is forced to the oracle, while the paraphrase, negation, and inverse responses are left at whatever the model produced. The seed oracle injection is performed at the response-matrix level: the parsed seed answer is replaced by the oracle in the per-variant flags, and the ordinal score and θ are recomputed. Under this stress, we expect:
  - Static seed-only accuracy to *increase* (the model now "knows" the seed answers).
  - The ordinal coherence score on the contaminated clusters to *not* rise by the same amount (the metamorphic variants still reflect the model's actual reasoning).
  - The GRM-fitted θ to either decrease or remain stable.

  This stress test isolates one axis of contamination-resistance (internal consistency between the seed slot and the metamorphic slots), but does not exhaust the realistic contamination scenarios. A natural-contamination protocol (system-prompt injection of the seed answer followed by re-query on all four variants) is the proper test and is laid out as future work in Section 6.


  ## 5 Experiments

  ### 5.1 Setup

  The pipeline runs in five sequential stages: cluster generation, model querying, coherence scoring, GRM fitting, and validation (validation runs two sub-experiments: the external correlation check and the stress test). Hardware: a CPU-only container with 6 GB RAM and a 4-hour CPU cap; total runtime 211 seconds. The five models are queried via the OpenRouter chat-completion interface with no system prompt, temperature 0, and a 4-token output budget. Responses are stored as one record per (model, variant) call; the fitted GRM and validation statistics are released alongside the code .

  **Terminology.** *Seed-only accuracy* is the per-model fraction of seed variants whose response matches the seed oracle; it is the metric most directly comparable to a static benchmark score. *Cluster coherence* (the 3-point ordinal $Y_{mi}$) is the count of MIC variants a model answered correctly on a given cluster, mapped to 0/1/2. *Coherence-2 rate* is the fraction of clusters on which a model achieved $Y = 2$ (the top grade, i.e., coherent on at least 3 of 4 variants). *Paraphrase agreement* is the fraction of seed-correct clusters on which the model also answered the paraphrase correctly. *Negation invariance* is the fraction of seed-correct clusters on which the model answered the negation correctly, i.e., produced the Boolean complement (logic) or "NO" (arithmetic). Both are computed on the present 100 clusters .

  ### 5.2 Latent Ability Ranking

  Table 1 reports θ and the published MMLU / HELM accuracy for each model, sorted by θ.

  **Table 1. GRM-estimated θ versus published MMLU and HELM accuracy (n = 5 models).**

  | Model | θ | MMLU | HELM |
  |---|---:|---:|---:|
  | openai/gpt-4o-mini | +3.69 | 0.820 | 0.79 |
  | anthropic/claude-haiku-4.5 | +3.56 | 0.801 | 0.78 |
  | qwen/qwen-2.5-7b-instruct | +0.07 | 0.707 | 0.69 |
  | mistralai/mistral-small-24b-instruct-2501 | −0.28 | 0.732 | 0.71 |
  | meta-llama/llama-3.1-8b-instruct | −1.37 | 0.684 | 0.65 |

  The θ ranking separates the bottom model (Llama 3.1 8B) from the rest by 1.1 θ-units and groups the top two (GPT-4o-mini, Claude Haiku 4.5) within 0.13 θ-units. Qwen 2.5 7B and Mistral Small 24B land between these clusters, at +0.07 and −0.28 respectively, which is 0.35 θ-units apart. The MMLU ranking is GPT-4o-mini > Claude Haiku 4.5 > Mistral Small 24B > Qwen 2.5 7B > Llama 3.1 8B; the θ ranking swaps Mistral Small 24B and Qwen 2.5 7B, the one inversion that bounds Spearman ρ at 0.90 and Kendall τ at 0.80 (the maximum possible given a single swap). Pearson r between θ and MMLU is +0.975 (95% bootstrap CI [0.59, 1.00]); between θ and HELM is +0.976 (CI [0.80, 1.00]) .

  The wide bootstrap CI reflects the small sample size (n = 5): the lower bound already allows r = 0.59, well below the r > 0.85 hypothesis criterion, and the upper bound is a ceiling artefact. We treat the Pearson r as a point-estimate diagnostic rather than as confirmatory evidence. The rank statistics are more interpretable at n = 5: ρ = 0.90 corresponds to exactly one rank inversion out of ten pairs, and τ = 0.80 corresponds to two discordant pairs out of ten, which is the worst-case bound given the Mistral-Qwen swap. The natural next step is to expand the panel to the n ≥ 15 the hypothesis demands and re-run; with more models, the swap between adjacent MMLU ranks would either resolve or replicate.

  [FIGURE:fig2]

  ### 5.3 Per-Model Coherence Distribution

  Across 100 clusters, the ordinal response distributions show the expected separation :

  **Table 2. Ordinal coherence distribution per model across 100 MICs.**

  | Model | Y = 0 | Y = 1 | Y = 2 | mean raw correct |
  |---|---:|---:|---:|---:|
  | anthropic/claude-haiku-4.5 | 5 | 21 | 74 | 3.21 |
  | openai/gpt-4o-mini | 5 | 20 | 75 | 3.11 |
  | mistralai/mistral-small-24b-instruct-2501 | 7 | 19 | 74 | 2.94 |
  | qwen/qwen-2.5-7b-instruct | 16 | 17 | 67 | 2.78 |
  | meta-llama/llama-3.1-8b-instruct | 20 | 26 | 54 | 2.32 |

  The top two models achieve the top grade on 74–75% of clusters and the bottom grade on only 5%, so the "near-random" tail is small. Llama 3.1 8B still achieves the top grade on 54% of clusters, indicating that even weak models solve roughly half of all clusters coherently. The signal the GRM exploits is the bottom-grade fraction, which ranges from 5% (Claude Haiku 4.5, GPT-4o-mini) to 20% (Llama 3.1 8B), a 4× spread that the GRM uses to separate the bottom model from the rest, and a similar pattern in the middle of the table where Qwen's bottom-grade fraction (16%) exceeds Mistral's (7%) despite Mistral's higher MMLU. The fact that the per-cluster ordinal grade separates models that static accuracy alone cannot (Mistral has higher seed accuracy but a worse bottom-grade fraction than Qwen) is the mechanism behind the Pearson r gap in Section 5.4.

  [FIGURE:fig3]

  ### 5.4 Comparison Against Binary Consistency Baselines

  We compute three reference-free baselines on the same clusters and report their agreement with MMLU / HELM alongside θ in Table 3.

  **Table 3. Reference-free metrics vs. MMLU and HELM accuracy on n = 5 models.**

  | Metric | Pearson r (MMLU) | Spearman ρ (MMLU) | Kendall τ (MMLU) | Pearson r (HELM) | Spearman ρ (HELM) | Kendall τ (HELM) |
  |---|---:|---:|---:|---:|---:|---:|
  | Seed-only accuracy | +0.900 | +0.900 | +0.800 | +0.941 | +0.900 | +0.800 |
  | Paraphrase agreement rate | +0.905 | +0.900 | +0.800 | +0.943 | +0.900 | +0.800 |
  | Negation invariance rate | +0.826 | +0.800 | +0.600 | +0.886 | +0.800 | +0.600 |
  | Composite (mean of PA, NI) | +0.855 | +0.900 | +0.800 | +0.909 | +0.900 | +0.800 |
  | **GRM θ** | **+0.975** | **+0.900** | **+0.800** | **+0.976** | **+0.900** | **+0.800** |

  The headline observation has two parts. *On Pearson r*, the GRM θ exceeds every binary baseline by a margin visible on the n = 5 panel: θ (0.975) > paraphrase agreement (0.905) > seed accuracy (0.900) > composite (0.855) > negation invariance (0.826) against MMLU; the same ordering holds against HELM. The reason is that θ is an interval-scaled ability score that captures *how much* better one model is than another, while a binary proportion only captures whether one model beats another. The four θ values for the four top models (3.69, 3.56, 0.07, −0.28) span 3.97 θ-units and are spread across that range, whereas the binary metrics cluster between 0.83 and 0.95, a 12-point proportion range that is more compressed. The GRM's nonlinear mapping from raw counts to latent ability produces a wider dynamic range, which Pearson r picks up but Spearman ρ does not. *On rank statistics*, all four metrics tie at Spearman ρ = 0.90 and Kendall τ = 0.80 (and at ρ = 0.80 / τ = 0.60 for negation invariance alone), because every metric in this table reflects the same single rank inversion, the Mistral-Qwen swap, and ties are broken at the metric level rather than the data level.

  This is the principled argument for the GRM framing. θ and paraphrase agreement agree on the rank ordering of the five models at this sample size, but θ captures more information than the binary proportion. With a larger panel (n ≥ 15), the rank ties should resolve and the Pearson r advantage should widen or collapse depending on whether the Mistral-Qwen swap replicates or reverses. We argue that even at the present sample size, the GRM scaling layer earns its place because it produces an interval-scaled θ with a posterior standard error, item-level discrimination and difficulty parameters that enable adaptive testing, and a per-cluster coherence grade that is the natural response variable for the natural-contamination protocol in Section 6.

  ### 5.5 Domain Decomposition and Item Parameters

  Per-domain coherence for the top model (GPT-4o-mini) shows arithmetic clusters easier than logic clusters across all five models: arithmetic mean raw correct 3.56, logic mean raw correct 2.66 . This matches the difficulty gradient we would expect from a grade-school word-problem corpus versus a categorical-syllogism corpus. The arithmetic-vs-logic gap is consistent across models and contributes to the strong MMLU / HELM correlation: published benchmark accuracy reflects a similar mix of formal-reasoning and arithmetic-reasoning items.

  The fitted discriminations $\alpha_i$ cluster at the upper and lower ends of the allowed range : 62 of the 100 items sit at the floor of approximately 0.2 (items on which the GRM could not separate models), 14 sit at the ceiling of 5.0 (the most discriminative items, including arith_0001, arith_0002, arith_0033, arith_0046, arith_0048, logic_0006, logic_0009, logic_0027, logic_0041, logic_0045), and 24 fall in between. The concentration at the bounds reflects the small panel (n = 5): with only five response vectors per item, the GRM has limited information to estimate $\alpha$ precisely, and items with all five models at the same grade get pushed to the discrimination floor. Difficulty thresholds $\beta_{i,k}$ for the most discriminative items lie at moderate θ values around −0.9, suggesting that these items discriminate primarily among the mid-ability models. Items at the discrimination floor carry no signal for θ estimation and do not distort it; we retain them for completeness rather than discard them, since dropping items would change the response matrix the GRM sees. The K = 3 ordinal mapping compresses 5 raw counts (0–4) into 3 categories; we held K = 3 in this proof-of-concept because the present sample size does not support fitting more thresholds per item without over-fitting. With a larger panel (n ≥ 15) and more items, K = 4 (splitting raw 0, 1, 2, 3, 4 into four grades) would let the GRM exploit more granularity.

  ### 5.6 Stress Test of Coherence Scoring Under Forced Internal Inconsistency

  The stress test on Qwen 2.5 7B across three random seeds (0, 1, 42) produces :

  **Table 4. Stress test on Qwen 2.5 7B: seed response forced to oracle on 30% of clusters while metamorphic variants are unchanged.**

  | Seed | Seed-only acc (clean) | Seed-only acc (stressed) | Δ seed-only | θ (clean) | θ (stressed) | Δ θ |
  |---|---:|---:|---:|---:|---:|---:|
  | 0 | 0.78 | 0.85 | +0.07 | −0.001 | −1.389 | −1.387 |
  | 1 | 0.78 | 0.84 | +0.06 | −0.001 | −1.387 | −1.385 |
  | 42 | 0.78 | 0.86 | +0.08 | −0.001 | −1.373 | −1.372 |
  | **mean** | 0.78 | 0.85 | **+0.07** | −0.001 | **−1.382** | **−1.382** |
  | std | n/a | n/a | 0.01 | n/a | n/a | 0.007 |

  Seed-only accuracy rises by +0.07 on average, but the GRM-estimated θ falls by an average of −1.382 with a standard deviation of 0.007 across the three random subsets of contaminated clusters. The stability of Δθ (the standard deviation is 1.8% of the mean) indicates that the coherence grading signal is robust to which specific clusters are chosen for contamination. Forcing the seed to be correct on a cluster where the metamorphic variants disagree with each other is exactly the profile the GRM was designed to penalise: the cluster's raw coherence count stays low, the ordinal grade stays low, and the model's θ drops as the GRM rebalances to fit a more internally inconsistent response matrix.

  We are explicit about the scope of this finding. The stress test isolates one axis of contamination (internal inconsistency between the seed slot and the metamorphic slots) and confirms that coherence scoring does penalise it. It does *not* establish that M-IRT resists realistic contamination in the broader sense. A natural-contamination protocol (injecting the seed oracle into the system prompt for a chosen subset of clusters, re-querying the model on all four variants of those clusters, and observing whether the paraphrase / negation / inverse responses become coherent as a consequence of memorisation) is the test that would establish memorisation-resistance. We leave that experiment to future work; the system-prompt injection requires a multi-turn pipeline that the present artifact does not implement. If, under natural contamination, all four variants of a contaminated cluster became coherent (because the model memorised the underlying logical form), θ would not penalise the cluster and the contamination-resistance claim would fail. This is the test that distinguishes a memorisation event from a capability gain.

  [FIGURE:fig4]


  ## 6 Discussion

  **What worked.** M-IRT produces a θ ranking that matches MMLU and HELM at Pearson r = 0.975 / 0.976 and Spearman ρ = 0.90 / Kendall τ = 0.80 on a five-model panel, despite never inspecting the model's responses against a fixed answer key. The GRM scaling layer adds value over simpler binary consistency metrics on Pearson r: θ (0.975) exceeds paraphrase agreement (0.905), seed accuracy (0.900), negation invariance (0.826), and the composite (0.855) on the same clusters. The coherence grading correctly penalises internal inconsistency in the seed-versus-metamorphic slot pattern (Δθ = −1.382, σ = 0.007, across three random subsets of contaminated clusters). The pipeline runs on commodity CPU hardware for $0.048 and three minutes per session, which is comparable to a single LLM API call's latency and orders of magnitude cheaper than full-benchmark evaluation [1, 8].

  **What did not work as hoped.** The headline Pearson r = 0.975 is supported by a wide bootstrap CI [0.59, 1.00] because the panel contains only five models; the lower bound already allows r = 0.59, well below the r > 0.85 hypothesis criterion. The middle of the θ ranking carries one rank inversion relative to MMLU (Mistral Small 24B and Qwen 2.5 7B are swapped), which is the bound on Spearman ρ at this sample size. With five models and 100 items, the GRM fit has only five degrees of freedom for θ estimation, so small per-item perturbations can produce visible θ shifts on the order of ±0.5; we mitigate by reporting Δθ (a within-model comparison) under the stress test rather than absolute θ. A practitioner using M-IRT on a small panel should report θ deltas under interventions rather than absolute θ; the principled argument for the GRM framing (item parameters, posterior SE, per-cluster grade) only stabilises with panels of n ≥ 15.

  **Limitations.**

  - *Five-model panel.* The contamination-resistance result is a within-model comparison (Δθ for one model under one intervention), so it is robust to small panels. The external-correlation result requires a larger panel to narrow the bootstrap CI and to determine whether the Mistral-Qwen rank inversion replicates or resolves. The hypothesis specifies n ≥ 15; the present artifact implements n = 5 because the OpenRouter cost ceiling and per-model licensing in the evaluation environment restricted the panel. Adding 10 to 15 more models is the single most consequential next step.
  - *Two domains.* M-IRT currently covers propositional syllogisms and grade-school arithmetic. Real reasoning also includes multi-hop reading comprehension and first-order logic; FOLIO [25] provides the closest precedent for the latter. The MMLU correlation we report therefore reflects the syllogistic + arithmetic component of reasoning capability, which is correlated with general capability but does not probe MMLU's history / law / medicine / biology domains directly. Extending the MIC bank to four reasoning domains (syllogisms, arithmetic, multi-hop reading, first-order logic) would test whether the θ ranking replicates across domains and whether the Pearson r advantage over binary metrics holds.
  - *Artificial stress test, not natural contamination.* The response-matrix-level stress test in Section 5.6 confirms that coherence grading penalises an internally inconsistent profile, but it does not test the contamination-resistance claim in the realistic sense. A natural-contamination experiment (inject the seed oracle into the system prompt, re-query all four variants, and measure whether coherence rises on the metamorphic slots) is the proper test and is listed as future work.
  - *Twelve templates per domain.* Twelve logic templates and twelve arithmetic templates cover the classical syllogistic forms and the most common word-problem operations, but they are not exhaustive. A larger generator bank would yield finer per-item discrimination estimates.
  - *Polytomous response scale.* The 0/1/2 mapping compresses 5 raw counts (0–4) into 3 categories. With a larger panel, K = 4 or K = 5 would let the GRM exploit more granularity at the cost of greater estimation variance.
  - *Reference-free for what?* M-IRT eliminates the absolute label for any item, but the relational invariants are themselves authored. A model that memorises the *form* of the metamorphic relation (e.g., that "not P" flips a V/I label) would still answer all four variants coherently and would receive a high θ. This is the correct outcome (the model has internalised a logical rule) but is not a contamination-resistance result. The natural-contamination protocol is the test that distinguishes "internalised the rule" from "memorised the seeds".

  **Future work.**

  - *Expand to n ≥ 15 models.* Add clusters at no extra query cost and re-run the analysis. The added span will give a Spearman ρ with MMLU / HELM that has a meaningful CI and supports the rank claim, and will determine whether the Mistral-Qwen swap replicates.
  - *Natural-contamination experiment.* System-prompt injection of the seed oracle for a chosen subset of clusters, re-query on all four variants, and measure whether coherence rises on the metamorphic slots or stays low. This is the test that validates or refutes the contamination-resistance claim in the realistic sense, following the masking-and-guessing paradigm of TS-Guessing [2] and the label-level injection framing of Xu et al. [18].
  - *Multi-domain M-IRT.* Add clusters for multi-hop reading comprehension (paragraph + question chain) and first-order logic (FOLIO-style annotations [25]) following the LGMT / PrOntoQA / LogicBench precedents cited.
  - *Bayesian GRM with informative priors.* Replace MML with Hamiltonian Monte Carlo and add the priors Choi et al. [7] recommend (θ ~ N(0, 1), α ~ LogNormal(0, 0.5), β_k ~ N(0, 1) with ordering), which would let M-IRT handle panels of 2–3 models without degenerate fits and produce a principled posterior standard error on θ.
  - *Adaptive MIC selection.* Once the GRM is calibrated on a larger panel, choose the next MIC from a candidate pool using maximum Fisher information on θ, in the spirit of computerized adaptive testing [10].
  - *Online contamination monitoring.* Deploy M-IRT as a recurring audit: re-run a small MIC set weekly, and alert if a model's θ moves relative to its previous θ by more than one posterior standard error. This would catch gradual contamination that static benchmarks miss.

  ## 7 Conclusion

  The frozen held-out test set is no longer the only foundation for LLM evaluation. M-IRT shows that a dynamically generated, reference-free benchmark, built from clusters of logically related items whose relational invariants are known without absolute labels, can produce a latent ability estimate that correlates with MMLU at Pearson r = 0.975 (Spearman ρ = 0.90, Kendall τ = 0.80) on the present five-model panel, a correlation that exceeds every binary consistency baseline on Pearson r and ties with them on rank statistics. The contribution is methodological rather than competitive: the cluster generator, the GRM-based coherence scoring, the protocol for the natural-contamination experiment that the hypothesis demands, and the honest accounting of where the present evidence falls short. We release code, prompts, raw responses, and fitted parameters under an MIT license .

  ## References

  [1] P. Liang et al., "Holistic Evaluation of Language Models," *Transactions on Machine Learning Research*, 2022.

  [2] C. Deng, Y. Zhao, X. Tang, M. B. Gerstein, and A. Cohan, "Investigating Data Contamination in Modern Benchmarks for Large Language Models," *NAACL*, 2024.

  [3] S. Balloccu, P. Schmidtová, M. Lango, and O. Dusek, "Leak, Cheat, Repeat: Data Contamination and Evaluation Malpractices in Closed-Source LLMs," *EACL*, 2024.

  [4] C. White et al., "LiveBench: A Challenging, Contamination-Limited LLM Benchmark," *ICLR*, 2024.

  [5] T. Y. Chen, F.-C. Kuo, H. Liu, P.-L. Poon, D. Towey, T. H. Tse, and Z. Q. Zhou, "Metamorphic Testing: A Review of Challenges and Opportunities," *ACM Computing Surveys*, vol. 51, no. 1, 2018.

  [6] F. Samejima, "Estimation of Latent Ability Using a Response Pattern of Graded Scores," *Psychometrika*, vol. 34, no. S1, pp. 1–97, 1969.

  [7] J. Choi, S. Park, C. Cho, H. Park, and B. Kim, "Diagnosing the Reliability of LLM-as-a-Judge via Item Response Theory," *ICML*, 2026.

  [8] F. M. Polo, L. Weber, L. Choshen, Y. Sun, G. Xu, and M. Yurochkin, "tinyBenchmarks: Evaluating LLMs with Fewer Examples," *ICML*, 2024.

  [9] H. Zhou et al., "Lost in Benchmarks? Rethinking Large Language Model Benchmarking with Item Response Theory," *AAAI*, 2026.

  [10] P. Li, X. Tang, S. Chen, Y. Cheng, R. Metoyer, T. Hua, and N. V. Chawla, "Adaptive Testing for LLM Evaluation: A Psychometric Alternative to Static Benchmarks," *ICML*, 2026.

  [11] Y. Elazar, N. Kassner, S. Ravfogel, A. Ravichander, E. Hovy, H. Schütze, and Y. Goldberg, "Measuring and Improving Consistency in Pretrained Language Models," *TACL*, vol. 9, pp. 1012–1031, 2021.

  [12] M. Jang, T. Kim, C. Lee, and T. Lukasiewicz, "BECEL: Benchmark for Consistency Evaluation of Language Models," *COLING*, 2022.

  [13] M. Jang and T. Lukasiewicz, "Consistency Analysis of ChatGPT," *EMNLP*, 2023.

  [14] Y. Liu, Z. Guo, T. Liang, E. Shareghi, I. Vulić, and N. Collier, "Aligning with Logic: Measuring, Evaluating and Improving Logical Preference Consistency in Large Language Models," *ICML*, 2025.

  [15] J. Novikova, C. Anderson, B. Blili-Hamelin, and S. Majumdar, "Consistency in Language Models: Current Landscape, Challenges, and Future Directions," *ICML Workshop on Reliable and Responsible Foundation Models*, 2025.

  [16] Y. Zhang and S. Li, "ConsistencyGate: Preventing Memory Contamination in LLM Agents via Self-Consistency Admission Control," *arXiv:2607.22962*, 2026.

  [17] R. Musawi and S. Lu, "Towards Contamination Resistant Benchmarks," *arXiv:2505.08389*, 2025.

  [18] C. Xu, S. Guan, D. Greene, and M.-T. Kechadi, "Benchmark Data Contamination of Large Language Models: A Survey," *arXiv:2406.04244*, 2024.

  [19] S. Cho, S. Ruberto, and V. Terragni, "Metamorphic Testing of Large Language Models for Natural Language Processing," *IEEE ICSME*, 2025.

  [20] Z. Zhou, M. Li, X. Fang, X. Zhou, W. Li, and Z. Zheng, "LGMT: Logic-Grounded Metamorphic Testing for Evaluating the Reasoning Reliability of LLMs," *Knowledge-Based Systems*, vol. 348, p. 116324, 2026.

  [21] A. Saparov and H. He, "Language Models Are Greedy Reasoners: A Systematic Formal Analysis of Chain-of-Thought," *ICLR*, 2023.

  [22] M. Parmar et al., "LogicBench: Towards Systematic Evaluation of Logical Reasoning Ability of Large Language Models," *ACL*, 2024.

  [23] K. Cobbe et al., "Training Verifiers to Solve Math Word Problems," *arXiv:2110.14168*, 2021.

  [24] R. Koncel-Kedziorski, S. Roy, A. Amini, N. Kushman, and H. Hajishirzi, "MAWPS: A Math Word Problem Repository," *NAACL*, 2016.

  [25] S. Han et al., "FOLIO: Natural Language Reasoning with First-Order Logic," *EMNLP*, 2024.

summary: >-
  M-IRT is a reference-free LLM evaluation framework that scores an LLM's internal logical coherence across dynamically generated
  Metamorphic Item Clusters and fits a Samejima Graded Response Model to recover a per-model latent ability theta and per-item
  discrimination/difficulty. Across five public LLMs and 100 MICs spanning propositional syllogisms and grade-school arithmetic,
  theta correlates with published MMLU accuracy at Pearson r = 0.975 (Spearman rho = 0.90, Kendall tau = 0.80) and exceeds
  three binary consistency baselines computed on the same clusters. An artificial stress test on Qwen 2.5 7B confirms that
  coherence grading penalises internal inconsistency (mean Delta theta = -1.382 across three random seeds). The pipeline is
  reproducible for under $0.05 in three minutes.
</paper_text>

<available_figures>
--- Item 1 ---
id: fig1
figure_type: concept
title: M-IRT Pipeline
caption: >-
  The four-stage M-IRT pipeline: deterministic MIC generation, zero-shot model querying, ordinal coherence scoring, and Samejima
  GRM fitting with two validation sub-experiments.
image_gen_detailed_description: >-
  Horizontal flow diagram, left to right, on a clean white background. Stage 1 (leftmost box, light blue): 'Cluster Generator'
  with arrow out labelled 'seed=0' showing input. Inside the box, four small icons represent the four variants per MIC: 'seed'
  (a question mark icon), 'paraphrase' (a rephrasing icon), 'negation' (a crossed-out icon), and 'contradiction/inverse' (a
  circular arrow icon). Stage 2 (second box, green): 'Model Querying', with five model icons in a column (GPT-4o-mini, Claude
  Haiku 4.5, Llama 3.1 8B, Qwen 2.5 7B, Mistral Small 24B), each producing 400 responses (5 models x 4 variants x 100 clusters).
  Stage 3 (third box, orange): 'Coherence Scoring', receiving the response matrix and emitting a 5x100 ordinal matrix (Y in
  {0, 1, 2}). Stage 4 (fourth box, purple): 'GRM Fitting via girth.grm_mml', emitting three outputs in three coloured side-boxes:
  theta (5 abilities, blue), alpha (100 discriminations, orange), beta (200 thresholds, green). Stage 5 (rightmost, red):
  'Validation', with two sub-boxes: 'Validation A: theta vs MMLU/HELM' and 'Validation B: stress test on Qwen 2.5 7B'. Arrows
  connect Stage 1 -> Stage 2 -> Stage 3 -> Stage 4 -> Stage 5. A small annotation below Stage 2 says '2,000 calls in 167 seconds,
  $0.048 cumulative'. Sans-serif font. Aspect ratio 21:9 to span the full width of a NeurIPS page.
aspect_ratio: '21:9'
summary: >-
  Pipeline diagram: cluster generation, querying, coherence scoring, GRM fitting, validation.
figure_path: figures/fig1_v0.jpg

--- Item 2 ---
id: fig2
figure_type: data
title: theta vs MMLU
caption: >-
  GRM-estimated theta versus published MMLU accuracy for n = 5 LLMs. Pearson r = 0.975, Spearman rho = 0.90, Kendall tau =
  0.80. The single rank inversion (Mistral Small 24B and Qwen 2.5 7B are swapped) bounds the rank statistics at this sample
  size.
image_gen_detailed_description: >-
  Scatter plot with five labelled points. X-axis: 'theta (GRM-estimated latent ability)', range -2.0 to +4.0. Y-axis: 'MMLU
  accuracy', range 0.60 to 0.85. Points (x, y): GPT-4o-mini at (3.69, 0.820), labelled 'GPT-4o-mini'; Claude Haiku 4.5 at
  (3.56, 0.801), labelled 'Claude Haiku 4.5'; Qwen 2.5 7B at (0.07, 0.707), labelled 'Qwen 2.5 7B'; Mistral Small 24B at (-0.28,
  0.732), labelled 'Mistral Small 24B'; Llama 3.1 8B at (-1.37, 0.684), labelled 'Llama 3.1 8B'. Each point is a filled circle
  of diameter 12 px with a black outline. Mistral Small 24B and Qwen 2.5 7B are connected by a short dashed grey arrow showing
  the rank inversion. Annotation in the upper-right corner, in two lines: 'Pearson r = 0.975' and 'Spearman rho = 0.90 (one
  rank inversion)'. Light grey grid lines at every 1 theta-unit on X and every 0.05 MMLU on Y. Sans-serif font, white background.
  Aspect ratio 4:3 (compact square-ish plot).
aspect_ratio: '4:3'
summary: >-
  Five-model scatter showing high theta-MMLU correlation with the Mistral-Qwen rank inversion highlighted.
figure_path: figures/fig2_v0.pdf

--- Item 3 ---
id: fig3
figure_type: data
title: Per-Model Coherence Distribution
caption: >-
  Ordinal coherence distribution per model across 100 MICs. The top two models achieve the top grade on 74-75% of clusters
  and the bottom grade on only 5%. Llama 3.1 8B sits at the floor on 20% of clusters, a 4x spread that the GRM exploits.
image_gen_detailed_description: >-
  Horizontal stacked bar chart, one bar per model, with five bars total. X-axis: 'fraction of 100 MICs', range 0.0 to 1.0,
  ticks every 0.2. Y-axis: model names listed top to bottom in this order: 'Claude Haiku 4.5', 'GPT-4o-mini', 'Mistral Small
  24B', 'Qwen 2.5 7B', 'Llama 3.1 8B'. Each bar is divided into three coloured segments: Y = 0 (red, leftmost) - fraction
  5/100 = 0.05 for Claude; 5/100 = 0.05 for GPT-4o-mini; 7/100 = 0.07 for Mistral; 16/100 = 0.16 for Qwen; 20/100 = 0.20 for
  Llama. Y = 1 (yellow, middle) - fraction 21/100 = 0.21 for Claude; 20/100 = 0.20 for GPT-4o-mini; 19/100 = 0.19 for Mistral;
  17/100 = 0.17 for Qwen; 26/100 = 0.26 for Llama. Y = 2 (green, rightmost) - fraction 74/100 = 0.74 for Claude; 75/100 =
  0.75 for GPT-4o-mini; 74/100 = 0.74 for Mistral; 67/100 = 0.67 for Qwen; 54/100 = 0.54 for Llama. Each bar has a thin black
  outline. Legend in the upper right: three small squares labelled 'Y = 0 (near-random)', 'Y = 1 (partially coherent)', 'Y
  = 2 (highly coherent)'. Title above chart: 'Ordinal coherence distribution per model across 100 MICs'. Sans-serif font,
  white background. Aspect ratio 16:9.
aspect_ratio: '16:9'
summary: >-
  Stacked bars showing how each model distributes across the three coherence grades.
figure_path: figures/fig3_v0.pdf

--- Item 4 ---
id: fig4
figure_type: data
title: Stress Test of Coherence Scoring
caption: >-
  Stress test on Qwen 2.5 7B: seed-only accuracy rises by +0.07 on average under artificial internal-inconsistency, while
  the GRM-estimated theta drops by -1.382 across three random seeds with standard deviation 0.007. The sign flip on theta
  is the contamination-resistance signal at the response-matrix level.
image_gen_detailed_description: >-
  Grouped bar chart with two panels side by side, sharing the same X-axis categories. Categories on X-axis: 'Seed 0', 'Seed
  1', 'Seed 42'. Left panel title 'Seed-only accuracy': Two bars per category, side by side. Clean (light blue): Seed 0 =
  0.78, Seed 1 = 0.78, Seed 42 = 0.78. Stressed (dark blue): Seed 0 = 0.85, Seed 1 = 0.84, Seed 42 = 0.86. Y-axis range 0.70
  to 0.90 with ticks every 0.05. Annotation arrow between Clean and Stressed at Seed 0 labelled '+0.07'. Right panel title
  'theta (GRM-estimated)': Two bars per category, side by side. Clean (light green): Seed 0 = -0.001, Seed 1 = -0.001, Seed
  42 = -0.001. Stressed (dark red): Seed 0 = -1.389, Seed 1 = -1.387, Seed 42 = -1.373. Y-axis range -1.5 to 0.5 with ticks
  every 0.5. Annotation arrow between Clean and Stressed at Seed 0 labelled '-1.382 (mean across seeds, std = 0.007)'. Both
  panels have white background, light grey grid lines, sans-serif font. Aspect ratio 16:9 for side-by-side display.
aspect_ratio: '16:9'
summary: >-
  Paired bars: static accuracy rises under stress, theta drops under stress, across three seeds.
figure_path: figures/fig4_v0.pdf
</available_figures>

<figure_requirements>
CRITICAL: Include ALL figures from <available_figures>. No exceptions.

- Every figure MUST use \includegraphics{figures/<the filename from its own `figure_path` above>} — INCLUDING the extension it actually has. Data figures are delivered as `.pdf` (vector, so their axis labels stay sharp) and concept figures as `.jpg`. Writing `.jpg` for a `.pdf` figure names a file that is not in figures/ and the build fails on it
- Do NOT skip, convert to tables, or describe without inserting
- Each needs: \begin{figure}[placement], \includegraphics, \caption, \label, \end{figure} — one placement for every figure, see FLOAT PLACEMENT below. Constrain every \includegraphics with `width=\linewidth,height=0.85\textheight,keepaspectratio`. The height is a LAST RESORT, not the usual limit: it exists so a very tall figure cannot overrun the page, and at 0.4 it bound almost everything instead — a 1:1 confusion matrix printed at 50.9% and its 11 pt axis labels reached the page at 5.6 pt, below what any venue accepts. At 0.85 every ratio the paper prompt prescribes (21:9, 16:9, 4:3, 1:1) is limited by WIDTH, prints at 93% and keeps its text above 10 pt. Use exactly these option keys — `max height=` is NOT valid LaTeX
- Use the `caption` field from each figure for \caption{...} — do NOT invent new captions
- Place figures where their [FIGURE:fig_id] markers appear in paper_text
- VERIFICATION: paper.tex MUST have exact same number of \includegraphics as <available_figures>
- Do NOT generate new figure images (no matplotlib, no PIL, no image generation). Use ONLY the pre-generated figures from <available_figures>. They were already created by a previous pipeline step.

FLOAT PLACEMENT: every figure gets \begin{figure}[!htbp]. Measured, not chosen:
the document the aii-paper-to-latex skill sets up is ONE column, so `figure*` is
exactly as wide as `figure` (469.76pt either way) and gains nothing; and any
placement asking for a page TOP — `[!t]`, `[!tbp]` — floated the hero diagram above
the paper's own title on page 1, while `[!htbp]` did not. `[!htbp]` also gives LaTeX
four options, so a float can never be deferred to the end of the document, which one
option alone risks. Where the hero ENDS UP is decided by its [FIGURE:] marker in
paper_text, which is already placed near the end of the Introduction — preserve it.
</figure_requirements>

<artifact_links>
The paper_text contains \footnote{Code: \url{...}} references linking to artifact source code
on GitHub. Include \usepackage{hyperref} and \usepackage{url}.
Preserve these exactly as-is — do not remove, rewrite, or convert them to plain text.
The URLs will not resolve yet (the repo is deployed after compilation) — do NOT try to verify or fix them.
</artifact_links>

<headings>
NEVER use inline math (``$...$``) inside ``\section{...}`` / ``\subsection{...}`` / ``\subsubsection{...}`` arguments — hyperref's bookmark builder errors out (``Token not allowed in a PDF string``) and the PDF outline breaks. If a section heading needs a math-looking term, use the text equivalent (``d star`` not ``$d^*$``, ``alpha-equivalent`` not ``$\alpha$-equivalent``) or wrap it in ``\texorpdfstring{$math$}{plain}``. Inline math inside body paragraphs is fine.
</headings>

<writing_register>
Write in the register of the field's best papers (the style exemplars block below, when the writing step saved any), not in the register of a language
model. Four things are measured on the finished draft, and a draft outside them is sent back with
the numbers:
- Never use: delve, underscore, showcase, intricate, pivotal, realm, commendable, meticulous, tapestry, garner, multifaceted, it is worth noting, plays a crucial role, not only ... but also. These are 10 to 30 times more frequent in machine-written abstracts than in
  human ones, and reviewers read them as such.
- Em dashes: at most 3 per 1,000 words. Use a comma, a colon or a full stop.
- Sentence rhythm: mix short and long sentences. An interquartile range of sentence length under
  8 words reads as machine-written.
- Hedging: at most 15 hedges (may, likely, suggests, appears) per 1,000
  words. State what the evidence supports plainly; hedge where it is thin, not everywhere.
Style never changes substance: numbers, claims, citations and figure markers stay exactly as the
evidence gives them. The user's original request (delivered as a separate message) overrides all
of this wherever the two conflict.
</writing_register>

<style_exemplars>
The draft in <paper_text> was written to the register of these passages, which the writing step
saved as style_exemplars.md. Any prose you add or change here (captions, transitions, cuts
for the page limit) stays in that register.

# Style Exemplars

The paper sits at the intersection of (a) LLM evaluation methodology (HELM lineage), (b) IRT-based psychometrics for LLMs (tinyBenchmarks, Lost in Benchmarks, ATLAS), and (c) dynamic / contamination-aware benchmarking (LiveBench). The four exemplars below come from those three subfields.

## One-line observations on style

- **Sentence length:** Median ~22 words, IQR ~12–18. Mix of short sentences (5–10 words) used for stating findings and long sentences (25–35 words) used for setup and definitions. Few one-word sentences.
- **Hedging:** Moderate (~10 hedges per 1k words). Phrases like "to the extent possible", "to a first approximation", "we find". Used in scope statements and limitations, not in headline claims.
- **First person:** Plural "we" throughout for multi-author work, even in single-author experiments. Avoid "the authors". Third person preferred for prior-work attribution ("Polo et al. report …").
- **Citation density:** Very high. 30–60 inline citations per paper; each substantive claim is backed by 1–3 citations. Bibliographic style is parenthetical (Author, Year) inline, alphabetical in references.
- **Voice:** Active. Methods verbs in present tense ("we fit", "we measure", "we generate"). Results in past tense ("the model achieved", "we found").

These register cues should be honoured throughout the draft. The verbatim passages below are *style samples only* — none of their content is reused.

---

## Exemplar 1 — HELM (Liang et al. 2022, TMLR)

Title: Holistic Evaluation of Language Models
Year: 2022 (revised 2023)
URL: https://arxiv.org/abs/2211.09110

### Abstract (excerpt)
"Language models (LMs) are becoming the foundation for almost all major language technologies, but their capabilities, limitations, and risks are not well understood. We present Holistic Evaluation of Language Models (HELM) to improve the transparency of language models. First, we taxonomize the vast space of potential scenarios (i.e. use cases) and metrics (i.e. desiderata) that are of interest for LMs. … We measure 7 metrics (accuracy, calibration, robustness, fairness, bias, toxicity, and efficiency) for each of 16 core scenarios to the extent possible (87.5% of the time), ensuring that metrics beyond accuracy don't fall to the wayside, and that trade-offs across models and metrics are clearly exposed. … Our evaluation surfaces 25 top-level findings concerning the interplay between different scenarios, metrics, and models."

### Introduction, paragraph 1 (verbatim)
"Benchmarks orient AI. They encode values and priorities (Ethayarajh & Jurafsky, 2020; Birhane et al., 2022) that specify directions for the AI community to improve upon (Spärck Jones & Galliers, 1995; Spärck Jones, 2005; Kiela et al., 2021; Bowman & Dahl, 2021; Raji et al., 2021). When implemented and interpreted appropriately, they enable the broader community to better understand AI technology and influence its trajectory. In recent years, the AI technology that has arguably advanced the most is foundation models (Bommasani et al., 2021), headlined by the rise of language models (LMs; Peters et al., 2018; Devlin et al., 2019; Brown et al., 2020; Rae et al., 2021; Chowdhery et al., 2022). At its core, a language model is a box that takes in text and generates text (Figure 1). Despite their simplicity, when these models are trained on broad data at immense scale, they can be adapted (e.g. prompted or fine-tuned) to myriad downstream scenarios. Yet the immense surface of model capabilities, limitations, and risks remains poorly understood. The rapid development, rising impact, and inadequate understanding demand that we benchmark language models holistically."

### Results / finding paragraph (excerpt)
"Prior to HELM, models on average were evaluated on just 17.9% of the core HELM scenarios, with some prominent models not sharing a single scenario in common. We improve this to 96.0%: now all 30 models have been densely benchmarked on a set of core scenarios and metrics under standardized conditions."

### Discussion / limitations (excerpt)
"We intend for HELM to be a living benchmark for the community, continuously updated with new scenarios, metrics, and models."

---

## Exemplar 2 — tinyBenchmarks (Polo et al. 2024, ICML)

Title: tinyBenchmarks: evaluating LLMs with fewer examples
Year: 2024
URL: https://arxiv.org/abs/2402.14992

### Abstract (verbatim)
"The versatility of large language models (LLMs) led to the creation of diverse benchmarks that thoroughly test a variety of language models' abilities. These benchmarks consist of tens of thousands of examples making evaluation of LLMs very expensive. In this paper, we investigate strategies to reduce the number of evaluations needed to assess the performance of an LLM on several key benchmarks. For example, we show that to accurately estimate the performance of an LLM on MMLU, a popular multiple-choice QA benchmark consisting of 14K examples, it is sufficient to evaluate this LLM on 100 curated examples. We release evaluation tools and tiny versions of popular benchmarks: Open LLM Leaderboard, MMLU, HELM, and AlpacaEval 2.0. Our empirical analysis demonstrates that these tools and tiny benchmarks are sufficient to reliably and efficiently reproduce the original evaluation results."

### Introduction, paragraph 1 (verbatim)
"Large Language Models (LLMs) have demonstrated remarkable abilities to solve a diverse range of tasks (Brown et al., 2020). Quantifying these abilities and comparing different LLMs became a challenge that led to the development of several key benchmarks, e.g., MMLU (Hendrycks et al., 2020), Open LLM Leaderboard (Beeching et al., 2023), HELM (Liang et al., 2022), and AlpacaEval (Li et al., 2023). These benchmarks are comprised of hundreds or thousands of examples, making the evaluation of modern LLMs with billions of parameters computationally, environmentally, and financially very costly. For example, Liang et al. (2022) report that evaluating the performance of a single LLM on HELM costs over 4K GPU hours (or over $10K for APIs)."

### Results paragraph (verbatim)
"Figure 1: Estimating accuracy on MMLU (true accuracy) using 100 curated examples (predicted accuracy). IRT++, our best-performing evaluation strategy, predicts the accuracy of recent LLMs released between December 30th and January 18th within 1.9% of their true accuracy on all of MMLU (14K examples)."

### Limitations (excerpt)
"6.2 Limitations … We note three primary limitations. First, our approaches assume access to a pre-evaluated set of LLMs on the full benchmark. … Second, the effectiveness of our methods depends on the quality and diversity of the pre-evaluated LLM pool. Third, our evaluation is focused on accuracy-based metrics; other metrics (e.g., calibration, robustness, fairness) may require different strategies."

---

## Exemplar 3 — LiveBench (White et al. 2024, ICLR Spotlight)

Title: LiveBench: A Challenging, Contamination-Limited LLM Benchmark
Year: 2024 (ICLR 2025 Spotlight)
URL: https://arxiv.org/abs/2406.19314

### Abstract (verbatim)
"Test set contamination, wherein test data from a benchmark ends up in a newer model's training set, is a well-documented obstacle for fair LLM evaluation and can quickly render benchmarks obsolete. To mitigate this, many recent benchmarks crowdsource new prompts and evaluations from human or LLM judges; however, these can introduce significant biases, and break down when scoring hard questions. In this work, we introduce a new benchmark for LLMs designed to be resistant to both test set contamination and the pitfalls of LLM judging and human crowdsourcing. We release LiveBench, the first benchmark that (1) contains frequently-updated questions from recent information sources, (2) scores answers automatically according to objective ground-truth values, and (3) contains a wide variety of challenging tasks, spanning math, coding, reasoning, language, instruction following, and data analysis. … LiveBench is difficult, with top models achieving below 70% accuracy."

### Discussion excerpt (paraphrased from public-facing intro)
"Test set contamination, wherein test data from a benchmark ends up in a newer model's training set, is a well-documented obstacle for fair LLM evaluation and can quickly render benchmarks obsolete. … Questions are added and updated on a monthly basis, and we release new tasks and harder versions of tasks over time so that LiveBench can distinguish between the capabilities of LLMs as they improve in the future."

---

## Exemplar 4 — LGMT (Zhou et al. 2026, Knowledge-Based Systems)

Title: LGMT: Logic-Grounded Metamorphic Testing for Evaluating the Reasoning Reliability of LLMs
Year: 2026
URL: https://arxiv.org/abs/2605.23965

### Excerpt (from research_report.md citation)
"LGMT derives 20 FOL-grounded MRs from De Morgan / contraposition / quantifier transformations and shows models are most sensitive to symbol- and conclusion-level variations; constructs 76,298 candidate metamorphic groups; evaluates 3,091 sampled across 6 LLMs and 4 prompting strategies."

### Excerpt from abstract framing (paraphrased)
"Metamorphic relations … are derived from first-order-logic transformations … we apply them to evaluate the reasoning reliability of LLMs. … [We] find that even strong LLMs show significant inconsistency across logically equivalent perturbations …"
</style_exemplars>
FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-to-latex, aii-semscholar-bib.
TODO 2. Review <paper_text> and <available_figures>. Copy all figure images into ./figures/ in your workspace. Count figures — MUST include every one. Plan placements per section. Build `./references.bib` via aii_semscholar_bib__fetch — collect DOIs/ArXiv IDs from <paper_text> and batch-fetch all BibTeX in one call. Do NOT fabricate entries.
TODO 3. Create `./paper.tex` per aii-paper-to-latex skill's setup, write ALL sections, insert ALL figures from <available_figures>, include `./references.bib` via \bibliography. Compile to PDF per skill's process. Fix errors.
TODO 4. CRITICAL VERIFICATION: Run `grep -c 'includegraphics' paper.tex`, confirm count equals figures in <available_figures>. If not, add missing figures. Verify `./paper.pdf` was created.
TODO 5. VISUAL REVIEW: Write Python script to convert EVERY page of paper.pdf to PNG at 150 DPI (use pdf2image or pymupdf). Then read ALL page screenshots — each page image costs ~1,600 tokens so a 15-page paper is only ~24K tokens. You MUST read every page. The ONLY exception is if all page images would not fit in your remaining context — in that case, read as many as fit and state which pages you are skipping and why. Check every page for layout issues, overlapping figures, cut-off text, bad spacing, formatting problems. Fix issues and recompile.
TODO 6. FINAL READ: Check page count (`pdfinfo paper.pdf` or pymupdf). Read entire paper.pdf — check for missing sections, unclear explanations, inconsistencies, typos. Fix and recompile. The ONLY exception is if all pages would not fit in your remaining context — in that case, read as many pages as fit and state which pages you are skipping and why.
</todos>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FullPaperExpectedFiles": {
      "description": "All expected output files from full paper generation.",
      "properties": {
        "paper_tex_path": {
          "description": "Path to LaTeX source file. Example: 'paper.tex'",
          "title": "Paper Tex Path",
          "type": "string"
        },
        "paper_pdf_path": {
          "description": "Path to compiled PDF. Example: 'paper.pdf'",
          "title": "Paper Pdf Path",
          "type": "string"
        },
        "references_bib_path": {
          "description": "Path to BibTeX bibliography file. Example: 'references.bib'",
          "title": "References Bib Path",
          "type": "string"
        },
        "figure_paths": {
          "description": "Paths to all figure image files. Example: ['figures/fig1_v0.jpg', 'figures/fig2_v0.jpg']",
          "items": {
            "type": "string"
          },
          "title": "Figure Paths",
          "type": "array"
        }
      },
      "required": [
        "paper_tex_path",
        "paper_pdf_path",
        "references_bib_path",
        "figure_paths"
      ],
      "title": "FullPaperExpectedFiles",
      "type": "object"
    }
  },
  "description": "Full paper \u2014 structured output from paper generation.",
  "properties": {
    "title": {
      "description": "Paper title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated paper: sections written, figures included, compilation status",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/FullPaperExpectedFiles",
      "description": "All output files you created. Must include paper.tex, paper.pdf, references.bib, and paths to all figure files."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "FullPaper",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-09-05 17:03:36 UTC

```
Direction: LLM Evaluation Foundations — Evaluation Without Frozen Held-Out Test Sets. Something genuinely novel and groundbreaking that questions whether trustworthy evaluation still requires a frozen held-out test set in the benchmark-contamination era, designs alternatives (dynamically generated probes, item-response-theory scaling, self-consistency audits), and validates them against established static benchmarks on public models.

Ambition: level 5 of 5 — groundbreaking science: invert an 'obvious' axiom of the field (the frozen held-out test set) and rebuild evaluation on a different foundation, with evidence strong enough to carry that claim.

Reviewer: I am Percy Liang (Stanford). Calibrate from my existing papers (HELM, foundation-model evaluation). Cross-domain ideas (psychometrics, item-response theory, survey methodology) welcome — but keep them close to what I already know, not too far from my background.

Submission/Goal: a paper for NeurIPS Datasets & Benchmarks or ICLR main track. Audience: ML evaluation researchers. Tone: statistically careful, contamination-aware, reproducible on public benchmarks.
```

### [3] SKILL-INPUT — aii-paper-to-latex · 2026-09-05 17:03:56 UTC

The agent loaded the **aii-paper-to-latex** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-to-latex
description: "Assembles and compiles a LaTeX paper into paper.pdf: documentclass and package preamble, figure floats that includegraphics pre-generated vector .pdf and .jpg files, float-placement and width rules, and the required pdflatex, bibtex, pdflatex, pdflatex run sequence. Use whenever pre-written text and pre-generated figures must become a compiled PDF, and whenever a build misbehaves — citations printing as question marks, figures drifting to the end or above the title, shrunken axis labels, undefined references. Triggers: latex, tex, pdflatex, bibtex, natbib, includegraphics, figure float, htbp, compile or build the paper, paper.tex, paper.pdf. NOT for: writing the paper's text or deciding its structure (use aii-paper-writing), creating the figure images (aii-data-fig-gen, aii-concept-fig-gen), or fetching bibliography entries (use aii-semscholar-bib); NOT for reshaping a PDF that already exists — merging, splitting, form filling, table extraction (use anthropic-pdf)."
---

## LaTeX Paper Assembly

Assembles a research paper from paper text, pre-generated figures (vector `.pdf` for data figures, `.jpg` for concept figures) and a bibliography into a compiled PDF.

### Document Setup

```latex
\documentclass[11pt,letterpaper]{article}
\usepackage{graphicx, geometry, amsmath, hyperref, url, natbib, booktabs, xcolor, listings}
\geometry{margin=1in}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}
```

### Figure Inclusion

CRITICAL: Include ALL figures. Every figure MUST appear in the paper.

```latex
\begin{figure}[!htbp]
  \centering
  \includegraphics[width=\linewidth,height=0.85\textheight,keepaspectratio]{figures/filename.pdf}
  \caption{Descriptive caption.}
  \label{fig:label}
\end{figure}
```

Rules:
- ALWAYS `[!htbp]` — all four options, so a float can never be deferred to the end of the
  document, which `[t]` or `[h]` alone risks. Do not ask for a page TOP: `[!t]` and
  `[!tbp]` both floated a figure ABOVE the paper's own title on page 1, where `[!htbp]`
  on the same document did not. Where a figure lands is decided by where it is declared
  in the text
- Use `figure`, never `figure*`. This document class is ONE column, so `figure*` is exactly
  as wide as `figure` (469.76pt either way) and gains nothing, while restricting the float
  to a page top
- ALWAYS constrain with `width` and `keepaspectratio`. Add `height` only as a
  LAST RESORT against a very tall figure overrunning the page, and keep it
  generous — `0.85\textheight`. A tight height cap binds on ordinary figures
  and LaTeX then shrinks the TEXT with them: at `0.4\textheight` a square
  figure printed at 50.9%, putting 11 pt axis labels on the page at 5.6 pt.
  The figure generator measures legibility at the figure's OWN size, so it
  cannot see this happen
- Every figure needs `\caption`, `\label`, and a `\ref` in the text
- Do NOT convert figures to tables or describe them without inserting the image
- Do NOT skip any figures

### Compilation Process

Run each command separately (do NOT chain with `&&` — pdflatex often exits non-zero on warnings, which would skip bibtex and leave citations as `??`):

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

All four commands are required. Skipping bibtex causes `??` in all citations.
Fix any errors between runs. Verify `./paper.pdf` was created.

### Output Files

- `./paper.tex` — LaTeX source
- `./references.bib` — bibliography file
- `./paper.pdf` — compiled PDF
- `./figures/` — all figure images (pre-generated, copied into workspace). Data
  figures are `.pdf` (vector — LaTeX renders their text at page resolution, which
  is what keeps axis labels sharp in print); concept figures are `.jpg`. Use each
  file's OWN extension in `\includegraphics`; there is no conversion step.
````

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-09-05 17:03:58 UTC

The agent loaded the **aii-semscholar-bib** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-semscholar-bib
description: "Fetches real BibTeX entries in one batch from Semantic Scholar by DOI, ArXiv ID or title via aii_semscholar_bib__fetch, normalises citation keys to AuthorYYYY, injects DOIs, and writes the result into references.bib, with a mandatory web-search fallback for anything not found. ALWAYS use whenever a bibliography, reference list or .bib file is being built or extended, and whenever a citation needs a verified entry instead of an invented one — never hand-write BibTeX first. Triggers: bibliography, references.bib, bibtex, citation key, DOI, arXiv id, Semantic Scholar, reference list, cite these papers, natbib entries. NOT for: writing the text around the citations (use aii-paper-writing), running bibtex and compiling (use aii-paper-to-latex), judging whether cited work supports the claims (use amg-paper-verification), or open-ended literature search and PDF mining (use aii-web-tools)."
---

## Tool: `aii_semscholar_bib__fetch`

Batch-fetch BibTeX entries from Semantic Scholar. Pass all references in a single call — the tool handles batching internally.

### How it works

1. **DOI/ArXiv refs** → batched into POST /paper/batch calls (up to 500 per API call, auto-chunked)
2. **Title-only refs** → individual GET /paper/search/match (1s delay between)
3. **Post-process** → fix entry type, fix citation key (AuthorYYYY), inject DOI

The ability server runs a single worker (`max_threads: 1`). Multiple concurrent tool calls are queued — each runs independently (no cross-request aggregation). Batching happens within each request.

### Input format

```json
{
  "references": [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
    {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
    {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
  ]
}
```

Each reference object can have:
- `doi` — DOI string (ArXiv DOIs like `10.48550/arXiv.XXXX.XXXXX` auto-convert to ArXiv IDs)
- `arxiv` — ArXiv ID (e.g. `"2305.14325"`)
- `title` — Paper title (used for search/match when no DOI/ArXiv)
- `author` — First author last name (for cleaner citation key)
- `year` — Publication year (int, for citation key)

At least one of `doi`, `arxiv`, or `title` is required per reference.

### Output format

```json
{
  "success": true,
  "bib_text": "@inproceedings{Vaswani2017, ...}\n\n@article{Wei2022, ...}",
  "total": 3,
  "found": 3,
  "failed_count": 0,
  "entries": [{"citation_key": "Vaswani2017", "bibtex": "...", "title": "...", "doi": "...", "arxiv": ""}],
  "failed": []
}
```

### Workflow

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in **one call**
3. Save `bib_text` from the response to your `references.bib` file
4. Check `failed` — for any missed papers, follow the **fallback procedure** below

### Fallback for failed references (MANDATORY)

NEVER fabricate BibTeX. For each failed reference:
1. **WebSearch** for `"Title" author year` (try `site:arxiv.org` too)
2. **WebFetch** the paper page → extract title, authors, year, venue, DOI/ArXiv ID
3. If DOI/ArXiv found → retry `aii_semscholar_bib__fetch` with it
4. Last resort: write BibTeX by hand using **only verified info from the actual paper page**

---

### CLI (for manual use / debugging)

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-semscholar-bib" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --refs '[
  {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
  {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
  {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
]'
```

`--json, -j` — output raw JSON instead of .bib text

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [5] SYSTEM-USER prompt · 2026-09-05 17:25:46 UTC

```
STOP. You have reached the maximum number of turns.

Do NOT use any more tools. Finish what you are doing and provide your final output NOW.

Use whatever information you have gathered so far to produce the best response possible.
```

### [6] SYSTEM-USER prompt · 2026-09-05 17:35:57 UTC

````
<task>
Create a publication-ready top-conference LaTeX paper with BibTeX from <paper_text> and <available_figures>, compile to PDF.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<paper_text>
title: >-
  M-IRT: Reference-Free LLM Evaluation via Samejima Graded Response Models on Dynamically Generated Metamorphic Item Clusters
abstract: >-
  Static LLM benchmarks with frozen held-out answer keys have become suspect as language models are trained on increasingly
  large fractions of the public web [2, 3, 18]. We ask a sharper question: can reasoning capability be measured when no answer
  key is trusted to be free of contamination? We introduce Metamorphic Item Response Theory (M-IRT), a reference-free framework
  that scores an LLM's internal logical coherence across dynamically generated Metamorphic Item Clusters (MICs). Each cluster
  carries four variants (seed, paraphrase, negation, and inverse or contrapositive) bound by a relational invariant whose
  oracle is derivable from the question text alone, so no absolute label exists. An ordinal coherence grade per (model, cluster)
  cell feeds a Samejima Graded Response Model (GRM) [6] fit by marginal maximum likelihood, recovering a per-model latent
  ability θ and per-item discrimination/difficulty. Across five public LLMs and 100 MICs spanning propositional syllogisms
  and grade-school arithmetic, the θ ranking correlates with published MMLU accuracy at Pearson r = 0.975 and exceeds three
  simpler binary consistency metrics computed on the same clusters. A stress test in which a model's seed response is forced
  to the oracle on 30% of clusters confirms that coherence grading penalises internally inconsistent response profiles. The
  pipeline is reproducible for under $0.05 in three minutes. The headline is methodological: the GRM scaling layer, the dynamic
  cluster generator, and a clearly scoped protocol for the natural-contamination experiment (system-prompt injection plus
  re-query) that the framework's hypothesis requires.
paper_text: |+
  ## 1 Introduction

  Benchmarks orient AI. They specify what is worth measuring and, in doing so, shape what is worth improving [1]. For language models, this role has been carried by fixed, curated test sets: a frozen set of items with a frozen answer key, run against a frozen evaluation harness. HELM [1] argued that the field needed broader coverage and multi-metric measurement, not that the frozen-test-set axiom itself was at risk. Six years on, that axiom is breaking.

  The proximate cause is contamination. As LLM training corpora have grown to include large fractions of the public web, fixed benchmark items and their gold labels have leaked into pre-training data. Deng et al. [2] report that GPT-4 verbatim fills in 57% of multiple-choice options masked from MMLU and ChatGPT 52%; the same pattern holds across HELM, GSM8K, and HumanEval. Balloccu et al. [3] document evaluation malpractice that effectively rewards memorisation, and Xu et al. [18] survey a four-level taxonomy of contamination (semantic, information, data, label) and matching-based versus comparison-based detection. Dynamic benchmarks that refresh items from recent sources, such as LiveBench [4], are one mitigation, but they still rely on a trusted answer key and so remain reference-dependent.

  This paper asks whether the answer key itself is dispensable. If we can construct a cluster of items whose correct answers are logically bound to one another, without specifying any absolute answer, then the only thing we need to measure is whether a model behaves consistently across that cluster. We call such a cluster a *Metamorphic Item Cluster (MIC)*, drawing the term from metamorphic testing [5, 22], where a metamorphic relation specifies how an output should transform when an input is perturbed, rather than what the output should equal. The same idea, applied to logical reasoning, says: if you can answer *P* correctly, then you should answer *not P* by the flipped label, the paraphrase by the same label, and the inverse (or contrapositive) by the same label. Logical coherence across the cluster is a graded observable; we never have to know whether the cluster's seed answer is "True" or "False" or "24".

  Logical coherence is not a measurement of accuracy, but it is a measurement of capability. A model that reasons tends to maintain coherence; a model that memorises a surface form breaks coherence the moment a paraphrase, negation, or inverse is applied. Coherence therefore satisfies a property no static benchmark can offer: it is invariant to having seen the answer key, because no answer key exists. If a model has memorised the answer to "All A are B; all B are C. Therefore all A are C", it has not memorised the answer to "Is it NOT the case that all A are C?" and it has not memorised the answer to the paraphrase using a different vocabulary.

  We turn coherence into a latent ability estimate by combining MICs with a Graded Response Model (GRM) [6]. The GRM is the canonical polytomous extension of item response theory, used in educational testing to score essay responses on ordered rubrics and recently applied to LLM-judge reliability [7]. Our application differs: the response variable is not a Likert rating or a correctness call, but the count of MIC variants a model answered coherently. Mapping this count to a 3-point ordinal scale (0/1/2) yields the response matrix that the GRM fits. From a fitted GRM we extract a per-model latent ability θ and per-item discrimination and difficulty parameters, in the standard IRT fashion [6, 8, 9, 10].

  A parallel literature (Elazar et al. [11], BECEL [13], Liu et al. [14], Novikova et al. [15], ConsistencyGate [16], Musawi and Lu [17]) uses logical consistency of an LLM's outputs as a reference-free evaluation signal, without IRT. M-IRT is distinct from this thread in three concrete ways. *First*, the response variable is polytomous: a 3-point ordinal grade driven by how many of the four variants a model answered coherently, rather than a binary invariance indicator. The polytomous GRM produces an interval-scaled θ whose Pearson correlation with MMLU (r = 0.975) exceeds the binary consistency metrics computed on the same clusters (paraphrase agreement: r = 0.905; negation invariance: r = 0.826). *Second*, the clusters are generated dynamically per evaluation session, so no cluster member can appear in any prior training corpus; the consistency literature operates on fixed prompt sets. *Third*, the target of evaluation is contamination-resistance as a property of the *response profile*: M-IRT measures whether a model's seed-only accuracy can rise while θ stays within its posterior standard error when the seed oracle is injected, which distinguishes a memorisation event from a capability gain. The consistency literature targets robustness, which is the same property under a different name and a different statistical instrument.

  Concretely, we generate 100 MICs (50 propositional syllogisms across 12 templates; 50 arithmetic word problems across 12 templates) and query five public LLMs on each of the four variants, for 2,000 calls completed in 167 seconds at $0.05 cumulative spend. The resulting θ values rank the models in close agreement with their published MMLU (Spearman ρ = 0.90; Kendall τ = 0.80) and HELM (ρ = 0.90; τ = 0.80) accuracy, despite never consulting those benchmarks during evaluation. We compare θ against simpler binary consistency metrics on the same clusters and find the metrics tie on rank statistics at this sample size (Spearman ρ = 0.90 across all of θ, paraphrase agreement, seed accuracy, and a composite) but separate on Pearson r, where θ (0.975) exceeds paraphrase agreement (0.905), seed accuracy (0.900), negation invariance (0.826), and the composite (0.855). An artificial stress test in which a model's seed response is forced to the oracle on 30% of clusters while the metamorphic variants are left untouched raises static seed accuracy by +0.07 and drops θ by −1.38, confirming that coherence grading penalises internal inconsistency but not establishing robustness to realistic memorisation. The natural-contamination protocol (system-prompt injection of the seed oracle followed by re-query on all four variants) is laid out in Section 6 as the test that would establish memorisation-resistance.

  **Summary of contributions.**

  - (i) A reference-free evaluation framework (M-IRT) that produces MICs dynamically, derives ordinal coherence grades from relational invariants, and fits a Samejima GRM to recover a per-model latent ability θ with no ground-truth answer key in the loop.
  - (ii) A reproducible pipeline of 100 MICs across two reasoning domains and a panel of five public models, completed end-to-end for under $0.05 and ~3 minutes, with an explicit ablation showing that θ's Pearson r with MMLU (0.975) exceeds three binary consistency metrics on the same clusters and that the metrics tie on Spearman ρ and Kendall τ at this sample size.
  - (iii) An artificial stress test that confirms coherence grading penalises internal inconsistency (Δstatic = +0.07, Δθ = −1.38), and a clearly scoped protocol (system-prompt injection of the seed oracle followed by re-query on all four variants) for the natural-contamination experiment the framework's hypothesis demands.

  [FIGURE:fig1]

  ## 2 Related Work

  **Holistic and multi-metric evaluation.** HELM [1] is the reference point for multi-metric LLM evaluation: a top-down taxonomy of scenarios and metrics applied to many models under standardised conditions. M-IRT inherits HELM's emphasis on standardised conditions and full-result transparency, but relaxes the assumption that the same items must be used for every model. Each model sees a freshly generated MIC, which removes the contamination vector HELM's frozen scenarios cannot eliminate.

  **Item response theory for LLM benchmarks.** Three recent works apply IRT to LLM evaluation. tinyBenchmarks [8] shows that 100 carefully chosen MMLU examples can reproduce full-benchmark accuracy within 1.9% MAE using a generalised performance-IRT estimator. Lost in Benchmarks [9] introduces PSN-IRT, a pseudo-siamese network for 4PL neural calibration trained end-to-end on 11 benchmarks (41,871 items) and reports stronger alignment with human preference than raw items. ATLAS [10] applies computerized adaptive testing to a calibrated bank of 3,000+ LLMs across five benchmarks, achieving MAE 0.157 on HellaSwag with 41 items. All three operate on *static* items with *known correct answers* and are therefore reference-dependent. M-IRT shares the GRM machinery with the LLM-judge reliability line [7] but replaces the correctness response with a coherence response, sidestepping both the calibration bank and the answer key.

  **Consistency as a research thread.** A parallel literature proposes logical consistency of an LLM's outputs as a reference-free evaluation signal, without using IRT. Elazar et al. [11] introduced the foundational definition: "the invariance of [a model's] behaviour under meaning-preserving alternations in its input", instantiated in ParaRel (328 paraphrases × 38 relations) and shown to be low across pretrained LMs. Jang, Kim, Lee, and Lukasiewicz [12] operationalised negational, symmetric, transitive, and additive consistency in BECEL across six transformer LMs and 21 tasks. Jang and Lukasiewicz [13] extended the framework to ChatGPT and GPT-4. Liu et al. [14] study logical preference consistency (negation, transitivity, commutativity) and report Spearman ρ = 0.98 (p = 0.000) between transitivity and self-agreement on NovelEval. Novikova et al. [15] survey the consistency literature and classify the twelve categories that have appeared. ConsistencyGate [16] applies self-consistency as a write-time admission gate to suppress memory contamination in LLM agents. Musawi and Lu [17] propose "contamination resistance" as an evaluation paradigm and instantiate it with a Caesar-cipher benchmark whose shift varies per instance.

  M-IRT is distinct from this thread in three concrete ways. *First*, the response variable is polytomous: a 3-point ordinal grade driven by how many of the four variants a model answered coherently, rather than a binary invariance indicator. The polytomous GRM produces an interval-scaled θ whose Pearson correlation with MMLU (0.975) exceeds the binary consistency metrics computed on the same clusters (paraphrase agreement: 0.905; negation invariance: 0.826), and a posterior standard error on θ that the binary indicators do not provide. *Second*, the clusters are generated dynamically per evaluation session, so no cluster member can appear in any prior training corpus; the consistency literature operates on fixed prompt sets. *Third*, the target of evaluation is contamination-resistance as a property of the *response profile*: M-IRT measures whether a contaminated model's seed-only accuracy can rise while θ stays within its posterior standard error when the seed oracle is injected, which distinguishes a memorisation event from a capability gain. The consistency literature targets robustness, namely whether paraphrase and negation invariance is preserved across perturbations, which is the same property under a different name and a different statistical instrument.

  **Contamination detection.** Deng et al. [2] introduce TS-Guessing, which masks a multiple-choice option and checks verbatim fill-in. Xu et al. [18] survey a four-level contamination taxonomy (semantic / information / data / label) and matching-based versus comparison-based detection. These works *detect* contamination after the fact; M-IRT is *immune* to label-level contamination because no label exists. The framework is not, however, immune to all contamination: a model that memorises the underlying *logical form* (e.g., the de Morgan identity) would still answer all four variants coherently and would receive a high θ, which is the correct outcome (the model has internalised a logical rule) but not a contamination-resistance result. The natural-contamination protocol in Section 4.6 is the test that distinguishes these cases.

  **Contamination-limited dynamic benchmarks.** LiveBench [4] refreshes items monthly from competitions, arXiv, and news. M-IRT is complementary: LiveBench's items still need an answer key, whereas MICs do not. The two can be combined into a dynamic benchmark whose scoring is by logical coherence rather than answer match.

  **Metamorphic testing for LLMs.** Chen et al. [5] define metamorphic relations (MRs) as input-output relations used to verify programs in lieu of oracles. LLMORPH [19] catalogues 191 NLP MRs across 24 tasks and runs 561,267 test executions, flagging MRs 9, 142, 154 as high-failure-low-false-positive. LGMT [20] derives 20 first-order-logic-grounded MRs (De Morgan, contraposition, quantifier shifts) and shows models are most sensitive to symbol- and conclusion-level variation. M-IRT adopts LGMT's logical perturbation set and uses a smaller but sufficient subset (paraphrase, negation, inverse / contrapositive) within each cluster.

  **Polytomous IRT in education.** Samejima's original GRM [6] estimates ordered-category responses with per-category thresholds, and is the foundation of M-IRT's response model. Choi et al. [7] apply the GRM to LLM-judge reliability and recommend priors (θ ~ N(0, 1), α ~ LogNormal(0, 0.5), β_k ~ N(0, 1) with ordering) that we adopt in our Bayesian-GRM future work.

  ## 3 Preliminaries

  **Notation.** For a panel of *M* LLMs and a set of *I* Metamorphic Item Clusters, each cluster contains four variants indexed by role *r* ∈ {seed, paraphrase, negation, inverse / contrapositive}. The cluster *i* carries relational invariants that bind the four oracle answers $\mathbf{a}_i = (a_{i,1}, \ldots, a_{i,4})$ without specifying an absolute label for any item. For logic, the negation variant's oracle is the Boolean complement of the seed's; for arithmetic, the negation variant's oracle is the fixed label "NO" (derived from the question text alone, without computing the seed's numeric answer), and the inverse variant's oracle is a quantity that appears explicitly in the seed's question text.

  **Graded Response Model.** Following Samejima [6], the probability that a model with latent ability θ produces a response of category $k \in \{0, 1, \ldots, K-1\}$ on item *i* is
  $$P(Y_i \geq k \mid \theta) = \frac{1}{1 + \exp(-\alpha_i(\theta - \beta_{i,k}))},$$
  where $\alpha_i > 0$ is the discrimination of item *i*, and $\beta_{i,1} < \beta_{i,2} < \ldots$ are the ordered category boundaries. The category probability is $P(Y_i = k \mid \theta) = P(Y_i \geq k \mid \theta) - P(Y_i \geq k+1 \mid \theta)$. Parameters are fit by marginal maximum likelihood using Gauss-Hermite quadrature on θ.

  **Coherence response.** For a (model, cluster) pair, let $c_{mi}$ denote the count of the four variants on which the model's response matches the role-appropriate oracle. We map $c_{mi}$ to an ordinal response
  $$Y_{mi} = \begin{cases} 0 & c_{mi} \in \{0, 1\} \\ 1 & c_{mi} = 2 \\ 2 & c_{mi} \in \{3, 4\}. \end{cases}$$

  The mapping is monotone: more coherent models receive higher grades. The 3-category structure is the smallest K that distinguishes "near-random" ($Y = 0$) from "partially coherent" ($Y = 1$) from "highly coherent" ($Y = 2$). The $c = 2$ bin captures "coherent on half the variants", the smallest signal that the model is reasoning rather than guessing; the $c \geq 3$ bin captures near-full coherence; the $c \leq 1$ bin captures chance-level performance. With 5 models and 100 items we cannot stably fit a K = 4 or K = 5 model; this is a sample-size limitation, not a principled choice.

  **Metamorphic relation.** A *metamorphic relation* [5] for a reasoning task is a deterministic relation $R(\text{input}_1, \text{input}_2) \Rightarrow R'(\text{output}_1, \text{output}_2)$ that holds for any correct solver. For syllogisms, the relation "input 2 is the negation of input 1" implies the relation "output 2 is the Boolean complement of output 1". For arithmetic, the relation "input 2 asks whether the answer equals an arbitrary non-answer integer" implies the relation "output 2 is the fixed label NO", derivable from the question text alone, not from the seed's value.


  ## 4 Method: M-IRT

  The M-IRT pipeline has four stages: MIC generation, model querying, coherence scoring, and GRM fitting with validation. Figure 1 diagrams the end-to-end flow.

  ### 4.1 Metamorphic Item Cluster Generator

  The generator is deterministic given a seed. It draws on two domain generators and produces four-variant clusters \footnote{Code: \url{https://github.com/ai-inventor-papers/ai-invention-0afdfa-checking-ai-logic-without-ground-truth/tree/main/round-1/experiment-1}}.

  **Logic generator.** Twelve syllogistic templates $T_1, \ldots, T_{12}$ express the canonical valid and invalid forms, inspired by the controlled-ontology construction of PrOntoQA [21] and the negation-sensitive template design of LogicBench [22]. Each template takes noun slots *A*, *B*, *C* drawn from disjoint noun pools for the seed and the paraphrase, ensuring that paraphrase and seed never share vocabulary. A template returns a two-premise argument, a candidate conclusion, and an oracle label V (valid) or I (invalid). The four variants are:
  - *Seed:* the original syllogism with original nouns.
  - *Paraphrase:* the same argument with nouns from a disjoint pool.
  - *Negation:* the conclusion negated; oracle is the Boolean complement of the seed label, derivable from the question text alone.
  - *Contradiction* (the logic-domain equivalent of the arithmetic inverse): one premise negated; oracle flips if and only if the syllogism is *Barbara*-style (T4, T10, T12); otherwise it stays.

  **Arithmetic generator.** Twelve templates express one- and two-step word problems with named participants, named items, and integer quantities in $[2, 99]$, following the GSM8K [23] and MAWPS [24] constructions. Paraphrase substitutes items from a disjoint pool and may rename participants. The negation variant asks "Is the answer to this problem equal to *wrong*?", where *wrong* is an arbitrary non-answer integer (a different *wrong* per cluster); the oracle is the fixed label "NO", derivable from the question text alone without solving the seed. The inverse variant asks "What was the original starting quantity (the first number mentioned)?"; the oracle is a quantity that appears explicitly in the seed's question text, also derivable without solving the seed.

  The two generators together emit 50 logic clusters and 50 arithmetic clusters, for 100 clusters per evaluation session . Each cluster carries an oracle answer, a difficulty hint (medium / hard), and a relational-invariant table that the scorer uses to evaluate the negation and inverse variants. Two evaluation sessions run with different seeds produce disjoint clusters, so the contamination surface for any single MIC is the single session that ran it.

  ### 4.2 Model Querying

  We evaluate five public LLMs via the OpenRouter chat-completion API: GPT-4o-mini, Claude Haiku 4.5, Llama 3.1 8B Instruct, Qwen 2.5 7B Instruct, and Mistral Small 24B Instruct 2501. Each model is presented with each of the 400 variant questions (100 clusters × 4 variants) in a single, zero-shot prompt: "Answer with V or I." for logic, or with the integer answer for arithmetic. We run with concurrency 10 and a global 12 rpm cap, completing all 2,000 calls in 167 seconds at $0.048 cumulative spend . No model is fine-tuned or prompted with worked examples; the prompt template is identical across models.

  ### 4.3 Ordinal Coherence Scoring

  For each (model, cluster) pair, we parse each variant's response into the canonical response space ({V, I} for logic, integer or {YES, NO} for arithmetic) and compare to the role-appropriate oracle. The negation variant's oracle is *not* the seed's oracle; for logic it is the Boolean complement, for arithmetic it is the fixed label "NO". The inverse variant's oracle is a quantity that appears explicitly in the seed's question text, also derivable without computing the seed. A correct response on all four variants yields a raw count of 4; we map it to the ordinal scale $Y_{mi} \in \{0, 1, 2\}$ as in Section 3. The scoring rules are deterministic and parser-level: they do not depend on a separate language model, judge, or human rater.

  ### 4.4 GRM Fitting

  We fit the GRM via `girth.grm_mml`, an open-source marginal-maximum-likelihood implementation in Python. The input is the (M × I) integer response matrix; the output is a vector of M latent abilities $\theta_j$, a vector of I discriminations $\alpha_i$, and an (I × (K − 1)) matrix of difficulty thresholds $\beta_{i,k}$. We use K = 3 categories. No priors are imposed on θ beyond the standard normal default of `girth`; discrimination and difficulty are estimated freely. The fit takes roughly three seconds on the (5 × 100) matrix .

  ### 4.5 Validation A: External-Benchmark Correlation

  To verify that θ captures reasoning rather than a proxy unrelated to capability, we correlate θ with each model's published MMLU accuracy and HELM accuracy . We report Pearson r with a 10,000-resample bootstrap 95% confidence interval, Spearman ρ, and Kendall τ. We also compute three binary consistency baselines on the same clusters (seed-only accuracy, paraphrase agreement rate, negation invariance rate, and their composite) and report the same correlations for each. The five-model panel limits the statistical resolution of all of these correlations; we treat them as point-estimate diagnostics rather than as confirmatory evidence.

  ### 4.6 Validation B: Stress Test of Coherence Scoring

  We probe the behaviour of coherence grading under a deliberately constructed internal inconsistency on Qwen 2.5 7B. On 30% of clusters (chosen by a random subset), the model's seed response is forced to the oracle, while the paraphrase, negation, and inverse responses are left at whatever the model produced. The seed oracle injection is performed at the response-matrix level: the parsed seed answer is replaced by the oracle in the per-variant flags, and the ordinal score and θ are recomputed. Under this stress, we expect:
  - Static seed-only accuracy to *increase* (the model now "knows" the seed answers).
  - The ordinal coherence score on the contaminated clusters to *not* rise by the same amount (the metamorphic variants still reflect the model's actual reasoning).
  - The GRM-fitted θ to either decrease or remain stable.

  This stress test isolates one axis of contamination-resistance (internal consistency between the seed slot and the metamorphic slots), but does not exhaust the realistic contamination scenarios. A natural-contamination protocol (system-prompt injection of the seed answer followed by re-query on all four variants) is the proper test and is laid out as future work in Section 6.


  ## 5 Experiments

  ### 5.1 Setup

  The pipeline runs in five sequential stages: cluster generation, model querying, coherence scoring, GRM fitting, and validation (validation runs two sub-experiments: the external correlation check and the stress test). Hardware: a CPU-only container with 6 GB RAM and a 4-hour CPU cap; total runtime 211 seconds. The five models are queried via the OpenRouter chat-completion interface with no system prompt, temperature 0, and a 4-token output budget. Responses are stored as one record per (model, variant) call; the fitted GRM and validation statistics are released alongside the code .

  **Terminology.** *Seed-only accuracy* is the per-model fraction of seed variants whose response matches the seed oracle; it is the metric most directly comparable to a static benchmark score. *Cluster coherence* (the 3-point ordinal $Y_{mi}$) is the count of MIC variants a model answered correctly on a given cluster, mapped to 0/1/2. *Coherence-2 rate* is the fraction of clusters on which a model achieved $Y = 2$ (the top grade, i.e., coherent on at least 3 of 4 variants). *Paraphrase agreement* is the fraction of seed-correct clusters on which the model also answered the paraphrase correctly. *Negation invariance* is the fraction of seed-correct clusters on which the model answered the negation correctly, i.e., produced the Boolean complement (logic) or "NO" (arithmetic). Both are computed on the present 100 clusters .

  ### 5.2 Latent Ability Ranking

  Table 1 reports θ and the published MMLU / HELM accuracy for each model, sorted by θ.

  **Table 1. GRM-estimated θ versus published MMLU and HELM accuracy (n = 5 models).**

  | Model | θ | MMLU | HELM |
  |---|---:|---:|---:|
  | openai/gpt-4o-mini | +3.69 | 0.820 | 0.79 |
  | anthropic/claude-haiku-4.5 | +3.56 | 0.801 | 0.78 |
  | qwen/qwen-2.5-7b-instruct | +0.07 | 0.707 | 0.69 |
  | mistralai/mistral-small-24b-instruct-2501 | −0.28 | 0.732 | 0.71 |
  | meta-llama/llama-3.1-8b-instruct | −1.37 | 0.684 | 0.65 |

  The θ ranking separates the bottom model (Llama 3.1 8B) from the rest by 1.1 θ-units and groups the top two (GPT-4o-mini, Claude Haiku 4.5) within 0.13 θ-units. Qwen 2.5 7B and Mistral Small 24B land between these clusters, at +0.07 and −0.28 respectively, which is 0.35 θ-units apart. The MMLU ranking is GPT-4o-mini > Claude Haiku 4.5 > Mistral Small 24B > Qwen 2.5 7B > Llama 3.1 8B; the θ ranking swaps Mistral Small 24B and Qwen 2.5 7B, the one inversion that bounds Spearman ρ at 0.90 and Kendall τ at 0.80 (the maximum possible given a single swap). Pearson r between θ and MMLU is +0.975 (95% bootstrap CI [0.59, 1.00]); between θ and HELM is +0.976 (CI [0.80, 1.00]) .

  The wide bootstrap CI reflects the small sample size (n = 5): the lower bound already allows r = 0.59, well below the r > 0.85 hypothesis criterion, and the upper bound is a ceiling artefact. We treat the Pearson r as a point-estimate diagnostic rather than as confirmatory evidence. The rank statistics are more interpretable at n = 5: ρ = 0.90 corresponds to exactly one rank inversion out of ten pairs, and τ = 0.80 corresponds to two discordant pairs out of ten, which is the worst-case bound given the Mistral-Qwen swap. The natural next step is to expand the panel to the n ≥ 15 the hypothesis demands and re-run; with more models, the swap between adjacent MMLU ranks would either resolve or replicate.

  [FIGURE:fig2]

  ### 5.3 Per-Model Coherence Distribution

  Across 100 clusters, the ordinal response distributions show the expected separation :

  **Table 2. Ordinal coherence distribution per model across 100 MICs.**

  | Model | Y = 0 | Y = 1 | Y = 2 | mean raw correct |
  |---|---:|---:|---:|---:|
  | anthropic/claude-haiku-4.5 | 5 | 21 | 74 | 3.21 |
  | openai/gpt-4o-mini | 5 | 20 | 75 | 3.11 |
  | mistralai/mistral-small-24b-instruct-2501 | 7 | 19 | 74 | 2.94 |
  | qwen/qwen-2.5-7b-instruct | 16 | 17 | 67 | 2.78 |
  | meta-llama/llama-3.1-8b-instruct | 20 | 26 | 54 | 2.32 |

  The top two models achieve the top grade on 74–75% of clusters and the bottom grade on only 5%, so the "near-random" tail is small. Llama 3.1 8B still achieves the top grade on 54% of clusters, indicating that even weak models solve roughly half of all clusters coherently. The signal the GRM exploits is the bottom-grade fraction, which ranges from 5% (Claude Haiku 4.5, GPT-4o-mini) to 20% (Llama 3.1 8B), a 4× spread that the GRM uses to separate the bottom model from the rest, and a similar pattern in the middle of the table where Qwen's bottom-grade fraction (16%) exceeds Mistral's (7%) despite Mistral's higher MMLU. The fact that the per-cluster ordinal grade separates models that static accuracy alone cannot (Mistral has higher seed accuracy but a worse bottom-grade fraction than Qwen) is the mechanism behind the Pearson r gap in Section 5.4.

  [FIGURE:fig3]

  ### 5.4 Comparison Against Binary Consistency Baselines

  We compute three reference-free baselines on the same clusters and report their agreement with MMLU / HELM alongside θ in Table 3.

  **Table 3. Reference-free metrics vs. MMLU and HELM accuracy on n = 5 models.**

  | Metric | Pearson r (MMLU) | Spearman ρ (MMLU) | Kendall τ (MMLU) | Pearson r (HELM) | Spearman ρ (HELM) | Kendall τ (HELM) |
  |---|---:|---:|---:|---:|---:|---:|
  | Seed-only accuracy | +0.900 | +0.900 | +0.800 | +0.941 | +0.900 | +0.800 |
  | Paraphrase agreement rate | +0.905 | +0.900 | +0.800 | +0.943 | +0.900 | +0.800 |
  | Negation invariance rate | +0.826 | +0.800 | +0.600 | +0.886 | +0.800 | +0.600 |
  | Composite (mean of PA, NI) | +0.855 | +0.900 | +0.800 | +0.909 | +0.900 | +0.800 |
  | **GRM θ** | **+0.975** | **+0.900** | **+0.800** | **+0.976** | **+0.900** | **+0.800** |

  The headline observation has two parts. *On Pearson r*, the GRM θ exceeds every binary baseline by a margin visible on the n = 5 panel: θ (0.975) > paraphrase agreement (0.905) > seed accuracy (0.900) > composite (0.855) > negation invariance (0.826) against MMLU; the same ordering holds against HELM. The reason is that θ is an interval-scaled ability score that captures *how much* better one model is than another, while a binary proportion only captures whether one model beats another. The four θ values for the four top models (3.69, 3.56, 0.07, −0.28) span 3.97 θ-units and are spread across that range, whereas the binary metrics cluster between 0.83 and 0.95, a 12-point proportion range that is more compressed. The GRM's nonlinear mapping from raw counts to latent ability produces a wider dynamic range, which Pearson r picks up but Spearman ρ does not. *On rank statistics*, all four metrics tie at Spearman ρ = 0.90 and Kendall τ = 0.80 (and at ρ = 0.80 / τ = 0.60 for negation invariance alone), because every metric in this table reflects the same single rank inversion, the Mistral-Qwen swap, and ties are broken at the metric level rather than the data level.

  This is the principled argument for the GRM framing. θ and paraphrase agreement agree on the rank ordering of the five models at this sample size, but θ captures more information than the binary proportion. With a larger panel (n ≥ 15), the rank ties should resolve and the Pearson r advantage should widen or collapse depending on whether the Mistral-Qwen swap replicates or reverses. We argue that even at the present sample size, the GRM scaling layer earns its place because it produces an interval-scaled θ with a posterior standard error, item-level discrimination and difficulty parameters that enable adaptive testing, and a per-cluster coherence grade that is the natural response variable for the natural-contamination protocol in Section 6.

  ### 5.5 Domain Decomposition and Item Parameters

  Per-domain coherence for the top model (GPT-4o-mini) shows arithmetic clusters easier than logic clusters across all five models: arithmetic mean raw correct 3.56, logic mean raw correct 2.66 . This matches the difficulty gradient we would expect from a grade-school word-problem corpus versus a categorical-syllogism corpus. The arithmetic-vs-logic gap is consistent across models and contributes to the strong MMLU / HELM correlation: published benchmark accuracy reflects a similar mix of formal-reasoning and arithmetic-reasoning items.

  The fitted discriminations $\alpha_i$ cluster at the upper and lower ends of the allowed range : 62 of the 100 items sit at the floor of approximately 0.2 (items on which the GRM could not separate models), 14 sit at the ceiling of 5.0 (the most discriminative items, including arith_0001, arith_0002, arith_0033, arith_0046, arith_0048, logic_0006, logic_0009, logic_0027, logic_0041, logic_0045), and 24 fall in between. The concentration at the bounds reflects the small panel (n = 5): with only five response vectors per item, the GRM has limited information to estimate $\alpha$ precisely, and items with all five models at the same grade get pushed to the discrimination floor. Difficulty thresholds $\beta_{i,k}$ for the most discriminative items lie at moderate θ values around −0.9, suggesting that these items discriminate primarily among the mid-ability models. Items at the discrimination floor carry no signal for θ estimation and do not distort it; we retain them for completeness rather than discard them, since dropping items would change the response matrix the GRM sees. The K = 3 ordinal mapping compresses 5 raw counts (0–4) into 3 categories; we held K = 3 in this proof-of-concept because the present sample size does not support fitting more thresholds per item without over-fitting. With a larger panel (n ≥ 15) and more items, K = 4 (splitting raw 0, 1, 2, 3, 4 into four grades) would let the GRM exploit more granularity.

  ### 5.6 Stress Test of Coherence Scoring Under Forced Internal Inconsistency

  The stress test on Qwen 2.5 7B across three random seeds (0, 1, 42) produces :

  **Table 4. Stress test on Qwen 2.5 7B: seed response forced to oracle on 30% of clusters while metamorphic variants are unchanged.**

  | Seed | Seed-only acc (clean) | Seed-only acc (stressed) | Δ seed-only | θ (clean) | θ (stressed) | Δ θ |
  |---|---:|---:|---:|---:|---:|---:|
  | 0 | 0.78 | 0.85 | +0.07 | −0.001 | −1.389 | −1.387 |
  | 1 | 0.78 | 0.84 | +0.06 | −0.001 | −1.387 | −1.385 |
  | 42 | 0.78 | 0.86 | +0.08 | −0.001 | −1.373 | −1.372 |
  | **mean** | 0.78 | 0.85 | **+0.07** | −0.001 | **−1.382** | **−1.382** |
  | std | n/a | n/a | 0.01 | n/a | n/a | 0.007 |

  Seed-only accuracy rises by +0.07 on average, but the GRM-estimated θ falls by an average of −1.382 with a standard deviation of 0.007 across the three random subsets of contaminated clusters. The stability of Δθ (the standard deviation is 1.8% of the mean) indicates that the coherence grading signal is robust to which specific clusters are chosen for contamination. Forcing the seed to be correct on a cluster where the metamorphic variants disagree with each other is exactly the profile the GRM was designed to penalise: the cluster's raw coherence count stays low, the ordinal grade stays low, and the model's θ drops as the GRM rebalances to fit a more internally inconsistent response matrix.

  We are explicit about the scope of this finding. The stress test isolates one axis of contamination (internal inconsistency between the seed slot and the metamorphic slots) and confirms that coherence scoring does penalise it. It does *not* establish that M-IRT resists realistic contamination in the broader sense. A natural-contamination protocol (injecting the seed oracle into the system prompt for a chosen subset of clusters, re-querying the model on all four variants of those clusters, and observing whether the paraphrase / negation / inverse responses become coherent as a consequence of memorisation) is the test that would establish memorisation-resistance. We leave that experiment to future work; the system-prompt injection requires a multi-turn pipeline that the present artifact does not implement. If, under natural contamination, all four variants of a contaminated cluster became coherent (because the model memorised the underlying logical form), θ would not penalise the cluster and the contamination-resistance claim would fail. This is the test that distinguishes a memorisation event from a capability gain.

  [FIGURE:fig4]


  ## 6 Discussion

  **What worked.** M-IRT produces a θ ranking that matches MMLU and HELM at Pearson r = 0.975 / 0.976 and Spearman ρ = 0.90 / Kendall τ = 0.80 on a five-model panel, despite never inspecting the model's responses against a fixed answer key. The GRM scaling layer adds value over simpler binary consistency metrics on Pearson r: θ (0.975) exceeds paraphrase agreement (0.905), seed accuracy (0.900), negation invariance (0.826), and the composite (0.855) on the same clusters. The coherence grading correctly penalises internal inconsistency in the seed-versus-metamorphic slot pattern (Δθ = −1.382, σ = 0.007, across three random subsets of contaminated clusters). The pipeline runs on commodity CPU hardware for $0.048 and three minutes per session, which is comparable to a single LLM API call's latency and orders of magnitude cheaper than full-benchmark evaluation [1, 8].

  **What did not work as hoped.** The headline Pearson r = 0.975 is supported by a wide bootstrap CI [0.59, 1.00] because the panel contains only five models; the lower bound already allows r = 0.59, well below the r > 0.85 hypothesis criterion. The middle of the θ ranking carries one rank inversion relative to MMLU (Mistral Small 24B and Qwen 2.5 7B are swapped), which is the bound on Spearman ρ at this sample size. With five models and 100 items, the GRM fit has only five degrees of freedom for θ estimation, so small per-item perturbations can produce visible θ shifts on the order of ±0.5; we mitigate by reporting Δθ (a within-model comparison) under the stress test rather than absolute θ. A practitioner using M-IRT on a small panel should report θ deltas under interventions rather than absolute θ; the principled argument for the GRM framing (item parameters, posterior SE, per-cluster grade) only stabilises with panels of n ≥ 15.

  **Limitations.**

  - *Five-model panel.* The contamination-resistance result is a within-model comparison (Δθ for one model under one intervention), so it is robust to small panels. The external-correlation result requires a larger panel to narrow the bootstrap CI and to determine whether the Mistral-Qwen rank inversion replicates or resolves. The hypothesis specifies n ≥ 15; the present artifact implements n = 5 because the OpenRouter cost ceiling and per-model licensing in the evaluation environment restricted the panel. Adding 10 to 15 more models is the single most consequential next step.
  - *Two domains.* M-IRT currently covers propositional syllogisms and grade-school arithmetic. Real reasoning also includes multi-hop reading comprehension and first-order logic; FOLIO [25] provides the closest precedent for the latter. The MMLU correlation we report therefore reflects the syllogistic + arithmetic component of reasoning capability, which is correlated with general capability but does not probe MMLU's history / law / medicine / biology domains directly. Extending the MIC bank to four reasoning domains (syllogisms, arithmetic, multi-hop reading, first-order logic) would test whether the θ ranking replicates across domains and whether the Pearson r advantage over binary metrics holds.
  - *Artificial stress test, not natural contamination.* The response-matrix-level stress test in Section 5.6 confirms that coherence grading penalises an internally inconsistent profile, but it does not test the contamination-resistance claim in the realistic sense. A natural-contamination experiment (inject the seed oracle into the system prompt, re-query all four variants, and measure whether coherence rises on the metamorphic slots) is the proper test and is listed as future work.
  - *Twelve templates per domain.* Twelve logic templates and twelve arithmetic templates cover the classical syllogistic forms and the most common word-problem operations, but they are not exhaustive. A larger generator bank would yield finer per-item discrimination estimates.
  - *Polytomous response scale.* The 0/1/2 mapping compresses 5 raw counts (0–4) into 3 categories. With a larger panel, K = 4 or K = 5 would let the GRM exploit more granularity at the cost of greater estimation variance.
  - *Reference-free for what?* M-IRT eliminates the absolute label for any item, but the relational invariants are themselves authored. A model that memorises the *form* of the metamorphic relation (e.g., that "not P" flips a V/I label) would still answer all four variants coherently and would receive a high θ. This is the correct outcome (the model has internalised a logical rule) but is not a contamination-resistance result. The natural-contamination protocol is the test that distinguishes "internalised the rule" from "memorised the seeds".

  **Future work.**

  - *Expand to n ≥ 15 models.* Add clusters at no extra query cost and re-run the analysis. The added span will give a Spearman ρ with MMLU / HELM that has a meaningful CI and supports the rank claim, and will determine whether the Mistral-Qwen swap replicates.
  - *Natural-contamination experiment.* System-prompt injection of the seed oracle for a chosen subset of clusters, re-query on all four variants, and measure whether coherence rises on the metamorphic slots or stays low. This is the test that validates or refutes the contamination-resistance claim in the realistic sense, following the masking-and-guessing paradigm of TS-Guessing [2] and the label-level injection framing of Xu et al. [18].
  - *Multi-domain M-IRT.* Add clusters for multi-hop reading comprehension (paragraph + question chain) and first-order logic (FOLIO-style annotations [25]) following the LGMT / PrOntoQA / LogicBench precedents cited.
  - *Bayesian GRM with informative priors.* Replace MML with Hamiltonian Monte Carlo and add the priors Choi et al. [7] recommend (θ ~ N(0, 1), α ~ LogNormal(0, 0.5), β_k ~ N(0, 1) with ordering), which would let M-IRT handle panels of 2–3 models without degenerate fits and produce a principled posterior standard error on θ.
  - *Adaptive MIC selection.* Once the GRM is calibrated on a larger panel, choose the next MIC from a candidate pool using maximum Fisher information on θ, in the spirit of computerized adaptive testing [10].
  - *Online contamination monitoring.* Deploy M-IRT as a recurring audit: re-run a small MIC set weekly, and alert if a model's θ moves relative to its previous θ by more than one posterior standard error. This would catch gradual contamination that static benchmarks miss.

  ## 7 Conclusion

  The frozen held-out test set is no longer the only foundation for LLM evaluation. M-IRT shows that a dynamically generated, reference-free benchmark, built from clusters of logically related items whose relational invariants are known without absolute labels, can produce a latent ability estimate that correlates with MMLU at Pearson r = 0.975 (Spearman ρ = 0.90, Kendall τ = 0.80) on the present five-model panel, a correlation that exceeds every binary consistency baseline on Pearson r and ties with them on rank statistics. The contribution is methodological rather than competitive: the cluster generator, the GRM-based coherence scoring, the protocol for the natural-contamination experiment that the hypothesis demands, and the honest accounting of where the present evidence falls short. We release code, prompts, raw responses, and fitted parameters under an MIT license .

  ## References

  [1] P. Liang et al., "Holistic Evaluation of Language Models," *Transactions on Machine Learning Research*, 2022.

  [2] C. Deng, Y. Zhao, X. Tang, M. B. Gerstein, and A. Cohan, "Investigating Data Contamination in Modern Benchmarks for Large Language Models," *NAACL*, 2024.

  [3] S. Balloccu, P. Schmidtová, M. Lango, and O. Dusek, "Leak, Cheat, Repeat: Data Contamination and Evaluation Malpractices in Closed-Source LLMs," *EACL*, 2024.

  [4] C. White et al., "LiveBench: A Challenging, Contamination-Limited LLM Benchmark," *ICLR*, 2024.

  [5] T. Y. Chen, F.-C. Kuo, H. Liu, P.-L. Poon, D. Towey, T. H. Tse, and Z. Q. Zhou, "Metamorphic Testing: A Review of Challenges and Opportunities," *ACM Computing Surveys*, vol. 51, no. 1, 2018.

  [6] F. Samejima, "Estimation of Latent Ability Using a Response Pattern of Graded Scores," *Psychometrika*, vol. 34, no. S1, pp. 1–97, 1969.

  [7] J. Choi, S. Park, C. Cho, H. Park, and B. Kim, "Diagnosing the Reliability of LLM-as-a-Judge via Item Response Theory," *ICML*, 2026.

  [8] F. M. Polo, L. Weber, L. Choshen, Y. Sun, G. Xu, and M. Yurochkin, "tinyBenchmarks: Evaluating LLMs with Fewer Examples," *ICML*, 2024.

  [9] H. Zhou et al., "Lost in Benchmarks? Rethinking Large Language Model Benchmarking with Item Response Theory," *AAAI*, 2026.

  [10] P. Li, X. Tang, S. Chen, Y. Cheng, R. Metoyer, T. Hua, and N. V. Chawla, "Adaptive Testing for LLM Evaluation: A Psychometric Alternative to Static Benchmarks," *ICML*, 2026.

  [11] Y. Elazar, N. Kassner, S. Ravfogel, A. Ravichander, E. Hovy, H. Schütze, and Y. Goldberg, "Measuring and Improving Consistency in Pretrained Language Models," *TACL*, vol. 9, pp. 1012–1031, 2021.

  [12] M. Jang, T. Kim, C. Lee, and T. Lukasiewicz, "BECEL: Benchmark for Consistency Evaluation of Language Models," *COLING*, 2022.

  [13] M. Jang and T. Lukasiewicz, "Consistency Analysis of ChatGPT," *EMNLP*, 2023.

  [14] Y. Liu, Z. Guo, T. Liang, E. Shareghi, I. Vulić, and N. Collier, "Aligning with Logic: Measuring, Evaluating and Improving Logical Preference Consistency in Large Language Models," *ICML*, 2025.

  [15] J. Novikova, C. Anderson, B. Blili-Hamelin, and S. Majumdar, "Consistency in Language Models: Current Landscape, Challenges, and Future Directions," *ICML Workshop on Reliable and Responsible Foundation Models*, 2025.

  [16] Y. Zhang and S. Li, "ConsistencyGate: Preventing Memory Contamination in LLM Agents via Self-Consistency Admission Control," *arXiv:2607.22962*, 2026.

  [17] R. Musawi and S. Lu, "Towards Contamination Resistant Benchmarks," *arXiv:2505.08389*, 2025.

  [18] C. Xu, S. Guan, D. Greene, and M.-T. Kechadi, "Benchmark Data Contamination of Large Language Models: A Survey," *arXiv:2406.04244*, 2024.

  [19] S. Cho, S. Ruberto, and V. Terragni, "Metamorphic Testing of Large Language Models for Natural Language Processing," *IEEE ICSME*, 2025.

  [20] Z. Zhou, M. Li, X. Fang, X. Zhou, W. Li, and Z. Zheng, "LGMT: Logic-Grounded Metamorphic Testing for Evaluating the Reasoning Reliability of LLMs," *Knowledge-Based Systems*, vol. 348, p. 116324, 2026.

  [21] A. Saparov and H. He, "Language Models Are Greedy Reasoners: A Systematic Formal Analysis of Chain-of-Thought," *ICLR*, 2023.

  [22] M. Parmar et al., "LogicBench: Towards Systematic Evaluation of Logical Reasoning Ability of Large Language Models," *ACL*, 2024.

  [23] K. Cobbe et al., "Training Verifiers to Solve Math Word Problems," *arXiv:2110.14168*, 2021.

  [24] R. Koncel-Kedziorski, S. Roy, A. Amini, N. Kushman, and H. Hajishirzi, "MAWPS: A Math Word Problem Repository," *NAACL*, 2016.

  [25] S. Han et al., "FOLIO: Natural Language Reasoning with First-Order Logic," *EMNLP*, 2024.

summary: >-
  M-IRT is a reference-free LLM evaluation framework that scores an LLM's internal logical coherence across dynamically generated
  Metamorphic Item Clusters and fits a Samejima Graded Response Model to recover a per-model latent ability theta and per-item
  discrimination/difficulty. Across five public LLMs and 100 MICs spanning propositional syllogisms and grade-school arithmetic,
  theta correlates with published MMLU accuracy at Pearson r = 0.975 (Spearman rho = 0.90, Kendall tau = 0.80) and exceeds
  three binary consistency baselines computed on the same clusters. An artificial stress test on Qwen 2.5 7B confirms that
  coherence grading penalises internal inconsistency (mean Delta theta = -1.382 across three random seeds). The pipeline is
  reproducible for under $0.05 in three minutes.
</paper_text>

<available_figures>
--- Item 1 ---
id: fig1
figure_type: concept
title: M-IRT Pipeline
caption: >-
  The four-stage M-IRT pipeline: deterministic MIC generation, zero-shot model querying, ordinal coherence scoring, and Samejima
  GRM fitting with two validation sub-experiments.
image_gen_detailed_description: >-
  Horizontal flow diagram, left to right, on a clean white background. Stage 1 (leftmost box, light blue): 'Cluster Generator'
  with arrow out labelled 'seed=0' showing input. Inside the box, four small icons represent the four variants per MIC: 'seed'
  (a question mark icon), 'paraphrase' (a rephrasing icon), 'negation' (a crossed-out icon), and 'contradiction/inverse' (a
  circular arrow icon). Stage 2 (second box, green): 'Model Querying', with five model icons in a column (GPT-4o-mini, Claude
  Haiku 4.5, Llama 3.1 8B, Qwen 2.5 7B, Mistral Small 24B), each producing 400 responses (5 models x 4 variants x 100 clusters).
  Stage 3 (third box, orange): 'Coherence Scoring', receiving the response matrix and emitting a 5x100 ordinal matrix (Y in
  {0, 1, 2}). Stage 4 (fourth box, purple): 'GRM Fitting via girth.grm_mml', emitting three outputs in three coloured side-boxes:
  theta (5 abilities, blue), alpha (100 discriminations, orange), beta (200 thresholds, green). Stage 5 (rightmost, red):
  'Validation', with two sub-boxes: 'Validation A: theta vs MMLU/HELM' and 'Validation B: stress test on Qwen 2.5 7B'. Arrows
  connect Stage 1 -> Stage 2 -> Stage 3 -> Stage 4 -> Stage 5. A small annotation below Stage 2 says '2,000 calls in 167 seconds,
  $0.048 cumulative'. Sans-serif font. Aspect ratio 21:9 to span the full width of a NeurIPS page.
aspect_ratio: '21:9'
summary: >-
  Pipeline diagram: cluster generation, querying, coherence scoring, GRM fitting, validation.
figure_path: figures/fig1_v0.jpg

--- Item 2 ---
id: fig2
figure_type: data
title: theta vs MMLU
caption: >-
  GRM-estimated theta versus published MMLU accuracy for n = 5 LLMs. Pearson r = 0.975, Spearman rho = 0.90, Kendall tau =
  0.80. The single rank inversion (Mistral Small 24B and Qwen 2.5 7B are swapped) bounds the rank statistics at this sample
  size.
image_gen_detailed_description: >-
  Scatter plot with five labelled points. X-axis: 'theta (GRM-estimated latent ability)', range -2.0 to +4.0. Y-axis: 'MMLU
  accuracy', range 0.60 to 0.85. Points (x, y): GPT-4o-mini at (3.69, 0.820), labelled 'GPT-4o-mini'; Claude Haiku 4.5 at
  (3.56, 0.801), labelled 'Claude Haiku 4.5'; Qwen 2.5 7B at (0.07, 0.707), labelled 'Qwen 2.5 7B'; Mistral Small 24B at (-0.28,
  0.732), labelled 'Mistral Small 24B'; Llama 3.1 8B at (-1.37, 0.684), labelled 'Llama 3.1 8B'. Each point is a filled circle
  of diameter 12 px with a black outline. Mistral Small 24B and Qwen 2.5 7B are connected by a short dashed grey arrow showing
  the rank inversion. Annotation in the upper-right corner, in two lines: 'Pearson r = 0.975' and 'Spearman rho = 0.90 (one
  rank inversion)'. Light grey grid lines at every 1 theta-unit on X and every 0.05 MMLU on Y. Sans-serif font, white background.
  Aspect ratio 4:3 (compact square-ish plot).
aspect_ratio: '4:3'
summary: >-
  Five-model scatter showing high theta-MMLU correlation with the Mistral-Qwen rank inversion highlighted.
figure_path: figures/fig2_v0.pdf

--- Item 3 ---
id: fig3
figure_type: data
title: Per-Model Coherence Distribution
caption: >-
  Ordinal coherence distribution per model across 100 MICs. The top two models achieve the top grade on 74-75% of clusters
  and the bottom grade on only 5%. Llama 3.1 8B sits at the floor on 20% of clusters, a 4x spread that the GRM exploits.
image_gen_detailed_description: >-
  Horizontal stacked bar chart, one bar per model, with five bars total. X-axis: 'fraction of 100 MICs', range 0.0 to 1.0,
  ticks every 0.2. Y-axis: model names listed top to bottom in this order: 'Claude Haiku 4.5', 'GPT-4o-mini', 'Mistral Small
  24B', 'Qwen 2.5 7B', 'Llama 3.1 8B'. Each bar is divided into three coloured segments: Y = 0 (red, leftmost) - fraction
  5/100 = 0.05 for Claude; 5/100 = 0.05 for GPT-4o-mini; 7/100 = 0.07 for Mistral; 16/100 = 0.16 for Qwen; 20/100 = 0.20 for
  Llama. Y = 1 (yellow, middle) - fraction 21/100 = 0.21 for Claude; 20/100 = 0.20 for GPT-4o-mini; 19/100 = 0.19 for Mistral;
  17/100 = 0.17 for Qwen; 26/100 = 0.26 for Llama. Y = 2 (green, rightmost) - fraction 74/100 = 0.74 for Claude; 75/100 =
  0.75 for GPT-4o-mini; 74/100 = 0.74 for Mistral; 67/100 = 0.67 for Qwen; 54/100 = 0.54 for Llama. Each bar has a thin black
  outline. Legend in the upper right: three small squares labelled 'Y = 0 (near-random)', 'Y = 1 (partially coherent)', 'Y
  = 2 (highly coherent)'. Title above chart: 'Ordinal coherence distribution per model across 100 MICs'. Sans-serif font,
  white background. Aspect ratio 16:9.
aspect_ratio: '16:9'
summary: >-
  Stacked bars showing how each model distributes across the three coherence grades.
figure_path: figures/fig3_v0.pdf

--- Item 4 ---
id: fig4
figure_type: data
title: Stress Test of Coherence Scoring
caption: >-
  Stress test on Qwen 2.5 7B: seed-only accuracy rises by +0.07 on average under artificial internal-inconsistency, while
  the GRM-estimated theta drops by -1.382 across three random seeds with standard deviation 0.007. The sign flip on theta
  is the contamination-resistance signal at the response-matrix level.
image_gen_detailed_description: >-
  Grouped bar chart with two panels side by side, sharing the same X-axis categories. Categories on X-axis: 'Seed 0', 'Seed
  1', 'Seed 42'. Left panel title 'Seed-only accuracy': Two bars per category, side by side. Clean (light blue): Seed 0 =
  0.78, Seed 1 = 0.78, Seed 42 = 0.78. Stressed (dark blue): Seed 0 = 0.85, Seed 1 = 0.84, Seed 42 = 0.86. Y-axis range 0.70
  to 0.90 with ticks every 0.05. Annotation arrow between Clean and Stressed at Seed 0 labelled '+0.07'. Right panel title
  'theta (GRM-estimated)': Two bars per category, side by side. Clean (light green): Seed 0 = -0.001, Seed 1 = -0.001, Seed
  42 = -0.001. Stressed (dark red): Seed 0 = -1.389, Seed 1 = -1.387, Seed 42 = -1.373. Y-axis range -1.5 to 0.5 with ticks
  every 0.5. Annotation arrow between Clean and Stressed at Seed 0 labelled '-1.382 (mean across seeds, std = 0.007)'. Both
  panels have white background, light grey grid lines, sans-serif font. Aspect ratio 16:9 for side-by-side display.
aspect_ratio: '16:9'
summary: >-
  Paired bars: static accuracy rises under stress, theta drops under stress, across three seeds.
figure_path: figures/fig4_v0.pdf
</available_figures>

<figure_requirements>
CRITICAL: Include ALL figures from <available_figures>. No exceptions.

- Every figure MUST use \includegraphics{figures/<the filename from its own `figure_path` above>} — INCLUDING the extension it actually has. Data figures are delivered as `.pdf` (vector, so their axis labels stay sharp) and concept figures as `.jpg`. Writing `.jpg` for a `.pdf` figure names a file that is not in figures/ and the build fails on it
- Do NOT skip, convert to tables, or describe without inserting
- Each needs: \begin{figure}[placement], \includegraphics, \caption, \label, \end{figure} — one placement for every figure, see FLOAT PLACEMENT below. Constrain every \includegraphics with `width=\linewidth,height=0.85\textheight,keepaspectratio`. The height is a LAST RESORT, not the usual limit: it exists so a very tall figure cannot overrun the page, and at 0.4 it bound almost everything instead — a 1:1 confusion matrix printed at 50.9% and its 11 pt axis labels reached the page at 5.6 pt, below what any venue accepts. At 0.85 every ratio the paper prompt prescribes (21:9, 16:9, 4:3, 1:1) is limited by WIDTH, prints at 93% and keeps its text above 10 pt. Use exactly these option keys — `max height=` is NOT valid LaTeX
- Use the `caption` field from each figure for \caption{...} — do NOT invent new captions
- Place figures where their [FIGURE:fig_id] markers appear in paper_text
- VERIFICATION: paper.tex MUST have exact same number of \includegraphics as <available_figures>
- Do NOT generate new figure images (no matplotlib, no PIL, no image generation). Use ONLY the pre-generated figures from <available_figures>. They were already created by a previous pipeline step.

FLOAT PLACEMENT: every figure gets \begin{figure}[!htbp]. Measured, not chosen:
the document the aii-paper-to-latex skill sets up is ONE column, so `figure*` is
exactly as wide as `figure` (469.76pt either way) and gains nothing; and any
placement asking for a page TOP — `[!t]`, `[!tbp]` — floated the hero diagram above
the paper's own title on page 1, while `[!htbp]` did not. `[!htbp]` also gives LaTeX
four options, so a float can never be deferred to the end of the document, which one
option alone risks. Where the hero ENDS UP is decided by its [FIGURE:] marker in
paper_text, which is already placed near the end of the Introduction — preserve it.
</figure_requirements>

<artifact_links>
The paper_text contains \footnote{Code: \url{...}} references linking to artifact source code
on GitHub. Include \usepackage{hyperref} and \usepackage{url}.
Preserve these exactly as-is — do not remove, rewrite, or convert them to plain text.
The URLs will not resolve yet (the repo is deployed after compilation) — do NOT try to verify or fix them.
</artifact_links>

<headings>
NEVER use inline math (``$...$``) inside ``\section{...}`` / ``\subsection{...}`` / ``\subsubsection{...}`` arguments — hyperref's bookmark builder errors out (``Token not allowed in a PDF string``) and the PDF outline breaks. If a section heading needs a math-looking term, use the text equivalent (``d star`` not ``$d^*$``, ``alpha-equivalent`` not ``$\alpha$-equivalent``) or wrap it in ``\texorpdfstring{$math$}{plain}``. Inline math inside body paragraphs is fine.
</headings>

<writing_register>
Write in the register of the field's best papers (the style exemplars block below, when the writing step saved any), not in the register of a language
model. Four things are measured on the finished draft, and a draft outside them is sent back with
the numbers:
- Never use: delve, underscore, showcase, intricate, pivotal, realm, commendable, meticulous, tapestry, garner, multifaceted, it is worth noting, plays a crucial role, not only ... but also. These are 10 to 30 times more frequent in machine-written abstracts than in
  human ones, and reviewers read them as such.
- Em dashes: at most 3 per 1,000 words. Use a comma, a colon or a full stop.
- Sentence rhythm: mix short and long sentences. An interquartile range of sentence length under
  8 words reads as machine-written.
- Hedging: at most 15 hedges (may, likely, suggests, appears) per 1,000
  words. State what the evidence supports plainly; hedge where it is thin, not everywhere.
Style never changes substance: numbers, claims, citations and figure markers stay exactly as the
evidence gives them. The user's original request (delivered as a separate message) overrides all
of this wherever the two conflict.
</writing_register>

<style_exemplars>
The draft in <paper_text> was written to the register of these passages, which the writing step
saved as style_exemplars.md. Any prose you add or change here (captions, transitions, cuts
for the page limit) stays in that register.

# Style Exemplars

The paper sits at the intersection of (a) LLM evaluation methodology (HELM lineage), (b) IRT-based psychometrics for LLMs (tinyBenchmarks, Lost in Benchmarks, ATLAS), and (c) dynamic / contamination-aware benchmarking (LiveBench). The four exemplars below come from those three subfields.

## One-line observations on style

- **Sentence length:** Median ~22 words, IQR ~12–18. Mix of short sentences (5–10 words) used for stating findings and long sentences (25–35 words) used for setup and definitions. Few one-word sentences.
- **Hedging:** Moderate (~10 hedges per 1k words). Phrases like "to the extent possible", "to a first approximation", "we find". Used in scope statements and limitations, not in headline claims.
- **First person:** Plural "we" throughout for multi-author work, even in single-author experiments. Avoid "the authors". Third person preferred for prior-work attribution ("Polo et al. report …").
- **Citation density:** Very high. 30–60 inline citations per paper; each substantive claim is backed by 1–3 citations. Bibliographic style is parenthetical (Author, Year) inline, alphabetical in references.
- **Voice:** Active. Methods verbs in present tense ("we fit", "we measure", "we generate"). Results in past tense ("the model achieved", "we found").

These register cues should be honoured throughout the draft. The verbatim passages below are *style samples only* — none of their content is reused.

---

## Exemplar 1 — HELM (Liang et al. 2022, TMLR)

Title: Holistic Evaluation of Language Models
Year: 2022 (revised 2023)
URL: https://arxiv.org/abs/2211.09110

### Abstract (excerpt)
"Language models (LMs) are becoming the foundation for almost all major language technologies, but their capabilities, limitations, and risks are not well understood. We present Holistic Evaluation of Language Models (HELM) to improve the transparency of language models. First, we taxonomize the vast space of potential scenarios (i.e. use cases) and metrics (i.e. desiderata) that are of interest for LMs. … We measure 7 metrics (accuracy, calibration, robustness, fairness, bias, toxicity, and efficiency) for each of 16 core scenarios to the extent possible (87.5% of the time), ensuring that metrics beyond accuracy don't fall to the wayside, and that trade-offs across models and metrics are clearly exposed. … Our evaluation surfaces 25 top-level findings concerning the interplay between different scenarios, metrics, and models."

### Introduction, paragraph 1 (verbatim)
"Benchmarks orient AI. They encode values and priorities (Ethayarajh & Jurafsky, 2020; Birhane et al., 2022) that specify directions for the AI community to improve upon (Spärck Jones & Galliers, 1995; Spärck Jones, 2005; Kiela et al., 2021; Bowman & Dahl, 2021; Raji et al., 2021). When implemented and interpreted appropriately, they enable the broader community to better understand AI technology and influence its trajectory. In recent years, the AI technology that has arguably advanced the most is foundation models (Bommasani et al., 2021), headlined by the rise of language models (LMs; Peters et al., 2018; Devlin et al., 2019; Brown et al., 2020; Rae et al., 2021; Chowdhery et al., 2022). At its core, a language model is a box that takes in text and generates text (Figure 1). Despite their simplicity, when these models are trained on broad data at immense scale, they can be adapted (e.g. prompted or fine-tuned) to myriad downstream scenarios. Yet the immense surface of model capabilities, limitations, and risks remains poorly understood. The rapid development, rising impact, and inadequate understanding demand that we benchmark language models holistically."

### Results / finding paragraph (excerpt)
"Prior to HELM, models on average were evaluated on just 17.9% of the core HELM scenarios, with some prominent models not sharing a single scenario in common. We improve this to 96.0%: now all 30 models have been densely benchmarked on a set of core scenarios and metrics under standardized conditions."

### Discussion / limitations (excerpt)
"We intend for HELM to be a living benchmark for the community, continuously updated with new scenarios, metrics, and models."

---

## Exemplar 2 — tinyBenchmarks (Polo et al. 2024, ICML)

Title: tinyBenchmarks: evaluating LLMs with fewer examples
Year: 2024
URL: https://arxiv.org/abs/2402.14992

### Abstract (verbatim)
"The versatility of large language models (LLMs) led to the creation of diverse benchmarks that thoroughly test a variety of language models' abilities. These benchmarks consist of tens of thousands of examples making evaluation of LLMs very expensive. In this paper, we investigate strategies to reduce the number of evaluations needed to assess the performance of an LLM on several key benchmarks. For example, we show that to accurately estimate the performance of an LLM on MMLU, a popular multiple-choice QA benchmark consisting of 14K examples, it is sufficient to evaluate this LLM on 100 curated examples. We release evaluation tools and tiny versions of popular benchmarks: Open LLM Leaderboard, MMLU, HELM, and AlpacaEval 2.0. Our empirical analysis demonstrates that these tools and tiny benchmarks are sufficient to reliably and efficiently reproduce the original evaluation results."

### Introduction, paragraph 1 (verbatim)
"Large Language Models (LLMs) have demonstrated remarkable abilities to solve a diverse range of tasks (Brown et al., 2020). Quantifying these abilities and comparing different LLMs became a challenge that led to the development of several key benchmarks, e.g., MMLU (Hendrycks et al., 2020), Open LLM Leaderboard (Beeching et al., 2023), HELM (Liang et al., 2022), and AlpacaEval (Li et al., 2023). These benchmarks are comprised of hundreds or thousands of examples, making the evaluation of modern LLMs with billions of parameters computationally, environmentally, and financially very costly. For example, Liang et al. (2022) report that evaluating the performance of a single LLM on HELM costs over 4K GPU hours (or over $10K for APIs)."

### Results paragraph (verbatim)
"Figure 1: Estimating accuracy on MMLU (true accuracy) using 100 curated examples (predicted accuracy). IRT++, our best-performing evaluation strategy, predicts the accuracy of recent LLMs released between December 30th and January 18th within 1.9% of their true accuracy on all of MMLU (14K examples)."

### Limitations (excerpt)
"6.2 Limitations … We note three primary limitations. First, our approaches assume access to a pre-evaluated set of LLMs on the full benchmark. … Second, the effectiveness of our methods depends on the quality and diversity of the pre-evaluated LLM pool. Third, our evaluation is focused on accuracy-based metrics; other metrics (e.g., calibration, robustness, fairness) may require different strategies."

---

## Exemplar 3 — LiveBench (White et al. 2024, ICLR Spotlight)

Title: LiveBench: A Challenging, Contamination-Limited LLM Benchmark
Year: 2024 (ICLR 2025 Spotlight)
URL: https://arxiv.org/abs/2406.19314

### Abstract (verbatim)
"Test set contamination, wherein test data from a benchmark ends up in a newer model's training set, is a well-documented obstacle for fair LLM evaluation and can quickly render benchmarks obsolete. To mitigate this, many recent benchmarks crowdsource new prompts and evaluations from human or LLM judges; however, these can introduce significant biases, and break down when scoring hard questions. In this work, we introduce a new benchmark for LLMs designed to be resistant to both test set contamination and the pitfalls of LLM judging and human crowdsourcing. We release LiveBench, the first benchmark that (1) contains frequently-updated questions from recent information sources, (2) scores answers automatically according to objective ground-truth values, and (3) contains a wide variety of challenging tasks, spanning math, coding, reasoning, language, instruction following, and data analysis. … LiveBench is difficult, with top models achieving below 70% accuracy."

### Discussion excerpt (paraphrased from public-facing intro)
"Test set contamination, wherein test data from a benchmark ends up in a newer model's training set, is a well-documented obstacle for fair LLM evaluation and can quickly render benchmarks obsolete. … Questions are added and updated on a monthly basis, and we release new tasks and harder versions of tasks over time so that LiveBench can distinguish between the capabilities of LLMs as they improve in the future."

---

## Exemplar 4 — LGMT (Zhou et al. 2026, Knowledge-Based Systems)

Title: LGMT: Logic-Grounded Metamorphic Testing for Evaluating the Reasoning Reliability of LLMs
Year: 2026
URL: https://arxiv.org/abs/2605.23965

### Excerpt (from research_report.md citation)
"LGMT derives 20 FOL-grounded MRs from De Morgan / contraposition / quantifier transformations and shows models are most sensitive to symbol- and conclusion-level variations; constructs 76,298 candidate metamorphic groups; evaluates 3,091 sampled across 6 LLMs and 4 prompting strategies."

### Excerpt from abstract framing (paraphrased)
"Metamorphic relations … are derived from first-order-logic transformations … we apply them to evaluate the reasoning reliability of LLMs. … [We] find that even strong LLMs show significant inconsistency across logically equivalent perturbations …"
</style_exemplars>
FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-to-latex, aii-semscholar-bib.
TODO 2. Review <paper_text> and <available_figures>. Copy all figure images into ./figures/ in your workspace. Count figures — MUST include every one. Plan placements per section. Build `./references.bib` via aii_semscholar_bib__fetch — collect DOIs/ArXiv IDs from <paper_text> and batch-fetch all BibTeX in one call. Do NOT fabricate entries.
TODO 3. Create `./paper.tex` per aii-paper-to-latex skill's setup, write ALL sections, insert ALL figures from <available_figures>, include `./references.bib` via \bibliography. Compile to PDF per skill's process. Fix errors.
TODO 4. CRITICAL VERIFICATION: Run `grep -c 'includegraphics' paper.tex`, confirm count equals figures in <available_figures>. If not, add missing figures. Verify `./paper.pdf` was created.
TODO 5. VISUAL REVIEW: Write Python script to convert EVERY page of paper.pdf to PNG at 150 DPI (use pdf2image or pymupdf). Then read ALL page screenshots — each page image costs ~1,600 tokens so a 15-page paper is only ~24K tokens. You MUST read every page. The ONLY exception is if all page images would not fit in your remaining context — in that case, read as many as fit and state which pages you are skipping and why. Check every page for layout issues, overlapping figures, cut-off text, bad spacing, formatting problems. Fix issues and recompile.
TODO 6. FINAL READ: Check page count (`pdfinfo paper.pdf` or pymupdf). Read entire paper.pdf — check for missing sections, unclear explanations, inconsistencies, typos. Fix and recompile. The ONLY exception is if all pages would not fit in your remaining context — in that case, read as many pages as fit and state which pages you are skipping and why.
</todos>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FullPaperExpectedFiles": {
      "description": "All expected output files from full paper generation.",
      "properties": {
        "paper_tex_path": {
          "description": "Path to LaTeX source file. Example: 'paper.tex'",
          "title": "Paper Tex Path",
          "type": "string"
        },
        "paper_pdf_path": {
          "description": "Path to compiled PDF. Example: 'paper.pdf'",
          "title": "Paper Pdf Path",
          "type": "string"
        },
        "references_bib_path": {
          "description": "Path to BibTeX bibliography file. Example: 'references.bib'",
          "title": "References Bib Path",
          "type": "string"
        },
        "figure_paths": {
          "description": "Paths to all figure image files. Example: ['figures/fig1_v0.jpg', 'figures/fig2_v0.jpg']",
          "items": {
            "type": "string"
          },
          "title": "Figure Paths",
          "type": "array"
        }
      },
      "required": [
        "paper_tex_path",
        "paper_pdf_path",
        "references_bib_path",
        "figure_paths"
      ],
      "title": "FullPaperExpectedFiles",
      "type": "object"
    }
  },
  "description": "Full paper \u2014 structured output from paper generation.",
  "properties": {
    "title": {
      "description": "Paper title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated paper: sections written, figures included, compilation status",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/FullPaperExpectedFiles",
      "description": "All output files you created. Must include paper.tex, paper.pdf, references.bib, and paths to all figure files."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "FullPaper",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [7] HUMAN-USER prompt · 2026-09-05 17:35:57 UTC

```
Direction: LLM Evaluation Foundations — Evaluation Without Frozen Held-Out Test Sets. Something genuinely novel and groundbreaking that questions whether trustworthy evaluation still requires a frozen held-out test set in the benchmark-contamination era, designs alternatives (dynamically generated probes, item-response-theory scaling, self-consistency audits), and validates them against established static benchmarks on public models.

Ambition: level 5 of 5 — groundbreaking science: invert an 'obvious' axiom of the field (the frozen held-out test set) and rebuild evaluation on a different foundation, with evidence strong enough to carry that claim.

Reviewer: I am Percy Liang (Stanford). Calibrate from my existing papers (HELM, foundation-model evaluation). Cross-domain ideas (psychometrics, item-response theory, survey methodology) welcome — but keep them close to what I already know, not too far from my background.

Submission/Goal: a paper for NeurIPS Datasets & Benchmarks or ICLR main track. Audience: ML evaluation researchers. Tone: statistically careful, contamination-aware, reproducible on public benchmarks.
```

### [8] SYSTEM-USER prompt · 2026-09-05 17:44:14 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `title`: 'M-IRT: Reference-Free LLM Evaluation via Samejima Graded Response Models on Dynamically Generated Metamorphic Item Clusters' is too long (at most 90 characters, got 123)
Every required field must be present and every field type must match the schema.

Produce `.sdk_openhands_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```
