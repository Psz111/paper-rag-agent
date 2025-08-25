# GSFix3D: Diffusion-Guided Repair of Novel Views in Gaussian Splatting

Recent developments in 3D Gaussian Splatting have significantly enhanced
novel view synthesis, yet generating high-quality renderings from extreme novel
viewpoints or partially observed regions remains challenging. Meanwhile,
diffusion models exhibit strong generative capabilities, but their reliance on
text prompts and lack of awareness of specific scene information hinder
accurate 3D reconstruction tasks. To address these limitations, we introduce
GSFix3D, a novel framework that improves the visual fidelity in
under-constrained regions by distilling prior knowledge from diffusion models
into 3D representations, while preserving consistency with observed scene
details. At its core is GSFixer, a latent diffusion model obtained via our
customized fine-tuning protocol that can leverage both mesh and 3D Gaussians to
adapt pretrained generative models to a variety of environments and artifact
types from different reconstruction methods, enabling robust novel view repair
for unseen camera poses. Moreover, we propose a random mask augmentation
strategy that empowers GSFixer to plausibly inpaint missing regions.
Experiments on challenging benchmarks demonstrate that our GSFix3D and GSFixer
achieve state-of-the-art performance, requiring only minimal scene-specific
fine-tuning on captured data. Real-world test further confirms its resilience
to potential pose errors. Our code and data will be made publicly available.
Project page: https://gsfix3d.github.io.

链接: http://arxiv.org/pdf/2508.14717v1
