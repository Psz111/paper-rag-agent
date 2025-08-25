# Unintended Misalignment from Agentic Fine-Tuning: Risks and Mitigation

Beyond simple text generation, Large Language Models (LLMs) have evolved into
agentic systems capable of planning and interacting with external tools to
solve complex tasks. This evolution involves fine-tuning LLMs on agent-specific
tasks to enhance their proficiency. However, safety concerns are frequently
overlooked during this fine-tuning process. In this work, we show that aligned
LLMs can become unintentionally misaligned, leading to a higher likelihood of
executing harmful tasks and a reduced tendency to refuse them when fine-tuned
to execute agentic tasks. To address these safety challenges, we propose Prefix
INjection Guard (PING), a simple yet effective method that prepends
automatically generated natural language prefixes to agent responses, guiding
them to refuse harmful requests while preserving performance on benign tasks.
Specifically, we introduce an iterative approach that alternates between (1)
generating candidate prefixes and (2) selecting those that optimize both task
performance and refusal behavior. Experimental results demonstrate that PING
significantly enhances the safety of fine-tuned LLM agents without sacrificing
their effectiveness. PING consistently outperforms existing prompting
approaches across diverse benchmarks in both web navigation and code generation
tasks. Our analysis of internal hidden states via linear probes reveals that
prefix tokens are crucial for behavior modification, explaining the performance
gains. WARNING: This paper contains contents that are unethical or offensive in
nature.

链接: http://arxiv.org/pdf/2508.14031v1
