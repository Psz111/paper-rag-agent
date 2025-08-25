# FOCUS: Frequency-Optimized Conditioning of DiffUSion Models for   mitigating catastrophic forgetting during Test-Time Adaptation

Test-time adaptation enables models to adapt to evolving domains. However,
balancing the tradeoff between preserving knowledge and adapting to domain
shifts remains challenging for model adaptation methods, since adapting to
domain shifts can induce forgetting of task-relevant knowledge. To address this
problem, we propose FOCUS, a novel frequency-based conditioning approach within
a diffusion-driven input-adaptation framework. Utilising learned, spatially
adaptive frequency priors, our approach conditions the reverse steps during
diffusion-driven denoising to preserve task-relevant semantic information for
dense prediction.
  FOCUS leverages a trained, lightweight, Y-shaped Frequency Prediction Network
(Y-FPN) that disentangles high and low frequency information from noisy images.
This minimizes the computational costs involved in implementing our approach in
a diffusion-driven framework. We train Y-FPN with FrequencyMix, a novel data
augmentation method that perturbs the images across diverse frequency bands,
which improves the robustness of our approach to diverse corruptions.
  We demonstrate the effectiveness of FOCUS for semantic segmentation and
monocular depth estimation across 15 corruption types and three datasets,
achieving state-of-the-art averaged performance. In addition to improving
standalone performance, FOCUS complements existing model adaptation methods
since we can derive pseudo labels from FOCUS-denoised images for additional
supervision. Even under limited, intermittent supervision with the pseudo
labels derived from the FOCUS denoised images, we show that FOCUS mitigates
catastrophic forgetting for recent model adaptation methods.

链接: http://arxiv.org/pdf/2508.14437v1
