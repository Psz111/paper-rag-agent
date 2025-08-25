# Credence Calibration Game? Calibrating Large Language Models through   Structured Play

As Large Language Models (LLMs) are increasingly deployed in
decision-critical domains, it becomes essential to ensure that their confidence
estimates faithfully correspond to their actual correctness. Existing
calibration methods have primarily focused on post-hoc adjustments or auxiliary
model training; however, many of these approaches necessitate additional
supervision or parameter updates. In this work, we propose a novel prompt-based
calibration framework inspired by the Credence Calibration Game. Our method
establishes a structured interaction loop wherein LLMs receive feedback based
on the alignment of their predicted confidence with correctness. Through
feedback-driven prompting and natural language summaries of prior performance,
our framework dynamically improves model calibration. Extensive experiments
across models and game configurations demonstrate consistent improvements in
evaluation metrics. Our results highlight the potential of game-based prompting
as an effective strategy for LLM calibration. Code and data are available at
https://anonymous.4open.science/r/LLM-Calibration/.

链接: http://arxiv.org/pdf/2508.14390v1
