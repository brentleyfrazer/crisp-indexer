# Mrs Crisp: Dynamic E-Prime Semantic Indexer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://img.shields.io/badge/DOI-10.25904%2F1912%2F527-blue.svg)](https://dx.doi.org/10.25904/1912/527)

A deterministic semantic parser designed to enforce **English Prime (E-Prime)** constraints, eliminate passive copular nominalization, and compute agency metrics for natural language.

Developed from doctoral research conducted at Griffith University by **Dr. Brentley Frazer**, *Mrs Crisp* served as the algorithmic verification engine for *Scoundrel Days* (UQP, 2017)—the first creative longform work in literary history composed entirely in 100% E-Prime.

---

## Theoretical Framework

Standard English relies heavily on the copula (*to be*), which introduces two structural flaws:
1. **The "Is of Identity"** ($X \text{ is } Y$): Falsely equates a subject with a label, bypassing context and perception.
2. **The "Is of Predication"** ($X \text{ is } \text{cold}$): Projects internal subjective perception onto objective external reality.

In human writing, reliance on the copula leads to passive, frozen prose. In generative language models (LLMs), copular predication contributes significantly to **ontological hallucinations**—assigning unjustified truth-values to probabilistic associations.

*Mrs Crisp* enforces active agency by stripping away the copula and evaluating the text along two mathematical vectors:
* **Bourland Crispiness Index ($I_C$)**: The ratio of copula-free sentences to total sentences ($I_C = \frac{S_{\text{crispy}}}{S_{\text{total}}}$).
* **Copula Density ($D_C$)**: The absolute frequency percentage of copular tokens relative to the total lexicon.

---

## Quickstart

```python
from crisp_indexer import CrispIndexer

indexer = CrispIndexer()
text = "The system runs smoothly. It processes every record without delay."

results = indexer.analyze(text)

print(f"Crispiness Index: {results['crispiness_index']}") # 1.0
print(f"100% E-Prime: {results['is_100_percent_eprime']}") # True