# SATURN: Autoregressive Image Generation Guided by Scene Graphs

State-of-the-art text-to-image models excel at photorealistic rendering but
often struggle to capture the layout and object relationships implied by
complex prompts. Scene graphs provide a natural structural prior, yet previous
graph-guided approaches have typically relied on heavy GAN or diffusion
pipelines, which lag behind modern autoregressive architectures in both speed
and fidelity. We introduce SATURN (Structured Arrangement of Triplets for
Unified Rendering Networks), a lightweight extension to VAR-CLIP that
translates a scene graph into a salience-ordered token sequence, enabling a
frozen CLIP-VQ-VAE backbone to interpret graph structure while fine-tuning only
the VAR transformer. On the Visual Genome dataset, SATURN reduces FID from
56.45% to 21.62% and increases the Inception Score from 16.03 to 24.78,
outperforming prior methods such as SG2IM and SGDiff without requiring extra
modules or multi-stage training. Qualitative results further confirm
improvements in object count fidelity and spatial relation accuracy, showing
that SATURN effectively combines structural awareness with state-of-the-art
autoregressive fidelity.

链接: http://arxiv.org/pdf/2508.14502v1
