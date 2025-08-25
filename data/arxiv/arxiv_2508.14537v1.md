# WISE-FUSE: Efficient Whole Slide Image Encoding via Coarse-to-Fine Patch   Selection with VLM and LLM Knowledge Fusion

Whole slide images (WSIs) in computational pathology (CPath) pose a major
computational challenge due to their gigapixel scale, often requiring the
processing of tens to hundreds of thousands of high-resolution patches per
slide. This results in prohibitive encoding costs, with preprocessing and
training times extending to days or even weeks-making WSI encoding the most
significant bottleneck in real-world deployment. In this work, we propose
WISE-FUSE, an adaptive WSI encoding framework that leverages pathology-domain
vision-language models and large language models to address this challenge by
selectively processing diagnostically relevant regions. WISE-FUSE first
computes similarity scores between low-resolution patches and class-specific
textual descriptions using a knowledge distillation mechanism that preserves
fine-grained diagnostic features. Based on these similarity scores, we select a
small subset of informative regions for the target task, which quickly
eliminates irrelevant patches at the coarse level. The corresponding
high-resolution patches are then selectively encoded and fused with textual
embeddings to reinforce diagnostic context. Extensive experiments demonstrate
that WISE-FUSE reduces WSI encoding time by over threefold while achieving
diagnostic performance comparable to or surpassing that of exhaustive patch
processing, offering a scalable and practical solution for CPath.

链接: http://arxiv.org/pdf/2508.14537v1
