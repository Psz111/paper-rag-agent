# Universal and Transferable Adversarial Attack on Large Language Models   Using Exponentiated Gradient Descent

As large language models (LLMs) are increasingly deployed in critical
applications, ensuring their robustness and safety alignment remains a major
challenge. Despite the overall success of alignment techniques such as
reinforcement learning from human feedback (RLHF) on typical prompts, LLMs
remain vulnerable to jailbreak attacks enabled by crafted adversarial triggers
appended to user prompts. Most existing jailbreak methods either rely on
inefficient searches over discrete token spaces or direct optimization of
continuous embeddings. While continuous embeddings can be given directly to
selected open-source models as input, doing so is not feasible for proprietary
models. On the other hand, projecting these embeddings back into valid discrete
tokens introduces additional complexity and often reduces attack effectiveness.
We propose an intrinsic optimization method which directly optimizes relaxed
one-hot encodings of the adversarial suffix tokens using exponentiated gradient
descent coupled with Bregman projection, ensuring that the optimized one-hot
encoding of each token always remains within the probability simplex. We
provide theoretical proof of convergence for our proposed method and implement
an efficient algorithm that effectively jailbreaks several widely used LLMs.
Our method achieves higher success rates and faster convergence compared to
three state-of-the-art baselines, evaluated on five open-source LLMs and four
adversarial behavior datasets curated for evaluating jailbreak methods. In
addition to individual prompt attacks, we also generate universal adversarial
suffixes effective across multiple prompts and demonstrate transferability of
optimized suffixes to different LLMs.

链接: http://arxiv.org/pdf/2508.14853v1
