# Towards LLM-generated explanations for Component-based Knowledge Graph   Question Answering Systems

Over time, software systems have reached a level of complexity that makes it
difficult for their developers and users to explain particular decisions made
by them. In this paper, we focus on the explainability of component-based
systems for Question Answering (QA). These components often conduct processes
driven by AI methods, in which behavior and decisions cannot be clearly
explained or justified, s.t., even for QA experts interpreting the executed
process and its results is hard. To address this challenge, we present an
approach that considers the components' input and output data flows as a source
for representing the behavior and provide explanations for the components,
enabling users to comprehend what happened. In the QA framework used here, the
data flows of the components are represented as SPARQL queries (inputs) and RDF
triples (outputs). Hence, we are also providing valuable insights on
verbalization regarding these data types. In our experiments, the approach
generates explanations while following template-based settings (baseline) or
via the use of Large Language Models (LLMs) with different configurations
(automatic generation). Our evaluation shows that the explanations generated
via LLMs achieve high quality and mostly outperform template-based approaches
according to the users' ratings. Therefore, it enables us to automatically
explain the behavior and decisions of QA components to humans while using RDF
and SPARQL as a context for explanations.

链接: http://arxiv.org/pdf/2508.14553v1
