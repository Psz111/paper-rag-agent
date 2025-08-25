# MUSE: Multi-Subject Unified Synthesis via Explicit Layout Semantic   Expansion

Existing text-to-image diffusion models have demonstrated remarkable
capabilities in generating high-quality images guided by textual prompts.
However, achieving multi-subject compositional synthesis with precise spatial
control remains a significant challenge. In this work, we address the task of
layout-controllable multi-subject synthesis (LMS), which requires both faithful
reconstruction of reference subjects and their accurate placement in specified
regions within a unified image. While recent advancements have separately
improved layout control and subject synthesis, existing approaches struggle to
simultaneously satisfy the dual requirements of spatial precision and identity
preservation in this composite task. To bridge this gap, we propose MUSE, a
unified synthesis framework that employs concatenated cross-attention (CCA) to
seamlessly integrate layout specifications with textual guidance through
explicit semantic space expansion. The proposed CCA mechanism enables
bidirectional modality alignment between spatial constraints and textual
descriptions without interference. Furthermore, we design a progressive
two-stage training strategy that decomposes the LMS task into learnable
sub-objectives for effective optimization. Extensive experiments demonstrate
that MUSE achieves zero-shot end-to-end generation with superior spatial
accuracy and identity consistency compared to existing solutions, advancing the
frontier of controllable image synthesis. Our code and model are available at
https://github.com/pf0607/MUSE.

链接: http://arxiv.org/pdf/2508.14440v1
