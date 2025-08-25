# DEPTH: Hallucination-Free Relation Extraction via Dependency-Aware   Sentence Simplification and Two-tiered Hierarchical Refinement

Relation extraction enables the construction of structured knowledge for many
downstream applications. While large language models (LLMs) have shown great
promise in this domain, most existing methods concentrate on relation
classification, which predicts the semantic relation type between a related
entity pair. However, we observe that LLMs often struggle to reliably determine
whether a relation exists, especially in cases involving complex sentence
structures or intricate semantics, which leads to spurious predictions. Such
hallucinations can introduce noisy edges in knowledge graphs, compromising the
integrity of structured knowledge and downstream reliability. To address these
challenges, we propose DEPTH, a framework that integrates Dependency-aware
sEntence simPlification and Two-tiered Hierarchical refinement into the
relation extraction pipeline. Given a sentence and its candidate entity pairs,
DEPTH operates in two stages: (1) the Grounding module extracts relations for
each pair by leveraging their shortest dependency path, distilling the sentence
into a minimal yet coherent relational context that reduces syntactic noise
while preserving key semantics; (2) the Refinement module aggregates all local
predictions and revises them based on a holistic understanding of the sentence,
correcting omissions and inconsistencies. We further introduce a
causality-driven reward model that mitigates reward hacking by disentangling
spurious correlations, enabling robust fine-tuning via reinforcement learning
with human feedback. Experiments on six benchmarks demonstrate that DEPTH
reduces the average hallucination rate to 7.0\% while achieving a 17.2\%
improvement in average F1 score over state-of-the-art baselines.

链接: http://arxiv.org/pdf/2508.14391v1
