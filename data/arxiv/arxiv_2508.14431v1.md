# HyperDiff: Hypergraph Guided Diffusion Model for 3D Human Pose   Estimation

Monocular 3D human pose estimation (HPE) often encounters challenges such as
depth ambiguity and occlusion during the 2D-to-3D lifting process.
Additionally, traditional methods may overlook multi-scale skeleton features
when utilizing skeleton structure information, which can negatively impact the
accuracy of pose estimation. To address these challenges, this paper introduces
a novel 3D pose estimation method, HyperDiff, which integrates diffusion models
with HyperGCN. The diffusion model effectively captures data uncertainty,
alleviating depth ambiguity and occlusion. Meanwhile, HyperGCN, serving as a
denoiser, employs multi-granularity structures to accurately model high-order
correlations between joints. This improves the model's denoising capability
especially for complex poses. Experimental results demonstrate that HyperDiff
achieves state-of-the-art performance on the Human3.6M and MPI-INF-3DHP
datasets and can flexibly adapt to varying computational resources to balance
performance and efficiency.

链接: http://arxiv.org/pdf/2508.14431v1
