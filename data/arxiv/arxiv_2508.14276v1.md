# Tooth-Diffusion: Guided 3D CBCT Synthesis with Fine-Grained Tooth   Conditioning

Despite the growing importance of dental CBCT scans for diagnosis and
treatment planning, generating anatomically realistic scans with fine-grained
control remains a challenge in medical image synthesis. In this work, we
propose a novel conditional diffusion framework for 3D dental volume
generation, guided by tooth-level binary attributes that allow precise control
over tooth presence and configuration. Our approach integrates wavelet-based
denoising diffusion, FiLM conditioning, and masked loss functions to focus
learning on relevant anatomical structures. We evaluate the model across
diverse tasks, such as tooth addition, removal, and full dentition synthesis,
using both paired and distributional similarity metrics. Results show strong
fidelity and generalization with low FID scores, robust inpainting performance,
and SSIM values above 0.91 even on unseen scans. By enabling realistic,
localized modification of dentition without rescanning, this work opens
opportunities for surgical planning, patient communication, and targeted data
augmentation in dental AI workflows. The codes are available at:
https://github.com/djafar1/tooth-diffusion.

链接: http://arxiv.org/pdf/2508.14276v1
