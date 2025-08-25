# A Non-Asymptotic Convergent Analysis for Scored-Based Graph Generative   Model via a System of Stochastic Differential Equations

Score-based graph generative models (SGGMs) have proven effective in critical
applications such as drug discovery and protein synthesis. However, their
theoretical behavior, particularly regarding convergence, remains
underexplored. Unlike common score-based generative models (SGMs), which are
governed by a single stochastic differential equation (SDE), SGGMs involve a
system of coupled SDEs. In SGGMs, the graph structure and node features are
governed by separate but interdependent SDEs. This distinction makes existing
convergence analyses from SGMs inapplicable for SGGMs. In this work, we present
the first non-asymptotic convergence analysis for SGGMs, focusing on the
convergence bound (the risk of generative error) across three key graph
generation paradigms: (1) feature generation with a fixed graph structure, (2)
graph structure generation with fixed node features, and (3) joint generation
of both graph structure and node features. Our analysis reveals several unique
factors specific to SGGMs (e.g., the topological properties of the graph
structure) which affect the convergence bound. Additionally, we offer
theoretical insights into the selection of hyperparameters (e.g., sampling
steps and diffusion length) and advocate for techniques like normalization to
improve convergence. To validate our theoretical findings, we conduct a
controlled empirical study using synthetic graph models, and the results align
with our theoretical predictions. This work deepens the theoretical
understanding of SGGMs, demonstrates their applicability in critical domains,
and provides practical guidance for designing effective models.

链接: http://arxiv.org/pdf/2508.14351v1
