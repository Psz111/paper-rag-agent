# DPad: Efficient Diffusion Language Models with Suffix Dropout

Diffusion-based Large Language Models (dLLMs) parallelize text generation by
framing decoding as a denoising process, but suffer from high computational
overhead since they predict all future suffix tokens at each step while
retaining only a small fraction. We propose Diffusion Scratchpad (DPad), a
training-free method that restricts attention to a small set of nearby suffix
tokens, preserving fidelity while eliminating redundancy. DPad integrates two
strategies: (i) a sliding window, which maintains a fixed-length suffix window,
and (ii) distance-decay dropout, which deterministically removes distant suffix
tokens before attention computation. This simple design is compatible with
existing optimizations such as prefix caching and can be implemented with only
a few lines of code. Comprehensive evaluations across multiple benchmarks on
LLaDA-1.5 and Dream models demonstrate that DPad delivers up to
$\mathbf{61.4\times}$ speedup over vanilla dLLMs while maintaining comparable
accuracy, highlighting its potential for efficient and scalable long-sequence
inference. Our code is available at https://github.com/Crys-Chen/DPad.

链接: http://arxiv.org/pdf/2508.14148v1
