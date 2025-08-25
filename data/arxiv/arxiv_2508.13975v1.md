# ChronoLLM: Customizing Language Models for Physics-Based Simulation Code   Generation

This contribution is concerned with the following issue: can pretrained large
language models (LLMs) be refined and customized to the point where they become
virtual assistants helping experts with the effective use of a simulation tool?
In this case study, the ``simulation tool'' considered is PyChrono, an open
source multi-physics dynamics engine for multibody systems. We present a
framework for refining and customizing both open- and closed-source LLMs to
harness the power of AI in generating scripts that perform PyChrono virtual
experiments. We refine and customize several classes of LLMs through a process
that leads to a quantifiable improvement in the quality of the generated
PyChrono simulation scripts. These scripts can range from simple
single-pendulum simulations to complex virtual experiments involving full
vehicles on deformable terrain. While the generated scripts are rarely perfect,
they often serve as strong starting points for the user to modify and improve
on. Additionally, the LLM can answer specific API questions about the
simulator, or recommend modeling approaches. The framework discussed is general
and can be applied to lower the entry barrier for simulation tools associated
with other application domains.

链接: http://arxiv.org/pdf/2508.13975v1
