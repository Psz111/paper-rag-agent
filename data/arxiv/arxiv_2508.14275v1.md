# Disentangling concept semantics via multilingual averaging in Sparse   Autoencoders

Connecting LLMs with formal knowledge representation and reasoning is a
promising approach to address their shortcomings. Embeddings and sparse
autoencoders are widely used to represent textual content, but the semantics
are entangled with syntactic and language-specific information. We propose a
method that isolates concept semantics in Large Langue Models by averaging
concept activations derived via Sparse Autoencoders. We create English text
representations from OWL ontology classes, translate the English into French
and Chinese and then pass these texts as prompts to the Gemma 2B LLM. Using the
open source Gemma Scope suite of Sparse Autoencoders, we obtain concept
activations for each class and language version. We average the different
language activations to derive a conceptual average. We then correlate the
conceptual averages with a ground truth mapping between ontology classes. Our
results give a strong indication that the conceptual average aligns to the true
relationship between classes when compared with a single language by itself.
The result hints at a new technique which enables mechanistic interpretation of
internal network states with higher accuracy.

链接: http://arxiv.org/pdf/2508.14275v1
