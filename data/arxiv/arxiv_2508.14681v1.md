# Virtual Multiplex Staining for Histological Images using a Marker-wise   Conditioned Diffusion Model

Multiplex imaging is revolutionizing pathology by enabling the simultaneous
visualization of multiple biomarkers within tissue samples, providing
molecular-level insights that traditional hematoxylin and eosin (H&E) staining
cannot provide. However, the complexity and cost of multiplex data acquisition
have hindered its widespread adoption. Additionally, most existing large
repositories of H&E images lack corresponding multiplex images, limiting
opportunities for multimodal analysis. To address these challenges, we leverage
recent advances in latent diffusion models (LDMs), which excel at modeling
complex data distributions utilizing their powerful priors for fine-tuning to a
target domain. In this paper, we introduce a novel framework for virtual
multiplex staining that utilizes pretrained LDM parameters to generate
multiplex images from H&E images using a conditional diffusion model. Our
approach enables marker-by-marker generation by conditioning the diffusion
model on each marker, while sharing the same architecture across all markers.
To tackle the challenge of varying pixel value distributions across different
marker stains and to improve inference speed, we fine-tune the model for
single-step sampling, enhancing both color contrast fidelity and inference
efficiency through pixel-level loss functions. We validate our framework on two
publicly available datasets, notably demonstrating its effectiveness in
generating up to 18 different marker types with improved accuracy, a
substantial increase over the 2-3 marker types achieved in previous approaches.
This validation highlights the potential of our framework, pioneering virtual
multiplex staining. Finally, this paper bridges the gap between H&E and
multiplex imaging, potentially enabling retrospective studies and large-scale
analyses of existing H&E image repositories.

链接: http://arxiv.org/pdf/2508.14681v1
