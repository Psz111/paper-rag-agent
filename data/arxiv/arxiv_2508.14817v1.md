# Evaluating Retrieval-Augmented Generation vs. Long-Context Input for   Clinical Reasoning over EHRs

Electronic health records (EHRs) are long, noisy, and often redundant, posing
a major challenge for the clinicians who must navigate them. Large language
models (LLMs) offer a promising solution for extracting and reasoning over this
unstructured text, but the length of clinical notes often exceeds even
state-of-the-art models' extended context windows. Retrieval-augmented
generation (RAG) offers an alternative by retrieving task-relevant passages
from across the entire EHR, potentially reducing the amount of required input
tokens. In this work, we propose three clinical tasks designed to be replicable
across health systems with minimal effort: 1) extracting imaging procedures, 2)
generating timelines of antibiotic use, and 3) identifying key diagnoses. Using
EHRs from actual hospitalized patients, we test three state-of-the-art LLMs
with varying amounts of provided context, using either targeted text retrieval
or the most recent clinical notes. We find that RAG closely matches or exceeds
the performance of using recent notes, and approaches the performance of using
the models' full context while requiring drastically fewer input tokens. Our
results suggest that RAG remains a competitive and efficient approach even as
newer models become capable of handling increasingly longer amounts of text.

链接: http://arxiv.org/pdf/2508.14817v1
