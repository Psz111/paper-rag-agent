# Improved Generalized Planning with LLMs through Strategy Refinement and   Reflection

LLMs have recently been used to generate Python programs representing
generalized plans in PDDL planning, i.e., plans that generalize across the
tasks of a given PDDL domain. Previous work proposed a framework consisting of
three steps: the LLM first generates a summary and then a strategy for the
domain, both in natural language, and then implements that strategy as a Python
program, that gets debugged on example planning tasks. In that work, only one
strategy is generated and passed directly to the program generation. If the
strategy is incorrect, its implementation will therefore result in an incorrect
generalized plan. Here, we introduce an approach that generates the strategy in
the form of pseudocode and enables automatic debugging of the pseudocode, hence
allowing us to identify and fix errors prior to the generation of the
generalized plan itself. Additionally, we extend the Python debugging phase
with a reflection step prompting the LLM to pinpoint the reason for the
observed plan failure. Finally, we take inspiration from LLM code generation to
produce several program variants and pick the best one. Running experiments on
17 benchmark domains, we show that these extensions substantially improve (and
never deteriorate) the quality of the generalized plans. In 12 of the domains,
our best Python programs solve all tasks that can be generated with the
respective instance generator.

链接: http://arxiv.org/pdf/2508.13876v1
