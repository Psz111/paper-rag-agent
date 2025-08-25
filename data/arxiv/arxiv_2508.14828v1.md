# Long Chain-of-Thought Reasoning Across Languages

Scaling inference through long chains-of-thought (CoTs) has unlocked
impressive reasoning capabilities in large language models (LLMs), yet the
reasoning process remains almost exclusively English-centric. We construct
translated versions of two popular English reasoning datasets, fine-tune Qwen
2.5 (7B) and Qwen 3 (8B) models, and present a systematic study of long CoT
generation across French, Japanese, Latvian, and Swahili. Our experiments
reveal three key findings. First, the efficacy of using English as a pivot
language varies by language: it provides no benefit for French, improves
performance when used as the reasoning language for Japanese and Latvian, and
proves insufficient for Swahili where both task comprehension and reasoning
remain poor. Second, extensive multilingual pretraining in Qwen 3 narrows but
does not eliminate the cross-lingual performance gap. A lightweight fine-tune
using only 1k traces still improves performance by over 30\% in Swahili. Third,
data quality versus scale trade-offs are language dependent: small, carefully
curated datasets suffice for English and French, whereas larger but noisier
corpora prove more effective for Swahili and Latvian. Together, these results
clarify when and why long CoTs transfer across languages and provide translated
datasets to foster equitable multilingual reasoning research.

链接: http://arxiv.org/pdf/2508.14828v1
