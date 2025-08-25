# Cross-Modality Controlled Molecule Generation with Diffusion Language   Model

Current SMILES-based diffusion models for molecule generation typically
support only unimodal constraint. They inject conditioning signals at the start
of the training process and require retraining a new model from scratch
whenever the constraint changes. However, real-world applications often involve
multiple constraints across different modalities, and additional constraints
may emerge over the course of a study. This raises a challenge: how to extend a
pre-trained diffusion model not only to support cross-modality constraints but
also to incorporate new ones without retraining. To tackle this problem, we
propose the Cross-Modality Controlled Molecule Generation with Diffusion
Language Model (CMCM-DLM), demonstrated by two distinct cross modalities:
molecular structure and chemical properties. Our approach builds upon a
pre-trained diffusion model, incorporating two trainable modules, the Structure
Control Module (SCM) and the Property Control Module (PCM), and operates in two
distinct phases during the generation process. In Phase I, we employs the SCM
to inject structural constraints during the early diffusion steps, effectively
anchoring the molecular backbone. Phase II builds on this by further
introducing PCM to guide the later stages of inference to refine the generated
molecules, ensuring their chemical properties match the specified targets.
Experimental results on multiple datasets demonstrate the efficiency and
adaptability of our approach, highlighting CMCM-DLM's significant advancement
in molecular generation for drug discovery applications.

链接: http://arxiv.org/pdf/2508.14748v1
