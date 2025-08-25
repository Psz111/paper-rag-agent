# GOGS: High-Fidelity Geometry and Relighting for Glossy Objects via   Gaussian Surfels

Inverse rendering of glossy objects from RGB imagery remains fundamentally
limited by inherent ambiguity. Although NeRF-based methods achieve
high-fidelity reconstruction via dense-ray sampling, their computational cost
is prohibitive. Recent 3D Gaussian Splatting achieves high reconstruction
efficiency but exhibits limitations under specular reflections. Multi-view
inconsistencies introduce high-frequency surface noise and structural
artifacts, while simplified rendering equations obscure material properties,
leading to implausible relighting results. To address these issues, we propose
GOGS, a novel two-stage framework based on 2D Gaussian surfels. First, we
establish robust surface reconstruction through physics-based rendering with
split-sum approximation, enhanced by geometric priors from foundation models.
Second, we perform material decomposition by leveraging Monte Carlo importance
sampling of the full rendering equation, modeling indirect illumination via
differentiable 2D Gaussian ray tracing and refining high-frequency specular
details through spherical mipmap-based directional encoding that captures
anisotropic highlights. Extensive experiments demonstrate state-of-the-art
performance in geometry reconstruction, material separation, and photorealistic
relighting under novel illuminations, outperforming existing inverse rendering
approaches.

链接: http://arxiv.org/pdf/2508.14563v1
