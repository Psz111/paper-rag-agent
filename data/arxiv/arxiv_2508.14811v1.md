# Tinker: Diffusion's Gift to 3D--Multi-View Consistent Editing From   Sparse Inputs without Per-Scene Optimization

We introduce Tinker, a versatile framework for high-fidelity 3D editing that
operates in both one-shot and few-shot regimes without any per-scene
finetuning. Unlike prior techniques that demand extensive per-scene
optimization to ensure multi-view consistency or to produce dozens of
consistent edited input views, Tinker delivers robust, multi-view consistent
edits from as few as one or two images. This capability stems from repurposing
pretrained diffusion models, which unlocks their latent 3D awareness. To drive
research in this space, we curate the first large-scale multi-view editing
dataset and data pipeline, spanning diverse scenes and styles. Building on this
dataset, we develop our framework capable of generating multi-view consistent
edited views without per-scene training, which consists of two novel
components: (1) Referring multi-view editor: Enables precise, reference-driven
edits that remain coherent across all viewpoints. (2) Any-view-to-video
synthesizer: Leverages spatial-temporal priors from video diffusion to perform
high-quality scene completion and novel-view generation even from sparse
inputs. Through extensive experiments, Tinker significantly reduces the barrier
to generalizable 3D content creation, achieving state-of-the-art performance on
editing, novel-view synthesis, and rendering enhancement tasks. We believe that
Tinker represents a key step towards truly scalable, zero-shot 3D editing.
Project webpage: https://aim-uofa.github.io/Tinker

链接: http://arxiv.org/pdf/2508.14811v1
