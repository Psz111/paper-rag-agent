# Semantic Energy: Detecting LLM Hallucination Beyond Entropy

Large Language Models (LLMs) are being increasingly deployed in real-world
applications, but they remain susceptible to hallucinations, which produce
fluent yet incorrect responses and lead to erroneous decision-making.
Uncertainty estimation is a feasible approach to detect such hallucinations.
For example, semantic entropy estimates uncertainty by considering the semantic
diversity across multiple sampled responses, thus identifying hallucinations.
However, semantic entropy relies on post-softmax probabilities and fails to
capture the model's inherent uncertainty, causing it to be ineffective in
certain scenarios. To address this issue, we introduce Semantic Energy, a novel
uncertainty estimation framework that leverages the inherent confidence of LLMs
by operating directly on logits of penultimate layer. By combining semantic
clustering with a Boltzmann-inspired energy distribution, our method better
captures uncertainty in cases where semantic entropy fails. Experiments across
multiple benchmarks show that Semantic Energy significantly improves
hallucination detection and uncertainty estimation, offering more reliable
signals for downstream applications such as hallucination detection.

链接: http://arxiv.org/pdf/2508.14496v1
