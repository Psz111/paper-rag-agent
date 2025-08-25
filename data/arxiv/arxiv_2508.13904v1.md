# Revisiting Diffusion Q-Learning: From Iterative Denoising to One-Step   Action Generation

The generative power of diffusion models (DMs) has recently enabled
high-performing decision-making algorithms in offline reinforcement learning
(RL), achieving state-of-the-art results across standard benchmarks. Among
them, Diffusion Q-Learning (DQL) stands out as a leading method for its
consistently strong performance. Nevertheless, DQL remains limited in practice
due to its reliance on multi-step denoising for action generation during both
training and inference. Although one-step denoising is desirable, simply
applying it to DQL leads to a drastic performance drop. In this work, we
revisit DQL and identify its core limitations. We then propose One-Step Flow
Q-Learning (OFQL), a novel framework that enables efficient one-step action
generation during both training and inference, without requiring auxiliary
models, distillation, or multi-phase training. Specifically, OFQL reformulates
DQL within the sample-efficient Flow Matching (FM) framework. While
conventional FM induces curved generative trajectories that impede one-step
generation, OFQL instead learns an average velocity field that facilitates
direct, accurate action generation. Collectively, OFQL eliminates the need for
multi-step sampling and recursive gradient updates in DQL, resulting in faster
and more robust training and inference. Extensive experiments on the D4RL
benchmark demonstrate that OFQL outperforms DQL and other diffusion-based
baselines, while substantially reducing both training and inference time
compared to DQL.

链接: http://arxiv.org/pdf/2508.13904v1
