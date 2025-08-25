# Physics-Constrained Diffusion Reconstruction with Posterior Correction   for Quantitative and Fast PET Imaging

Deep learning-based reconstruction of positron emission tomography(PET) data
has gained increasing attention in recent years. While these methods achieve
fast reconstruction,concerns remain regarding quantitative accuracy and the
presence of artifacts,stemming from limited model interpretability,data driven
dependence, and overfitting risks.These challenges have hindered clinical
adoption.To address them,we propose a conditional diffusion model with
posterior physical correction (PET-DPC) for PET image reconstruction. An
innovative normalization procedure generates the input Geometric TOF
Probabilistic Image (GTP-image),while physical information is incorporated
during the diffusion sampling process to perform posterior
scatter,attenuation,and random corrections. The model was trained and validated
on 300 brain and 50 whole-body PET datasets,a physical phantom,and 20 simulated
brain datasets. PET-DPC produced reconstructions closely aligned with fully
corrected OSEM images,outperforming end-to-end deep learning models in
quantitative metrics and,in some cases, surpassing traditional iterative
methods. The model also generalized well to out-of-distribution(OOD) data.
Compared to iterative methods,PET-DPC reduced reconstruction time by 50% for
brain scans and 85% for whole-body scans. Ablation studies confirmed the
critical role of posterior correction in implementing scatter and attenuation
corrections,enhancing reconstruction accuracy. Experiments with physical
phantoms further demonstrated PET-DPC's ability to preserve background
uniformity and accurately reproduce tumor-to-background intensity ratios.
Overall,these results highlight PET-DPC as a promising approach for rapid,
quantitatively accurate PET reconstruction,with strong potential to improve
clinical imaging workflows.

链接: http://arxiv.org/pdf/2508.14364v1
