# Ouroboros: Single-step Diffusion Models for Cycle-consistent Forward and   Inverse Rendering

While multi-step diffusion models have advanced both forward and inverse
rendering, existing approaches often treat these problems independently,
leading to cycle inconsistency and slow inference speed. In this work, we
present Ouroboros, a framework composed of two single-step diffusion models
that handle forward and inverse rendering with mutual reinforcement. Our
approach extends intrinsic decomposition to both indoor and outdoor scenes and
introduces a cycle consistency mechanism that ensures coherence between forward
and inverse rendering outputs. Experimental results demonstrate
state-of-the-art performance across diverse scenes while achieving
substantially faster inference speed compared to other diffusion-based methods.
We also demonstrate that Ouroboros can transfer to video decomposition in a
training-free manner, reducing temporal inconsistency in video sequences while
maintaining high-quality per-frame inverse rendering.

链接: http://arxiv.org/pdf/2508.14461v1
