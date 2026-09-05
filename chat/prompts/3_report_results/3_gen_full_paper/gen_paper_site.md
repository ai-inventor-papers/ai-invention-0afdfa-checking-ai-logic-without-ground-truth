# gen_paper_site — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `run_56IKXpJEZJ5b` — M-IRT: Reference-Free LLM Evaluation via Samejima Graded Response Models on Dynamically Generated Metamorphic Item Clusters
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_paper_site` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-09-05 17:26:12 UTC

````
<task>
Build the paper's public web page: ONE self-contained `index.html` that lets a reader grasp
this paper faster than opening the PDF would. It is published as this run's GitHub Pages site, so
it is the first thing anyone sees.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<what_is_already_here>
Your workspace is the finished paper folder. It already holds everything the page is made of, and
you must not change any of it — you are adding one file, not revising the paper.

- `paper.tex` — the paper as it was actually written. This is the source of truth for
  every claim, name and NUMBER that goes on the page.
- `paper.pdf` — the compiled paper. The page must NOT link to it by this local name:
  the PDF is published on the code branch and the page on a different one. Link to it at the
  full URL below instead.
- `references.bib` — the bibliography, when the paper has one.
- `figures/` — every figure the paper uses, flattened into one folder.
- `workspace/` — the scratch folder the LaTeX task worked in. Ignore it.
</what_is_already_here>

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
Each line gives the path the PAGE must use, then the figure's title and caption. It is the same
path the file has on disk here: the publish step copies the page and its figures into one folder,
so what works in this workspace is what works on the live site.

- figures/fig1_v0.jpg — "M-IRT Pipeline" (caption: "The four-stage M-IRT pipeline: deterministic MIC generation, zero-shot model querying, ordinal coherence scoring, and Samejima GRM fitting with two validation sub-experiments.")
- figures/fig2_v0.png [render from fig2_v0.pdf first] — "theta vs MMLU" (caption: "GRM-estimated theta versus published MMLU accuracy for n = 5 LLMs. Pearson r = 0.975, Spearman rho = 0.90, Kendall tau = 0.80. The single rank inversion (Mistral Small 24B and Qwen 2.5 7B are swapped) bounds the rank statistics at this sample size.")
- figures/fig3_v0.png [render from fig3_v0.pdf first] — "Per-Model Coherence Distribution" (caption: "Ordinal coherence distribution per model across 100 MICs. The top two models achieve the top grade on 74-75% of clusters and the bottom grade on only 5%. Llama 3.1 8B sits at the floor on 20% of clusters, a 4x spread that the GRM exploits.")
- figures/fig4_v0.png [render from fig4_v0.pdf first] — "Stress Test of Coherence Scoring" (caption: "Stress test on Qwen 2.5 7B: seed-only accuracy rises by +0.07 on average under artificial internal-inconsistency, while the GRM-estimated theta drops by -1.382 across three random seeds with standard deviation 0.007. The sign flip on theta is the contamination-resistance signal at the response-matrix level.")
</available_figures>

<figure_requirements>
- Reference every figure as `figures/` plus its filename, exactly as listed above.
  The publish step copies the page and its figures into one folder together, so that relative
  path is what resolves on the live site; anything else breaks once published.
- A browser cannot draw a PDF in an image element. Data figures are delivered as vector PDF for
  LaTeX's benefit, so for each one check whether a PNG of the same name already sits in
  `figures/`; if it does not, render one there at about 200 DPI with pdftoppm or
  pymupdf before referencing it. Renderable formats: .avif, .gif, .jpeg, .jpg, .png, .svg, .webp.
- Write those PNGs into `figures/` and nowhere else — that folder is published, a
  new folder of your own is not.
- Use each figure's own caption. Do not invent new ones, and do not describe a figure you did not
  place on the page.
- Look at every figure before you place it. A figure whose axis labels are unreadable at the size
  you give it is worse than no figure.
</figure_requirements>

<page_structure>
In this order, top to bottom:

1. HERO — the paper's title, the author line as the paper gives it, and a one-paragraph TL;DR in
   plain language: what was asked, what was found, and the single number that carries the finding.
   Not the abstract, and not a rewrite of it. Below it, two links: the PDF and the code
   repository, both at the exact URLs given in the links section below.
2. CONTRIBUTIONS — the paper's actual contributions as three to five scannable cards, each a short
   heading plus one or two sentences. If the paper claims four things, show four cards, not five.
3. METHOD — a walkthrough a technically literate non-specialist can follow: what goes in, what
   happens to it, what comes out, and why the design is the way it is. Lead with the paper's own
   method figure when it has one.
4. RESULTS — the paper's real headline numbers, read out of `paper.tex` and the data
   files behind it, each next to what it was measured on and what it is being compared against.
   A number that is not in the paper does not go on the page, and neither does a comparison the
   paper did not make. If a slot has no number, drop the slot.
5. FIGURE GALLERY — every figure, each with its caption, click-to-enlarge into a lightbox that
   closes on Escape, on a click outside, and on a visible close control.
6. LIMITATIONS — what the paper says it does not show. Verbatim in substance; do not soften it.
7. FOOTER — links to the PDF and the repository again, and the citation if the paper carries one.

A sticky section navigation runs alongside all of it and marks where the reader currently is.
</page_structure>

<technical_requirements>
- ONE file. All CSS in a style element, all JavaScript in a script element, both inline in
  `index.html`. No build step, no bundler, no framework, no external script, stylesheet, web
  font or analytics — nothing fetched at load time. The page must render with the network off,
  and the only files it may point at are the figures listed above and the PDF beside it.
- System font stack only, since no font may be downloaded.
- Light theme. Responsive from a 360px phone to a wide desktop, with no horizontal page scroll;
  wide content scrolls inside its own container.
- Honour prefers-reduced-motion: under it, transitions and any scroll-driven effect stop.
- Keyboard-navigable: every control reachable by Tab in a sensible order, a visible focus ring,
  the lightbox trapping focus while open and returning it to the thumbnail on close, and a skip
  link to the main content.
- Semantic HTML: one top-level heading, headings that descend without skipping, landmark elements,
  and alt text on every image that says what the figure shows rather than repeating its number.
- No emoji anywhere. No purple-to-blue gradients. No decorative icon fonts.
- Keep the whole file comfortably under a megabyte.
</technical_requirements>

<writing_register>
Write in the register of the field's best papers (the paper this page presents, which was written to them), not in the register of a language
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

<links>
Use these two URLs VERBATIM wherever the page links to the paper or the code. Do not shorten them,
do not turn either into a relative path, and do not compose one of your own.

- The paper PDF: https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-0afdfa-checking-ai-logic-without-ground-truth@main/paper.pdf
- The code repository: https://github.com/ai-inventor-papers/ai-invention-0afdfa-checking-ai-logic-without-ground-truth

Both carry the branch this run publishes to. A link without it opens a DIFFERENT run's work —
it resolves and looks correct, which is why it must be copied rather than derived. They begin
resolving only after this run finishes publishing, so do NOT try to open or verify them.
</links>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-web-tools.
TODO 2. Read `paper.tex` end to end and list `figures/`. Write down the
paper's title, its author line, its contributions, and every headline number together with the
sentence it appears in — those sentences are the only numbers allowed on the page. Note which
figures are PDFs and so need a PNG rendered.
TODO 3. Render a PNG at about 200 DPI, into `figures/`, for every figure not already
in a browser-renderable format, then LOOK at each image you plan to use so you know what it shows
and how large it has to be on the page to stay legible.
TODO 4. Write `index.html` following the page_structure and technical_requirements sections
above: one file, inline CSS and JavaScript, every image referenced through the published figure
prefix.
TODO 5. VERIFY THE NUMBERS: for each number on the page, grep `paper.tex` for it and
confirm it appears there with the same meaning. Delete any number you cannot find. Then confirm
every claim on the page is one the paper actually makes.
TODO 6. VERIFY THE PAGE: confirm `index.html` has no external script, stylesheet or font
reference; that every image path starts with the published figure prefix and names a file that
exists in `figures/`; and that the PDF and repository links are character-for-
character the two URLs given in the links section, not `paper.pdf` and not any URL you
composed. Then open the page in a browser, screenshot it at a phone width and a desktop width,
read both screenshots, and fix anything cramped, overlapping or cut off.
TODO 7. ACCESSIBILITY PASS: tab through the whole page and confirm every control is reachable with a
visible focus ring, the lightbox traps focus and closes on Escape, headings descend without
skipping, and every image has alt text. Fix what fails.
</todos>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "PaperSiteExpectedFiles": {
      "description": "All expected output files from paper-site generation.",
      "properties": {
        "site_html_path": {
          "description": "Path to the single self-contained HTML page. Example: 'index.html'",
          "title": "Site Html Path",
          "type": "string"
        }
      },
      "required": [
        "site_html_path"
      ],
      "title": "PaperSiteExpectedFiles",
      "type": "object"
    }
  },
  "description": "Paper site \u2014 structured output from presentation-page generation.",
  "properties": {
    "summary": {
      "description": "Brief summary of the page you built: the sections it carries, which figures it shows, which numbers it quotes and where each came from in the paper.",
      "maxLength": 5000,
      "minLength": 300,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/PaperSiteExpectedFiles",
      "description": "All output files you created. Must include index.html."
    }
  },
  "required": [
    "summary",
    "out_expected_files"
  ],
  "title": "PaperSite",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-09-05 17:26:12 UTC

```
Direction: LLM Evaluation Foundations — Evaluation Without Frozen Held-Out Test Sets. Something genuinely novel and groundbreaking that questions whether trustworthy evaluation still requires a frozen held-out test set in the benchmark-contamination era, designs alternatives (dynamically generated probes, item-response-theory scaling, self-consistency audits), and validates them against established static benchmarks on public models.

Ambition: level 5 of 5 — groundbreaking science: invert an 'obvious' axiom of the field (the frozen held-out test set) and rebuild evaluation on a different foundation, with evidence strong enough to carry that claim.

Reviewer: I am Percy Liang (Stanford). Calibrate from my existing papers (HELM, foundation-model evaluation). Cross-domain ideas (psychometrics, item-response theory, survey methodology) welcome — but keep them close to what I already know, not too far from my background.

Submission/Goal: a paper for NeurIPS Datasets & Benchmarks or ICLR main track. Audience: ML evaluation researchers. Tone: statistically careful, contamination-aware, reproducible on public benchmarks.
```

### [3] SKILL-INPUT — aii-web-tools · 2026-09-05 17:26:22 UTC

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

### [4] SKILL-INPUT — amg-open-img-ubuntu · 2026-09-05 17:27:33 UTC

The agent loaded the **amg-open-img-ubuntu** skill.

```
Tool: invoke_skill
{
  "name": "amg-open-img-ubuntu"
}
```

### [5] SYSTEM-USER prompt · 2026-09-05 17:29:21 UTC

````
PREVIOUS ATTEMPT FAILED
Failure reason: structured_output is None
Last actions before failure:
  - [agent_response]: I need to rename the PNGs since pdftoppm adds `-1` suffix:
  - [agent_tool_call] terminal: Tool: terminal
{
  "command": "mv fig2_v0-1.png fig2_v0.png && mv fig3_v0-1.png fig3_v0.png && mv fig4_v0-1.png fig4_v0.png && ls -la",
  "is_input": false,
  "timeout": null,
  "reset": false
}
  - [agent_tool_call] terminal: Tool: terminal
{
  "command": "cd /ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/figures && python3 -c \"\nfrom PIL import Image\nfor f in ['fig1_v0.jpg', 'fig2_v0.png', 'fig3_v0.png', 'fig4_v0.png']:\n    img = Image.open(f)\n    print(f, img.size, img.mode)\n\
  - [agent_tool_result] terminal: Tool: terminal
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "total 3243\ndrwxr-xr-x 2 root root 1028161 Sep  5 17:27 .\ndrwxr-xr-x 4 root root 2001090 Sep  5 17:26 ..\n-rw-r--r-- 1 root root   23913 Sep  5 17:26 fig1_v0.jpg\n-rw------- 1 root root    1526 Sep  5 17:26 fig2_sp
  - [agent_tool_result] terminal: Tool: terminal
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "fig1_v0.jpg (1024, 448) RGB\nfig2_v0.png (1200, 900) RGB\nfig3_v0.png (1400, 788) RGB\nfig4_v0.png (1826, 1267) RGB"}], "is_error": false, "command": "cd /ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/
  - [agent_response]: Now let me look at the figures to understand them:
  - [agent_tool_call] invoke_skill: Tool: invoke_skill
{
  "name": "amg-open-img-ubuntu"
}
  - [agent_tool_result] invoke_skill: Tool: invoke_skill
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "Unknown skill 'amg-open-img-ubuntu'. Available skills: aii-colab, aii-concept-fig-gen, aii-data-fig-gen, aii-file-size-limit, aii-handbook-auto-computational-linguistics, aii-handbook-auto-mechanistic-interpreta
  - [agent_tool_call] terminal: Tool: terminal
{
  "command": "cat /ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/figures/fig2_spec.json\necho \"---\"\ncat /ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/figures/fig3_spec.json\necho \"---\"\ncat /ai-invento
  - [agent_tool_result] terminal: Tool: terminal
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "Cannot execute multiple commands at once.\nPlease run each command separately OR chain them into a single command via && or ;\nProvided commands:\n(1) cat /ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "view",
  "path": "/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/figures/fig2_spec.json",
  "file_text": null,
  "old_str": null,
  "new_str": null,
  "insert_line": null,
  "view_range": null
}
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "view",
  "path": "/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/figures/fig3_spec.json",
  "file_text": null,
  "old_str": null,
  "new_str": null,
  "insert_line": null,
  "view_range": null
}
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "view",
  "path": "/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/figures/fig4_spec.json",
  "file_text": null,
  "old_str": null,
  "new_str": null,
  "insert_line": null,
  "view_range": null
}
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "Here's the result of running `cat -n` on /ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/figures/fig2_spec.json:\n     1\t{\n     2\t  \"type\": \"scatter_theta_mmlu\",\n     
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "Here's the result of running `cat -n` on /ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/figures/fig3_spec.json:\n     1\t{\n     2\t  \"type\": \"handwritten_horizontal_stack
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "Here's the result of running `cat -n` on /ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/figures/fig4_spec.json:\n     1\t{\n     2\t  \"type\": \"panel\",\n     3\t  \"title\
  - [agent_response]: I have full context now. Let me view the actual rendered images by opening them in a browser via Python and inspect via small thumbnails to know what they show:
  - [agent_tool_call] terminal: Tool: terminal
{
  "command": "cd /ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/figures && python3 -c \"\nfrom PIL import Image\nimport base64\nimport io\nfor f in ['fig1_v0.jpg', 'fig2_v0.png', 'fig3_v0.png', 'fig4_v0.png']:\n    img = Image.open(f)\n    img.t
  - [agent_tool_result] terminal: Tool: terminal
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "fig1_v0.jpg -> (400, 175)\nfig2_v0.png -> (400, 300)\nfig3_v0.png -> (400, 225)\nfig4_v0.png -> (400, 278)\n-rw-r--r-- 1 root root 28733 Sep  5 17:27 /tmp/fig1_v0_thumb.png\n-rw-r--r-- 1 root root 26104 Sep  5 17:27
  - [status_public_warning]: Conversation error [BadGatewayError]: litellm.BadGatewayError: BadGatewayError: OpenAIException - 

Use any partial work that exists from the previous attempt. Do NOT start over — pick up where the previous attempt left off.

<task>
Build the paper's public web page: ONE self-contained `index.html` that lets a reader grasp
this paper faster than opening the PDF would. It is published as this run's GitHub Pages site, so
it is the first thing anyone sees.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<what_is_already_here>
Your workspace is the finished paper folder. It already holds everything the page is made of, and
you must not change any of it — you are adding one file, not revising the paper.

- `paper.tex` — the paper as it was actually written. This is the source of truth for
  every claim, name and NUMBER that goes on the page.
- `paper.pdf` — the compiled paper. The page must NOT link to it by this local name:
  the PDF is published on the code branch and the page on a different one. Link to it at the
  full URL below instead.
- `references.bib` — the bibliography, when the paper has one.
- `figures/` — every figure the paper uses, flattened into one folder.
- `workspace/` — the scratch folder the LaTeX task worked in. Ignore it.
</what_is_already_here>

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
Each line gives the path the PAGE must use, then the figure's title and caption. It is the same
path the file has on disk here: the publish step copies the page and its figures into one folder,
so what works in this workspace is what works on the live site.

- figures/fig1_v0.jpg — "M-IRT Pipeline" (caption: "The four-stage M-IRT pipeline: deterministic MIC generation, zero-shot model querying, ordinal coherence scoring, and Samejima GRM fitting with two validation sub-experiments.")
- figures/fig2_v0.png [render from fig2_v0.pdf first] — "theta vs MMLU" (caption: "GRM-estimated theta versus published MMLU accuracy for n = 5 LLMs. Pearson r = 0.975, Spearman rho = 0.90, Kendall tau = 0.80. The single rank inversion (Mistral Small 24B and Qwen 2.5 7B are swapped) bounds the rank statistics at this sample size.")
- figures/fig3_v0.png [render from fig3_v0.pdf first] — "Per-Model Coherence Distribution" (caption: "Ordinal coherence distribution per model across 100 MICs. The top two models achieve the top grade on 74-75% of clusters and the bottom grade on only 5%. Llama 3.1 8B sits at the floor on 20% of clusters, a 4x spread that the GRM exploits.")
- figures/fig4_v0.png [render from fig4_v0.pdf first] — "Stress Test of Coherence Scoring" (caption: "Stress test on Qwen 2.5 7B: seed-only accuracy rises by +0.07 on average under artificial internal-inconsistency, while the GRM-estimated theta drops by -1.382 across three random seeds with standard deviation 0.007. The sign flip on theta is the contamination-resistance signal at the response-matrix level.")
</available_figures>

<figure_requirements>
- Reference every figure as `figures/` plus its filename, exactly as listed above.
  The publish step copies the page and its figures into one folder together, so that relative
  path is what resolves on the live site; anything else breaks once published.
- A browser cannot draw a PDF in an image element. Data figures are delivered as vector PDF for
  LaTeX's benefit, so for each one check whether a PNG of the same name already sits in
  `figures/`; if it does not, render one there at about 200 DPI with pdftoppm or
  pymupdf before referencing it. Renderable formats: .avif, .gif, .jpeg, .jpg, .png, .svg, .webp.
- Write those PNGs into `figures/` and nowhere else — that folder is published, a
  new folder of your own is not.
- Use each figure's own caption. Do not invent new ones, and do not describe a figure you did not
  place on the page.
- Look at every figure before you place it. A figure whose axis labels are unreadable at the size
  you give it is worse than no figure.
</figure_requirements>

<page_structure>
In this order, top to bottom:

1. HERO — the paper's title, the author line as the paper gives it, and a one-paragraph TL;DR in
   plain language: what was asked, what was found, and the single number that carries the finding.
   Not the abstract, and not a rewrite of it. Below it, two links: the PDF and the code
   repository, both at the exact URLs given in the links section below.
2. CONTRIBUTIONS — the paper's actual contributions as three to five scannable cards, each a short
   heading plus one or two sentences. If the paper claims four things, show four cards, not five.
3. METHOD — a walkthrough a technically literate non-specialist can follow: what goes in, what
   happens to it, what comes out, and why the design is the way it is. Lead with the paper's own
   method figure when it has one.
4. RESULTS — the paper's real headline numbers, read out of `paper.tex` and the data
   files behind it, each next to what it was measured on and what it is being compared against.
   A number that is not in the paper does not go on the page, and neither does a comparison the
   paper did not make. If a slot has no number, drop the slot.
5. FIGURE GALLERY — every figure, each with its caption, click-to-enlarge into a lightbox that
   closes on Escape, on a click outside, and on a visible close control.
6. LIMITATIONS — what the paper says it does not show. Verbatim in substance; do not soften it.
7. FOOTER — links to the PDF and the repository again, and the citation if the paper carries one.

A sticky section navigation runs alongside all of it and marks where the reader currently is.
</page_structure>

<technical_requirements>
- ONE file. All CSS in a style element, all JavaScript in a script element, both inline in
  `index.html`. No build step, no bundler, no framework, no external script, stylesheet, web
  font or analytics — nothing fetched at load time. The page must render with the network off,
  and the only files it may point at are the figures listed above and the PDF beside it.
- System font stack only, since no font may be downloaded.
- Light theme. Responsive from a 360px phone to a wide desktop, with no horizontal page scroll;
  wide content scrolls inside its own container.
- Honour prefers-reduced-motion: under it, transitions and any scroll-driven effect stop.
- Keyboard-navigable: every control reachable by Tab in a sensible order, a visible focus ring,
  the lightbox trapping focus while open and returning it to the thumbnail on close, and a skip
  link to the main content.
- Semantic HTML: one top-level heading, headings that descend without skipping, landmark elements,
  and alt text on every image that says what the figure shows rather than repeating its number.
- No emoji anywhere. No purple-to-blue gradients. No decorative icon fonts.
- Keep the whole file comfortably under a megabyte.
</technical_requirements>

<writing_register>
Write in the register of the field's best papers (the paper this page presents, which was written to them), not in the register of a language
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

<links>
Use these two URLs VERBATIM wherever the page links to the paper or the code. Do not shorten them,
do not turn either into a relative path, and do not compose one of your own.

- The paper PDF: https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-0afdfa-checking-ai-logic-without-ground-truth@main/paper.pdf
- The code repository: https://github.com/ai-inventor-papers/ai-invention-0afdfa-checking-ai-logic-without-ground-truth

Both carry the branch this run publishes to. A link without it opens a DIFFERENT run's work —
it resolves and looks correct, which is why it must be copied rather than derived. They begin
resolving only after this run finishes publishing, so do NOT try to open or verify them.
</links>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-web-tools.
TODO 2. Read `paper.tex` end to end and list `figures/`. Write down the
paper's title, its author line, its contributions, and every headline number together with the
sentence it appears in — those sentences are the only numbers allowed on the page. Note which
figures are PDFs and so need a PNG rendered.
TODO 3. Render a PNG at about 200 DPI, into `figures/`, for every figure not already
in a browser-renderable format, then LOOK at each image you plan to use so you know what it shows
and how large it has to be on the page to stay legible.
TODO 4. Write `index.html` following the page_structure and technical_requirements sections
above: one file, inline CSS and JavaScript, every image referenced through the published figure
prefix.
TODO 5. VERIFY THE NUMBERS: for each number on the page, grep `paper.tex` for it and
confirm it appears there with the same meaning. Delete any number you cannot find. Then confirm
every claim on the page is one the paper actually makes.
TODO 6. VERIFY THE PAGE: confirm `index.html` has no external script, stylesheet or font
reference; that every image path starts with the published figure prefix and names a file that
exists in `figures/`; and that the PDF and repository links are character-for-
character the two URLs given in the links section, not `paper.pdf` and not any URL you
composed. Then open the page in a browser, screenshot it at a phone width and a desktop width,
read both screenshots, and fix anything cramped, overlapping or cut off.
TODO 7. ACCESSIBILITY PASS: tab through the whole page and confirm every control is reachable with a
visible focus ring, the lightbox traps focus and closes on Escape, headings descend without
skipping, and every image has alt text. Fix what fails.
</todos>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "PaperSiteExpectedFiles": {
      "description": "All expected output files from paper-site generation.",
      "properties": {
        "site_html_path": {
          "description": "Path to the single self-contained HTML page. Example: 'index.html'",
          "title": "Site Html Path",
          "type": "string"
        }
      },
      "required": [
        "site_html_path"
      ],
      "title": "PaperSiteExpectedFiles",
      "type": "object"
    }
  },
  "description": "Paper site \u2014 structured output from presentation-page generation.",
  "properties": {
    "summary": {
      "description": "Brief summary of the page you built: the sections it carries, which figures it shows, which numbers it quotes and where each came from in the paper.",
      "maxLength": 5000,
      "minLength": 300,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/PaperSiteExpectedFiles",
      "description": "All output files you created. Must include index.html."
    }
  },
  "required": [
    "summary",
    "out_expected_files"
  ],
  "title": "PaperSite",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [6] HUMAN-USER prompt · 2026-09-05 17:29:21 UTC

```
Direction: LLM Evaluation Foundations — Evaluation Without Frozen Held-Out Test Sets. Something genuinely novel and groundbreaking that questions whether trustworthy evaluation still requires a frozen held-out test set in the benchmark-contamination era, designs alternatives (dynamically generated probes, item-response-theory scaling, self-consistency audits), and validates them against established static benchmarks on public models.

Ambition: level 5 of 5 — groundbreaking science: invert an 'obvious' axiom of the field (the frozen held-out test set) and rebuild evaluation on a different foundation, with evidence strong enough to carry that claim.

Reviewer: I am Percy Liang (Stanford). Calibrate from my existing papers (HELM, foundation-model evaluation). Cross-domain ideas (psychometrics, item-response theory, survey methodology) welcome — but keep them close to what I already know, not too far from my background.

Submission/Goal: a paper for NeurIPS Datasets & Benchmarks or ICLR main track. Audience: ML evaluation researchers. Tone: statistically careful, contamination-aware, reproducible on public benchmarks.
```

### [7] SYSTEM-USER prompt · 2026-09-05 17:44:51 UTC

````
<task>
Build the paper's public web page: ONE self-contained `index.html` that lets a reader grasp
this paper faster than opening the PDF would. It is published as this run's GitHub Pages site, so
it is the first thing anyone sees.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<what_is_already_here>
Your workspace is the finished paper folder. It already holds everything the page is made of, and
you must not change any of it — you are adding one file, not revising the paper.

- `paper.tex` — the paper as it was actually written. This is the source of truth for
  every claim, name and NUMBER that goes on the page.
- `paper.pdf` — the compiled paper. The page must NOT link to it by this local name:
  the PDF is published on the code branch and the page on a different one. Link to it at the
  full URL below instead.
- `references.bib` — the bibliography, when the paper has one.
- `figures/` — every figure the paper uses, flattened into one folder.
- `workspace/` — the scratch folder the LaTeX task worked in. Ignore it.
</what_is_already_here>

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
Each line gives the path the PAGE must use, then the figure's title and caption. It is the same
path the file has on disk here: the publish step copies the page and its figures into one folder,
so what works in this workspace is what works on the live site.

- figures/fig1_v0.jpg — "M-IRT Pipeline" (caption: "The four-stage M-IRT pipeline: deterministic MIC generation, zero-shot model querying, ordinal coherence scoring, and Samejima GRM fitting with two validation sub-experiments.")
- figures/fig2_v0.png [render from fig2_v0.pdf first] — "theta vs MMLU" (caption: "GRM-estimated theta versus published MMLU accuracy for n = 5 LLMs. Pearson r = 0.975, Spearman rho = 0.90, Kendall tau = 0.80. The single rank inversion (Mistral Small 24B and Qwen 2.5 7B are swapped) bounds the rank statistics at this sample size.")
- figures/fig3_v0.png [render from fig3_v0.pdf first] — "Per-Model Coherence Distribution" (caption: "Ordinal coherence distribution per model across 100 MICs. The top two models achieve the top grade on 74-75% of clusters and the bottom grade on only 5%. Llama 3.1 8B sits at the floor on 20% of clusters, a 4x spread that the GRM exploits.")
- figures/fig4_v0.png [render from fig4_v0.pdf first] — "Stress Test of Coherence Scoring" (caption: "Stress test on Qwen 2.5 7B: seed-only accuracy rises by +0.07 on average under artificial internal-inconsistency, while the GRM-estimated theta drops by -1.382 across three random seeds with standard deviation 0.007. The sign flip on theta is the contamination-resistance signal at the response-matrix level.")
</available_figures>

<figure_requirements>
- Reference every figure as `figures/` plus its filename, exactly as listed above.
  The publish step copies the page and its figures into one folder together, so that relative
  path is what resolves on the live site; anything else breaks once published.
- A browser cannot draw a PDF in an image element. Data figures are delivered as vector PDF for
  LaTeX's benefit, so for each one check whether a PNG of the same name already sits in
  `figures/`; if it does not, render one there at about 200 DPI with pdftoppm or
  pymupdf before referencing it. Renderable formats: .avif, .gif, .jpeg, .jpg, .png, .svg, .webp.
- Write those PNGs into `figures/` and nowhere else — that folder is published, a
  new folder of your own is not.
- Use each figure's own caption. Do not invent new ones, and do not describe a figure you did not
  place on the page.
- Look at every figure before you place it. A figure whose axis labels are unreadable at the size
  you give it is worse than no figure.
</figure_requirements>

<page_structure>
In this order, top to bottom:

1. HERO — the paper's title, the author line as the paper gives it, and a one-paragraph TL;DR in
   plain language: what was asked, what was found, and the single number that carries the finding.
   Not the abstract, and not a rewrite of it. Below it, two links: the PDF and the code
   repository, both at the exact URLs given in the links section below.
2. CONTRIBUTIONS — the paper's actual contributions as three to five scannable cards, each a short
   heading plus one or two sentences. If the paper claims four things, show four cards, not five.
3. METHOD — a walkthrough a technically literate non-specialist can follow: what goes in, what
   happens to it, what comes out, and why the design is the way it is. Lead with the paper's own
   method figure when it has one.
4. RESULTS — the paper's real headline numbers, read out of `paper.tex` and the data
   files behind it, each next to what it was measured on and what it is being compared against.
   A number that is not in the paper does not go on the page, and neither does a comparison the
   paper did not make. If a slot has no number, drop the slot.
5. FIGURE GALLERY — every figure, each with its caption, click-to-enlarge into a lightbox that
   closes on Escape, on a click outside, and on a visible close control.
6. LIMITATIONS — what the paper says it does not show. Verbatim in substance; do not soften it.
7. FOOTER — links to the PDF and the repository again, and the citation if the paper carries one.

A sticky section navigation runs alongside all of it and marks where the reader currently is.
</page_structure>

<technical_requirements>
- ONE file. All CSS in a style element, all JavaScript in a script element, both inline in
  `index.html`. No build step, no bundler, no framework, no external script, stylesheet, web
  font or analytics — nothing fetched at load time. The page must render with the network off,
  and the only files it may point at are the figures listed above and the PDF beside it.
- System font stack only, since no font may be downloaded.
- Light theme. Responsive from a 360px phone to a wide desktop, with no horizontal page scroll;
  wide content scrolls inside its own container.
- Honour prefers-reduced-motion: under it, transitions and any scroll-driven effect stop.
- Keyboard-navigable: every control reachable by Tab in a sensible order, a visible focus ring,
  the lightbox trapping focus while open and returning it to the thumbnail on close, and a skip
  link to the main content.
- Semantic HTML: one top-level heading, headings that descend without skipping, landmark elements,
  and alt text on every image that says what the figure shows rather than repeating its number.
- No emoji anywhere. No purple-to-blue gradients. No decorative icon fonts.
- Keep the whole file comfortably under a megabyte.
</technical_requirements>

<writing_register>
Write in the register of the field's best papers (the paper this page presents, which was written to them), not in the register of a language
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

<links>
Use these two URLs VERBATIM wherever the page links to the paper or the code. Do not shorten them,
do not turn either into a relative path, and do not compose one of your own.

- The paper PDF: https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-0afdfa-checking-ai-logic-without-ground-truth@main/paper.pdf
- The code repository: https://github.com/ai-inventor-papers/ai-invention-0afdfa-checking-ai-logic-without-ground-truth

Both carry the branch this run publishes to. A link without it opens a DIFFERENT run's work —
it resolves and looks correct, which is why it must be copied rather than derived. They begin
resolving only after this run finishes publishing, so do NOT try to open or verify them.
</links>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-web-tools.
TODO 2. Read `paper.tex` end to end and list `figures/`. Write down the
paper's title, its author line, its contributions, and every headline number together with the
sentence it appears in — those sentences are the only numbers allowed on the page. Note which
figures are PDFs and so need a PNG rendered.
TODO 3. Render a PNG at about 200 DPI, into `figures/`, for every figure not already
in a browser-renderable format, then LOOK at each image you plan to use so you know what it shows
and how large it has to be on the page to stay legible.
TODO 4. Write `index.html` following the page_structure and technical_requirements sections
above: one file, inline CSS and JavaScript, every image referenced through the published figure
prefix.
TODO 5. VERIFY THE NUMBERS: for each number on the page, grep `paper.tex` for it and
confirm it appears there with the same meaning. Delete any number you cannot find. Then confirm
every claim on the page is one the paper actually makes.
TODO 6. VERIFY THE PAGE: confirm `index.html` has no external script, stylesheet or font
reference; that every image path starts with the published figure prefix and names a file that
exists in `figures/`; and that the PDF and repository links are character-for-
character the two URLs given in the links section, not `paper.pdf` and not any URL you
composed. Then open the page in a browser, screenshot it at a phone width and a desktop width,
read both screenshots, and fix anything cramped, overlapping or cut off.
TODO 7. ACCESSIBILITY PASS: tab through the whole page and confirm every control is reachable with a
visible focus ring, the lightbox traps focus and closes on Escape, headings descend without
skipping, and every image has alt text. Fix what fails.
</todos>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "PaperSiteExpectedFiles": {
      "description": "All expected output files from paper-site generation.",
      "properties": {
        "site_html_path": {
          "description": "Path to the single self-contained HTML page. Example: 'index.html'",
          "title": "Site Html Path",
          "type": "string"
        }
      },
      "required": [
        "site_html_path"
      ],
      "title": "PaperSiteExpectedFiles",
      "type": "object"
    }
  },
  "description": "Paper site \u2014 structured output from presentation-page generation.",
  "properties": {
    "summary": {
      "description": "Brief summary of the page you built: the sections it carries, which figures it shows, which numbers it quotes and where each came from in the paper.",
      "maxLength": 5000,
      "minLength": 300,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/PaperSiteExpectedFiles",
      "description": "All output files you created. Must include index.html."
    }
  },
  "required": [
    "summary",
    "out_expected_files"
  ],
  "title": "PaperSite",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/ai-inventor/aii_data/runs/run_56IKXpJEZJ5b/4_gen_paper_repo/_4_assemble_paper/paper/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [8] HUMAN-USER prompt · 2026-09-05 17:44:51 UTC

```
Direction: LLM Evaluation Foundations — Evaluation Without Frozen Held-Out Test Sets. Something genuinely novel and groundbreaking that questions whether trustworthy evaluation still requires a frozen held-out test set in the benchmark-contamination era, designs alternatives (dynamically generated probes, item-response-theory scaling, self-consistency audits), and validates them against established static benchmarks on public models.

Ambition: level 5 of 5 — groundbreaking science: invert an 'obvious' axiom of the field (the frozen held-out test set) and rebuild evaluation on a different foundation, with evidence strong enough to carry that claim.

Reviewer: I am Percy Liang (Stanford). Calibrate from my existing papers (HELM, foundation-model evaluation). Cross-domain ideas (psychometrics, item-response theory, survey methodology) welcome — but keep them close to what I already know, not too far from my background.

Submission/Goal: a paper for NeurIPS Datasets & Benchmarks or ICLR main track. Audience: ML evaluation researchers. Tone: statistically careful, contamination-aware, reproducible on public benchmarks.
```

### [9] SYSTEM-USER prompt · 2026-09-05 17:59:59 UTC

```
STOP. You have reached the maximum number of turns.

Do NOT use any more tools. Finish what you are doing and provide your final output NOW.

Use whatever information you have gathered so far to produce the best response possible.
```

### [10] SYSTEM-USER prompt · 2026-09-05 18:00:49 UTC

```
SITE VERIFICATION FAILED: 1 problem(s) in index.html.

- image source '' does not start with 'figures/', so it will not resolve once the page is published beside its figures folder

You MUST:
1. Fix every problem listed above in index.html.
2. Keep the page ONE self-contained file — all CSS and JavaScript inline, no external scripts, stylesheets or web fonts, nothing fetched at load time.
3. Point every image at figures/<filename>, where <filename> is a browser-renderable image that really exists in your figures/ folder. A vector PDF figure needs a PNG rendered beside it first; reference the PNG.
4. Re-open the page and confirm it still renders before finishing.
```
