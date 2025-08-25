# Squeezed Diffusion Models

Diffusion models typically inject isotropic Gaussian noise, disregarding
structure in the data. Motivated by the way quantum squeezed states
redistribute uncertainty according to the Heisenberg uncertainty principle, we
introduce Squeezed Diffusion Models (SDM), which scale noise anisotropically
along the principal component of the training distribution. As squeezing
enhances the signal-to-noise ratio in physics, we hypothesize that scaling
noise in a data-dependent manner can better assist diffusion models in learning
important data features. We study two configurations: (i) a Heisenberg
diffusion model that compensates the scaling on the principal axis with inverse
scaling on orthogonal directions and (ii) a standard SDM variant that scales
only the principal axis. Counterintuitively, on CIFAR-10/100 and CelebA-64,
mild antisqueezing - i.e. increasing variance on the principal axis -
consistently improves FID by up to 15% and shifts the precision-recall frontier
toward higher recall. Our results demonstrate that simple, data-aware noise
shaping can deliver robust generative gains without architectural changes.

链接: http://arxiv.org/pdf/2508.14871v1
