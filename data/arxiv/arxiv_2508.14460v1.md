# DuPO: Enabling Reliable LLM Self-Verification via Dual Preference   Optimization

We present DuPO, a dual learning-based preference optimization framework that
generates annotation-free feedback via a generalized duality. DuPO addresses
two key limitations: Reinforcement Learning with Verifiable Rewards (RLVR)'s
reliance on costly labels and applicability restricted to verifiable tasks, and
traditional dual learning's restriction to strictly dual task pairs (e.g.,
translation and back-translation). Specifically, DuPO decomposes a primal
task's input into known and unknown components, then constructs its dual task
to reconstruct the unknown part using the primal output and known information
(e.g., reversing math solutions to recover hidden variables), broadening
applicability to non-invertible tasks. The quality of this reconstruction
serves as a self-supervised reward to optimize the primal task, synergizing
with LLMs' ability to instantiate both tasks via a single model. Empirically,
DuPO achieves substantial gains across diverse tasks: it enhances the average
translation quality by 2.13 COMET over 756 directions, boosts the mathematical
reasoning accuracy by an average of 6.4 points on three challenge benchmarks,
and enhances performance by 9.3 points as an inference-time reranker (trading
computation for accuracy). These results position DuPO as a scalable, general,
and annotation-free paradigm for LLM optimization.

链接: http://arxiv.org/pdf/2508.14460v1
