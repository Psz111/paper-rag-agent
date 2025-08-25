# The illusion of a perfect metric: Why evaluating AI's words is harder   than it looks

Evaluating Natural Language Generation (NLG) is crucial for the practical
adoption of AI, but has been a longstanding research challenge. While human
evaluation is considered the de-facto standard, it is expensive and lacks
scalability. Practical applications have driven the development of various
automatic evaluation metrics (AEM), designed to compare the model output with
human-written references, generating a score which approximates human judgment.
Over time, AEMs have evolved from simple lexical comparisons, to semantic
similarity models and, more recently, to LLM-based evaluators. However, it
seems that no single metric has emerged as a definitive solution, resulting in
studies using different ones without fully considering the implications. This
paper aims to show this by conducting a thorough examination of the
methodologies of existing metrics, their documented strengths and limitations,
validation methods, and correlations with human judgment. We identify several
key challenges: metrics often capture only specific aspects of text quality,
their effectiveness varies by task and dataset, validation practices remain
unstructured, and correlations with human judgment are inconsistent.
Importantly, we find that these challenges persist in the most recent type of
metric, LLM-as-a-Judge, as well as in the evaluation of Retrieval Augmented
Generation (RAG), an increasingly relevant task in academia and industry. Our
findings challenge the quest for the 'perfect metric'. We propose selecting
metrics based on task-specific needs and leveraging complementary evaluations
and advocate that new metrics should focus on enhanced validation
methodologies.

链接: http://arxiv.org/pdf/2508.13816v1
