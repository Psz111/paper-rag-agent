# Prompt-Based One-Shot Exact Length-Controlled Generation with LLMs

Controlling the length of text produced by large language models (LLMs)
remains challenging: models frequently overshoot or undershoot explicit length
instructions because they cannot reliably keep an internal token count. We
present a prompt-based, one-shot strategy that compels an off-the-shelf LLM to
generate exactly a desired number of tokens - words (English) or characters
(Chinese) - without any fine-tuning or iterative sampling. The prompt appends
countdown markers and explicit counting rules so that the model "writes while
counting." We evaluate on four settings: open-ended generation (1-1000 tokens),
XSUM summarization, MT-Bench-LI instruction following, and the LIFEBENCH
equal-length track. On MT-Bench-LI, strict length compliance with GPT-4.1 leaps
from below 30% under naive prompts to above 95% with our countdown prompt,
surpassing the popular draft-then-revise baseline, while judged answer quality
is preserved. These results show that precise length control can be achieved
through prompt engineering alone, offering a lightweight alternative to
training- or decoding-based methods.

链接: http://arxiv.org/pdf/2508.13805v1
