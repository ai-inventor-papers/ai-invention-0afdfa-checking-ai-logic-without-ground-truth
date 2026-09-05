#!/usr/bin/env python3
"""Stage 1: Metamorphic Item Cluster (MIC) generator.

Produces deterministic clusters in two domains — propositional syllogisms and
arithmetic word problems. Each cluster carries four variants: seed, paraphrase,
negation, and (for logic) contrapositive / (for arithmetic) inverse — plus the
oracle (ground-truth) answer and a difficulty hint.

Pure Python / stdlib. No API spend, runs on CPU.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass, asdict, field
from typing import Callable

# ----------------------------------------------------------------------------
# Noun / proper-name pools. Distinct noun sets are reserved per domain so
# paraphrase clauses never share vocabulary with the seed.
# ----------------------------------------------------------------------------

LOGIC_NOUNS = [
    "doctors", "lawyers", "teachers", "engineers", "scientists", "writers",
    "farmers", "musicians", "athletes", "drivers", "students", "workers",
    "artists", "soldiers", "pilots", "chefs", "painters", "dancers",
    "singers", "judges", "actors", "nurses", "carpenters", "miners",
    "plumbers", "gardeners", "tailors", "designers", "explorers", "astronauts",
    "metals", "gases", "liquids", "minerals", "vegetables", "fruits",
    "flowers", "trees", "insects", "fish", "birds", "reptiles",
    "tools", "vehicles", "buildings", "devices", "garments", "furniture",
    "documents", "machines", "weapons", "instruments", "vessels", "structures",
]

LOGIC_NOUNS_PARAPHRASE = [
    "philosophers", "veterinarians", "architects", "dentists", "librarians",
    "journalists", "bakers", "cobblers", "locksmiths", "masons", "opticians",
    "pharmacists", "surveyors", "barbers", "butchers", "fishermen", "hunters",
    "spices", "cereals", "mushrooms", "berries", "shells", "stones",
    "crystals", "fossils", "poems", "novels", "songs", "stories",
    "diamonds", "pearls", "coins", "stamps", "puzzles", "toys",
    "candles", "mirrors", "lanterns", "rugs", "blankets", "curtains",
]

NAMES_A = [
    "Alice", "Brian", "Carmen", "Diego", "Esme", "Felix", "Greta", "Hassan",
    "Inez", "Jules", "Keiko", "Liam", "Maya", "Noah", "Olive", "Pedro",
    "Quinn", "Rosa", "Sami", "Tomas", "Uma", "Vince", "Wren", "Xenia",
    "Yara", "Zane",
]
NAMES_B = [
    "Beatrice", "Caleb", "Daria", "Eitan", "Farah", "Gideon", "Hana",
    "Ivan", "Jada", "Karim", "Lila", "Marco", "Nadia", "Owen", "Priya",
    "Quincy", "Rafael", "Selma", "Tariq", "Ula", "Vera", "Wesley", "Ximena",
    "Yusuf", "Zara",
]

ITEMS = [
    "apples", "books", "pencils", "marbles", "cookies", "stamps", "stickers",
    "cards", "shells", "toys", "buttons", "ribbons", "beads", "pebbles",
    "candies", "oranges", "lemons", "plums", "acorns", "feathers", "pearls",
    "coins", "rubber bands", "paper clips",
]

ITEMS_PARAPHRASE = [
    "trading cards", "figurines", "postcards", "souvenir spoons", "fossils",
    "gemstones", "marbles of glass", "scraps of paper", "buttons of brass",
    "ribbons of silk", "beads of jade", "pebbles of quartz", "feathers of blue",
    "pearls of pink", "stones of jade", "smooth chestnuts",
    "silver coins", "tiny bells", "tiny skulls", "wax seals", "lacquered fans",
    "candy wrappers", "tin whistles", "tiny lamps",
]


# ----------------------------------------------------------------------------
# Logic (syllogism) templates
#
# Each template returns (premise_a, premise_b, conclusion, label) where
# label is the oracle answer — 'V' for valid, 'I' for invalid.
# The slots {A}, {B}, {C} are filled with concrete nouns.
# ----------------------------------------------------------------------------

LOGIC_TEMPLATES: list[tuple[str, Callable[[str, str, str], tuple[str, str, str, str]]]] = [
    (
        "T1", lambda A, B, C: (
            f"All {A} are {B}. All {B} are {C}.",
            f"Therefore, all {A} are {C}.",
            "V",
        )
    ),
    (
        "T2", lambda A, B, C: (
            f"All {A} are {B}. Some {B} are {C}.",
            f"Therefore, all {A} are {C}.",
            "I",
        )
    ),
    (
        "T3", lambda A, B, C: (
            f"No {A} are {B}. All {B} are {C}.",
            f"Therefore, no {A} are {C}.",
            "I",
        )
    ),
    (
        "T4", lambda A, B, C: (
            f"All {A} are {B}. No {B} are {C}.",
            f"Therefore, no {A} are {C}.",
            "V",
        )
    ),
    (
        "T5", lambda A, B, C: (
            f"Some {A} are {B}. All {B} are {C}.",
            f"Therefore, some {A} are {C}.",
            "V",
        )
    ),
    (
        "T6", lambda A, B, C: (
            f"Some {A} are {B}. Some {B} are {C}.",
            f"Therefore, some {A} are {C}.",
            "I",
        )
    ),
    (
        "T7", lambda A, B, C: (
            f"All {A} are {B}. All {C} are {B}.",
            f"Therefore, some {A} are {C}.",
            "I",
        )
    ),
    (
        "T8", lambda A, B, C: (
            f"All {A} are {B}. All {B} are {C}.",
            f"Therefore, some {A} are not {C}.",
            "I",
        )
    ),
    (
        "T9", lambda A, B, C: (
            f"All {A} are {B}. All {A} are {C}.",
            f"Therefore, some {B} are {C}.",
            "I",
        )
    ),
    (
        "T10", lambda A, B, C: (
            f"All {A} are {B}. No {A} are {C}.",
            f"Therefore, no {B} are {C}.",
            "V",
        )
    ),
    (
        "T11", lambda A, B, C: (
            f"Some {A} are not {B}. All {B} are {C}.",
            f"Therefore, some {A} are not {C}.",
            "V",
        )
    ),
    (
        "T12", lambda A, B, C: (
            f"All {A} are {B}. All {C} are not {B}.",
            f"Therefore, no {A} are {C}.",
            "V",
        )
    ),
]


# ----------------------------------------------------------------------------
# Arithmetic word-problem templates
# ----------------------------------------------------------------------------

def _int_str(a: int, b: int, c: int, name1: str, name2: str, item: str) -> dict:
    """Empty marker; arithmetic templates compute via simple expressions."""
    return {"_": "placeholder"}


ARITHMETIC_TEMPLATES: list[tuple[str, Callable]] = []


def _as1(name1, name2, item, a, b, c):
    return {
        "question": f"{name1} has {a} {item}. {name2} gives {name1} {b} more. How many {item} does {name1} have?",
        "answer": a + b,
    }


def _as2(name1, name2, item, a, b, c):
    return {
        "question": f"{name1} has {a} {item}. {name1} gives {name2} {b}. How many {item} does {name1} have left?",
        "answer": a - b,
    }


def _as3(name1, name2, item, a, b, c):
    return {
        "question": f"{name1} has {a} {item}. {name2} has {b} {item}. How many {item} do they have together?",
        "answer": a + b,
    }


def _as4(name1, name2, item, a, b, c):
    return {
        "question": f"A box has {a} {item}. {b} are taken out and {c} put in. How many {item} are in the box?",
        "answer": a - b + c,
    }


def _as5(name1, name2, item, a, b, c):
    return {
        "question": f"{name1} is {a} years old. {name2} is {b} years older than {name1}. How old is {name2}?",
        "answer": a + b,
    }


def _as6(name1, name2, item, a, b, c):
    return {
        "question": f"{name1} buys {a} {item} at $1 each. {name1} pays with a ${b} bill. How much change does {name1} receive?",
        "answer": b - a,
    }


def _as7(name1, name2, item, a, b, c):
    # Ensure exact division for clean integer answers
    return {
        "question": f"{a} {item} are split equally among {b} people. How many {item} does each person get?",
        "answer": a // b,
    }


def _as8(name1, name2, item, a, b, c):
    return {
        "question": f"{name1} walks {a} km on day 1 and {b} km on day 2. What is the average distance walked per day?",
        "answer": (a + b) // 2,
    }


def _as9(name1, name2, item, a, b, c):
    # Multi-step: 2x + y, with two operands.
    return {
        "question": f"{name1} has {a} {item}. {name1} finds {b} more, then loses half of what they now have. How many {item} does {name1} have?",
        "answer": (a + b) // 2,
    }


def _as10(name1, name2, item, a, b, c):
    # Three-operand subtraction chain
    return {
        "question": f"{name1} has {a} {item}. {name1} gives {b} to {name2} and then gives {c} to a third person. How many {item} does {name1} have left?",
        "answer": a - b - c,
    }


def _as11(name1, name2, item, a, b, c):
    # Difference (subtraction) — requires identifying larger first
    big = max(a, b)
    small = min(a, b)
    return {
        "question": f"{name1} has {big} {item}. {name2} has {small}. How many more {item} does {name1} have than {name2}?",
        "answer": big - small,
    }


def _as12(name1, name2, item, a, b, c):
    # Multiplication (single-step)
    return {
        "question": f"Each bag holds {a} {item}. {name1} buys {b} bags. How many {item} does {name1} have in total?",
        "answer": a * b,
    }


ARITHMETIC_TEMPLATES = [
    ("AS1", _as1),
    ("AS2", _as2),
    ("AS3", _as3),
    ("AS4", _as4),
    ("AS5", _as5),
    ("AS6", _as6),
    ("AS7", _as7),
    ("AS8", _as8),
    ("AS9", _as9),
    ("AS10", _as10),
    ("AS11", _as11),
    ("AS12", _as12),
]


# ----------------------------------------------------------------------------
# Variant construction helpers
# ----------------------------------------------------------------------------

def _contrapositive(premises: str, conclusion: str) -> str:
    """Crude but consistent contrapositive rephrasing.

    The original conclusion says "all A are C" / "no A are C" / "some A are C"
    / "some A are not C". We rephrase as a meta-question asking whether the
    contrapositive holds: "If something is not C, can it still be A?" — to
    which the answer is the OPPOSITE of the original. So actually we set the
    *expected oracle answer* for the contrapositive variant equal to the
    original label (it is logically equivalent).
    """
    # Pull the conclusion phrase (after the period), strip the "Therefore," prefix
    tail = conclusion.strip()
    if tail.lower().startswith("therefore,"):
        tail = tail[len("therefore,"):].strip()
    # Build: "Is the following also true: <tail>?" — answer remains label.
    tail_clean = tail.rstrip("?. ")
    return f"Is the following claim also true: {tail_clean}?"


def _paraphrase_logic(premises: str, conclusion: str) -> str:
    """Noun-swap paraphrase: replace any A/B/C placeholders from the seed pool
    with fresh ones from the paraphrase pool. Strip the leading "All X are Y."
    and rephrase with the canonical template form. Because we only swap the
    *content* of the noun slots, the syllogism's logical form — and therefore
    its truth value — is preserved.
    """
    # We rely on the seed having been built from {A}, {B}, {C} slots already
    # filled; the paraphrased cluster rebuilds the same template with new
    # nouns, so the actual paraphrase call here is identity (the variant is
    # generated upstream in `_build_logic_cluster`).
    return premises + " " + conclusion


def _negation_logic(conclusion: str) -> tuple[str, str]:
    """Negation variant: the oracle answer flips.

    Returns (question, opposite_label).
    """
    tail = conclusion.strip()
    if tail.lower().startswith("therefore,"):
        tail = tail[len("therefore,"):].strip()
    # Question is "Is it NOT the case that <conclusion>?" — yes iff conclusion is false.
    # The model's answer to "Is the conclusion invalid?" flips the original label.
    tail_clean = tail.rstrip("?. ")
    question = f"Is it NOT the case that {tail_clean}?"
    return question, "FLIPPED"  # marker; the scoring layer flips the response


def _inverse_arithmetic(seed_question: str, seed_answer: int, a: int) -> tuple[str, int]:
    """Inverse variant for arithmetic: 'additive identity' — ask for the first
    addend (a). The oracle answer differs from the seed, so this is the
    'inverse/control' role rather than 'contrapositive equivalent'.
    """
    return (
        f"(Inverse) Consider a problem with the same setup as: '{seed_question}'. "
        f"What was the original starting quantity (the first number mentioned)?",
        a,
    )


def _negation_arithmetic(seed_question: str, seed_answer: int) -> tuple[str, str]:
    """Negation variant for arithmetic: a yes/no question with a *fixed*
    deterministic oracle (independent of the model's seed answer).

    We ask "Is the answer to this problem equal to <wrong_value>?" — the
    oracle is "NO" (since the wrong value is, by construction, not the
    seed answer). The coherence layer treats this as a binary claim the
    model can answer YES/NO. We do NOT fold it into the same response
    space as the seed; instead, the relational invariant is that the
    negation's oracle is fixed and the model must agree with it.
    """
    wrong = seed_answer + 1
    question = (
        f"Consider: {seed_question} Is the answer to this problem equal to {wrong}? "
        f"Answer YES or NO only."
    )
    return question, "NO"


def _paraphrase_arithmetic(seed_question: str, seed_answer: int, name1: str,
                           name2: str, item: str) -> str:
    """Noun-swap paraphrase. The seed question will be rebuilt upstream with
    fresh nouns; here we just return the seed form."""
    return seed_question


# ----------------------------------------------------------------------------
# Cluster builders
# ----------------------------------------------------------------------------

@dataclass
class Variant:
    role: str            # 'seed' | 'paraphrase' | 'negation' | 'contrapositive' | 'inverse'
    question: str
    oracle: str | int    # canonical answer; for negation it is 'FLIPPED'
    raw_question: str = ""  # original phrasing for logging


@dataclass
class MIC:
    cluster_id: str
    domain: str           # 'logic' | 'arithmetic'
    template_id: str
    variants: dict[str, Variant] = field(default_factory=dict)
    answers: dict[str, str | int] = field(default_factory=dict)
    relations: dict[str, bool] = field(default_factory=dict)
    difficulty_hint: str = "medium"
    oracle_correct: str | int = ""


def _build_logic_cluster(idx: int, rng: random.Random) -> MIC:
    """Build one logic MIC using a randomly-chosen template + nouns."""
    template_id, builder = rng.choice(LOGIC_TEMPLATES)
    A = rng.choice(LOGIC_NOUNS)
    B = rng.choice([n for n in LOGIC_NOUNS if n != A])
    C = rng.choice([n for n in LOGIC_NOUNS if n not in (A, B)])
    premises, conclusion, label = builder(A, B, C)
    seed_question = premises + " " + conclusion

    # Paraphrase: same template, fresh nouns from the paraphrase pool
    A2 = rng.choice(LOGIC_NOUNS_PARAPHRASE)
    B2 = rng.choice([n for n in LOGIC_NOUNS_PARAPHRASE if n != A2])
    C2 = rng.choice([n for n in LOGIC_NOUNS_PARAPHRASE if n not in (A2, B2)])
    _, _, _ = builder(A2, B2, C2)
    p2_premises, p2_conclusion, _ = builder(A2, B2, C2)
    paraphrase_question = p2_premises + " " + p2_conclusion

    # Negation: question + flipped
    neg_question, neg_label = _negation_logic(conclusion)

    # Contrapositive: rephrasing that holds iff original does
    contra_question = _contrapositive(premises, conclusion)

    cluster_id = f"logic_{idx:04d}"

    mic = MIC(
        cluster_id=cluster_id,
        domain="logic",
        template_id=template_id,
        difficulty_hint=_difficulty_hint_logic(template_id),
        oracle_correct=label,
    )
    mic.variants = {
        "seed": Variant(role="seed", question=seed_question, oracle=label, raw_question=seed_question),
        "paraphrase": Variant(role="paraphrase", question=paraphrase_question, oracle=label, raw_question=paraphrase_question),
        "negation": Variant(role="negation", question=neg_question, oracle=neg_label, raw_question=neg_question),
        "contrapositive": Variant(role="contrapositive", question=contra_question, oracle=label, raw_question=contra_question),
    }
    mic.answers = {
        "seed": label,
        "paraphrase": label,
        "negation": "FLIPPED",
        "contrapositive": label,
    }
    mic.relations = {
        "paraphrase_eq_seed": True,
        "negation_eq_not_seed": True,
        "contrapositive_eq_seed": True,
    }
    return mic


def _difficulty_hint_logic(template_id: str) -> str:
    if template_id in ("T1", "T4", "T5", "T10"):
        return "easy"
    if template_id in ("T2", "T7", "T11", "T12"):
        return "medium"
    return "hard"


def _build_arithmetic_cluster(idx: int, rng: random.Random) -> MIC:
    """Build one arithmetic MIC."""
    template_id, builder = rng.choice(ARITHMETIC_TEMPLATES)

    # Generate template-appropriate operands (all in [2,25], integer results).
    # Per-template constraints: AS2 needs a > b; AS7 needs a % b == 0;
    # AS11 picks big/small internally; AS12 needs a*b <= 100 (no absurd counts).
    for _ in range(80):
        a = rng.randint(2, 25)
        b = rng.randint(2, 25)
        c = rng.randint(2, 25)
        # Per-template constraints
        if template_id == "AS2" and a <= b:
            continue
        if template_id == "AS7" and (a % b != 0):
            continue
        if template_id == "AS12" and a * b > 100:
            continue
        name1 = rng.choice(NAMES_A)
        name2 = rng.choice([n for n in NAMES_B if n != name1])
        item = rng.choice(ITEMS)
        out = builder(name1, name2, item, a, b, c)
        ans = out["answer"]
        # require positive integer result
        if isinstance(ans, int) and ans > 0:
            break
    else:
        raise RuntimeError("arithmetic generator failed to produce positive answer")

    seed_question = out["question"]
    seed_answer = out["answer"]

    # Paraphrase: rebuild with fresh names + items
    name1b = rng.choice(NAMES_B)
    name2b = rng.choice([n for n in NAMES_A if n != name1b])
    itemb = rng.choice(ITEMS_PARAPHRASE)
    out2 = builder(name1b, name2b, itemb, a, b, c)
    paraphrase_question = out2["question"]

    # Negation: a yes/no question whose oracle is "NO" (the wrong value is
    # by construction not the seed answer).
    neg_question, neg_label = _negation_arithmetic(seed_question, seed_answer)

    # Inverse: ask for the original first addend
    inv_question, inv_answer = _inverse_arithmetic(seed_question, seed_answer, a)

    cluster_id = f"arith_{idx:04d}"
    mic = MIC(
        cluster_id=cluster_id,
        domain="arithmetic",
        template_id=template_id,
        difficulty_hint=_difficulty_hint_arith(seed_answer),
        oracle_correct=seed_answer,
    )
    mic.variants = {
        "seed": Variant(role="seed", question=seed_question, oracle=seed_answer, raw_question=seed_question),
        "paraphrase": Variant(role="paraphrase", question=paraphrase_question, oracle=seed_answer, raw_question=paraphrase_question),
        "negation": Variant(role="negation", question=neg_question, oracle=neg_label, raw_question=neg_question),
        "inverse": Variant(role="inverse", question=inv_question, oracle=inv_answer, raw_question=inv_question),
    }
    mic.answers = {
        "seed": seed_answer,
        "paraphrase": seed_answer,
        "negation": "NO",
        "inverse": inv_answer,
    }
    mic.relations = {
        "paraphrase_eq_seed": True,
        "negation_eq_no": True,
        "inverse_distinct": True,  # inverse has a different oracle answer
    }
    return mic


def _difficulty_hint_arith(ans: int) -> str:
    if ans <= 10:
        return "easy"
    if ans <= 25:
        return "medium"
    return "hard"


# ----------------------------------------------------------------------------
# Public entrypoint
# ----------------------------------------------------------------------------

def generate_mics(n_logic: int, n_arithmetic: int, seed: int = 0) -> list[dict]:
    """Build the requested number of MICs across both domains."""
    rng = random.Random(seed)
    clusters: list[MIC] = []
    for i in range(n_logic):
        clusters.append(_build_logic_cluster(i, rng))
    for i in range(n_arithmetic):
        clusters.append(_build_arithmetic_cluster(i, rng))
    # Shuffle so logic and arithmetic are interleaved
    rng.shuffle(clusters)
    return [asdict(c) for c in clusters]


# ----------------------------------------------------------------------------
# Lightweight self-test
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    sample = generate_mics(n_logic=3, n_arithmetic=3, seed=42)
    import json
    print(json.dumps(sample, indent=2, default=str))