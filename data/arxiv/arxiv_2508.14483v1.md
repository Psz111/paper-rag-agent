# Vivid-VR: Distilling Concepts from Text-to-Video Diffusion Transformer   for Photorealistic Video Restoration

We present Vivid-VR, a DiT-based generative video restoration method built
upon an advanced T2V foundation model, where ControlNet is leveraged to control
the generation process, ensuring content consistency. However, conventional
fine-tuning of such controllable pipelines frequently suffers from distribution
drift due to limitations in imperfect multimodal alignment, resulting in
compromised texture realism and temporal coherence. To tackle this challenge,
we propose a concept distillation training strategy that utilizes the
pretrained T2V model to synthesize training samples with embedded textual
concepts, thereby distilling its conceptual understanding to preserve texture
and temporal quality. To enhance generation controllability, we redesign the
control architecture with two key components: 1) a control feature projector
that filters degradation artifacts from input video latents to minimize their
propagation through the generation pipeline, and 2) a new ControlNet connector
employing a dual-branch design. This connector synergistically combines
MLP-based feature mapping with cross-attention mechanism for dynamic control
feature retrieval, enabling both content preservation and adaptive control
signal modulation. Extensive experiments show that Vivid-VR performs favorably
against existing approaches on both synthetic and real-world benchmarks, as
well as AIGC videos, achieving impressive texture realism, visual vividness,
and temporal consistency. The codes and checkpoints are publicly available at
https://github.com/csbhr/Vivid-VR.

链接: http://arxiv.org/pdf/2508.14483v1
