# HERAKLES: Hierarchical Skill Compilation for Open-ended LLM Agents

Open-ended AI agents need to be able to learn efficiently goals of increasing
complexity, abstraction and heterogeneity over their lifetime. Beyond sampling
efficiently their own goals, autotelic agents specifically need to be able to
keep the growing complexity of goals under control, limiting the associated
growth in sample and computational complexity. To adress this challenge, recent
approaches have leveraged hierarchical reinforcement learning (HRL) and
language, capitalizing on its compositional and combinatorial generalization
capabilities to acquire temporally extended reusable behaviours. Existing
approaches use expert defined spaces of subgoals over which they instantiate a
hierarchy, and often assume pre-trained associated low-level policies. Such
designs are inadequate in open-ended scenarios, where goal spaces naturally
diversify across a broad spectrum of difficulties. We introduce HERAKLES, a
framework that enables a two-level hierarchical autotelic agent to continuously
compile mastered goals into the low-level policy, executed by a small, fast
neural network, dynamically expanding the set of subgoals available to the
high-level policy. We train a Large Language Model (LLM) to serve as the
high-level controller, exploiting its strengths in goal decomposition and
generalization to operate effectively over this evolving subgoal space. We
evaluate HERAKLES in the open-ended Crafter environment and show that it scales
effectively with goal complexity, improves sample efficiency through skill
compilation, and enables the agent to adapt robustly to novel challenges over
time.

链接: http://arxiv.org/pdf/2508.14751v1
