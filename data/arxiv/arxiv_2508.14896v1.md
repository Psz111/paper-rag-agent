# Quantization Meets dLLMs: A Systematic Study of Post-training   Quantization for Diffusion LLMs

Recent advances in diffusion large language models (dLLMs) have introduced a
promising alternative to autoregressive (AR) LLMs for natural language
generation tasks, leveraging full attention and denoising-based decoding
strategies. However, the deployment of these models on edge devices remains
challenging due to their massive parameter scale and high resource demands.
While post-training quantization (PTQ) has emerged as a widely adopted
technique for compressing AR LLMs, its applicability to dLLMs remains largely
unexplored. In this work, we present the first systematic study on quantizing
diffusion-based language models. We begin by identifying the presence of
activation outliers, characterized by abnormally large activation values that
dominate the dynamic range. These outliers pose a key challenge to low-bit
quantization, as they make it difficult to preserve precision for the majority
of values. More importantly, we implement state-of-the-art PTQ methods and
conduct a comprehensive evaluation across multiple task types and model
variants. Our analysis is structured along four key dimensions: bit-width,
quantization method, task category, and model type. Through this
multi-perspective evaluation, we offer practical insights into the quantization
behavior of dLLMs under different configurations. We hope our findings provide
a foundation for future research in efficient dLLM deployment. All codes and
experimental setups will be released to support the community.

链接: http://arxiv.org/pdf/2508.14896v1
