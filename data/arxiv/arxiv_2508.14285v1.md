# Amortized Bayesian Meta-Learning for Low-Rank Adaptation of Large   Language Models

Fine-tuning large language models (LLMs) with low-rank adaptaion (LoRA) is a
cost-effective way to incorporate information from a specific dataset. However,
it is often unclear how well the fine-tuned LLM will generalize, i.e., how well
it will perform on unseen datasets. Methods have been proposed to improve
generalization by optimizing with in-context prompts, or by using meta-learning
to fine-tune LLMs. However, these methods are expensive in memory and
computation, requiring either long-context prompts or saving copies of
parameters and using second-order gradient updates. To address these
challenges, we propose Amortized Bayesian Meta-Learning for LoRA (ABMLL). This
method builds on amortized Bayesian meta-learning for smaller models, adapting
this approach to LLMs while maintaining its computational efficiency. We
reframe task-specific and global parameters in the context of LoRA and use a
set of new hyperparameters to balance reconstruction accuracy and the fidelity
of task-specific parameters to the global ones. ABMLL provides effective
generalization and scales to large models such as Llama3-8B. Furthermore, as a
result of using a Bayesian framework, ABMLL provides improved uncertainty
quantification. We test ABMLL on Unified-QA and CrossFit datasets and find that
it outperforms existing methods on these benchmarks in terms of both accuracy
and expected calibration error.

链接: http://arxiv.org/pdf/2508.14285v1
