# SAGA: Learning Signal-Aligned Distributions for Improved Text-to-Image   Generation

State-of-the-art text-to-image models produce visually impressive results but
often struggle with precise alignment to text prompts, leading to missing
critical elements or unintended blending of distinct concepts. We propose a
novel approach that learns a high-success-rate distribution conditioned on a
target prompt, ensuring that generated images faithfully reflect the
corresponding prompts. Our method explicitly models the signal component during
the denoising process, offering fine-grained control that mitigates
over-optimization and out-of-distribution artifacts. Moreover, our framework is
training-free and seamlessly integrates with both existing diffusion and flow
matching architectures. It also supports additional conditioning modalities --
such as bounding boxes -- for enhanced spatial alignment. Extensive experiments
demonstrate that our approach outperforms current state-of-the-art methods. The
code is available at https://github.com/grimalPaul/gsn-factory.

链接: http://arxiv.org/pdf/2508.13866v1
