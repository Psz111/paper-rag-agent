# Your Reward Function for RL is Your Best PRM for Search: Unifying RL and   Search-Based TTS

Test-time scaling (TTS) for large language models (LLMs) has thus far fallen
into two largely separate paradigms: (1) reinforcement learning (RL) methods
that optimize sparse outcome-based rewards, yet suffer from instability and low
sample efficiency; and (2) search-based techniques guided by independently
trained, static process reward models (PRMs), which require expensive human- or
LLM-generated labels and often degrade under distribution shifts. In this
paper, we introduce AIRL-S, the first natural unification of RL-based and
search-based TTS. Central to AIRL-S is the insight that the reward function
learned during RL training inherently represents the ideal PRM for guiding
downstream search. Specifically, we leverage adversarial inverse reinforcement
learning (AIRL) combined with group relative policy optimization (GRPO) to
learn a dense, dynamic PRM directly from correct reasoning traces, entirely
eliminating the need for labeled intermediate process data. At inference, the
resulting PRM simultaneously serves as the critic for RL rollouts and as a
heuristic to effectively guide search procedures, facilitating robust reasoning
chain extension, mitigating reward hacking, and enhancing cross-task
generalization. Experimental results across eight benchmarks, including
mathematics, scientific reasoning, and code generation, demonstrate that our
unified approach improves performance by 9 % on average over the base model,
matching GPT-4o. Furthermore, when integrated into multiple search algorithms,
our PRM consistently outperforms all baseline PRMs trained with labeled data.
These results underscore that, indeed, your reward function for RL is your best
PRM for search, providing a robust and cost-effective solution to complex
reasoning tasks in LLMs.

链接: http://arxiv.org/pdf/2508.14313v1
