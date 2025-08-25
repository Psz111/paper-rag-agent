# Chunks as Arms: Multi-Armed Bandit-Guided Sampling for Long-Context LLM   Preference Optimization

Long-context modeling is critical for a wide range of real-world tasks,
including long-context question answering, summarization, and complex reasoning
tasks. Recent studies have explored fine-tuning Large Language Models (LLMs)
with synthetic data to enhance their long-context capabilities. However, the
effectiveness of such approaches is often limited by the low diversity and
factual inconsistencies in the generated data. To address these challenges, we
propose LongMab-PO, a novel framework that leverages a Multi-Armed Bandit (MAB)
rollout strategy to identify the most informative chunks from the given long
context for sampling high-quality and diverse responses and constructing
preference data pairs for Direct Preference Optimization (DPO) training.
Specifically, we treat context chunks as arms of MAB, select chunks based on
their expected reward scores to input into LLMs to generate responses, and
iteratively update these scores based on reward feedback. This exploration and
exploitation process enables the model to focus on the most relevant context
segments, thereby generating and collecting high-quality and diverse responses.
Finally, we collect these generated responses from the rollout process and
apply the DPO method to further optimize the LLM. Experimental results show
that LongMab-PO significantly improves the diversity and quality of preference
data pairs, achieving state-of-the-art performance on long-context reasoning
benchmarks. All code and data will be released on
https://github.com/NEUIR/LongMab-PO.

链接: http://arxiv.org/pdf/2508.13993v1
