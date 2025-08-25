# Transplant Then Regenerate: A New Paradigm for Text Data Augmentation

Data augmentation is a critical technique in deep learning. Traditional
methods like Back-translation typically focus on lexical-level rephrasing,
which primarily produces variations with the same semantics. While large
language models (LLMs) have enhanced text augmentation by their "knowledge
emergence" capability, controlling the style and structure of these outputs
remains challenging and requires meticulous prompt engineering. In this paper,
we propose LMTransplant, a novel text augmentation paradigm leveraging LLMs.
The core idea of LMTransplant is transplant-then-regenerate: incorporating seed
text into a context expanded by LLM, and asking the LLM to regenerate a variant
based on the expanded context. This strategy allows the model to create more
diverse and creative content-level variants by fully leveraging the knowledge
embedded in LLMs, while preserving the core attributes of the original text. We
evaluate LMTransplant across various text-related tasks, demonstrating its
superior performance over existing text augmentation methods. Moreover,
LMTransplant demonstrates exceptional scalability as the size of augmented data
grows.

链接: http://arxiv.org/pdf/2508.14723v1
