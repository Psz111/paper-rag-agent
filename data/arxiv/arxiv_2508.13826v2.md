# Latent Interpolation Learning Using Diffusion Models for Cardiac Volume   Reconstruction

Cardiac Magnetic Resonance (CMR) imaging is a critical tool for diagnosing
and managing cardiovascular disease, yet its utility is often limited by the
sparse acquisition of 2D short-axis slices, resulting in incomplete volumetric
information. Accurate 3D reconstruction from these sparse slices is essential
for comprehensive cardiac assessment, but existing methods face challenges,
including reliance on predefined interpolation schemes (e.g., linear or
spherical), computational inefficiency, and dependence on additional semantic
inputs such as segmentation labels or motion data. To address these
limitations, we propose a novel \textbf{Ca}rdiac \textbf{L}atent
\textbf{I}nterpolation \textbf{D}iffusion (CaLID) framework that introduces
three key innovations. First, we present a data-driven interpolation scheme
based on diffusion models, which can capture complex, non-linear relationships
between sparse slices and improves reconstruction accuracy. Second, we design a
computationally efficient method that operates in the latent space and speeds
up 3D whole-heart upsampling time by a factor of 24, reducing computational
overhead compared to previous methods. Third, with only sparse 2D CMR images as
input, our method achieves SOTA performance against baseline methods,
eliminating the need for auxiliary input such as morphological guidance, thus
simplifying workflows. We further extend our method to 2D+T data, enabling the
effective modeling of spatiotemporal dynamics and ensuring temporal coherence.
Extensive volumetric evaluations and downstream segmentation tasks demonstrate
that CaLID achieves superior reconstruction quality and efficiency. By
addressing the fundamental limitations of existing approaches, our framework
advances the state of the art for spatio and spatiotemporal whole-heart
reconstruction, offering a robust and clinically practical solution for
cardiovascular imaging.

链接: http://arxiv.org/pdf/2508.13826v2
