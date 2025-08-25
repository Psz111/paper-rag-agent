# Two Birds with One Stone: Multi-Task Detection and Attribution of   LLM-Generated Text

Large Language Models (LLMs), such as GPT-4 and Llama, have demonstrated
remarkable abilities in generating natural language. However, they also pose
security and integrity challenges. Existing countermeasures primarily focus on
distinguishing AI-generated content from human-written text, with most
solutions tailored for English. Meanwhile, authorship attribution--determining
which specific LLM produced a given text--has received comparatively little
attention despite its importance in forensic analysis. In this paper, we
present DA-MTL, a multi-task learning framework that simultaneously addresses
both text detection and authorship attribution. We evaluate DA-MTL on nine
datasets and four backbone models, demonstrating its strong performance across
multiple languages and LLM sources. Our framework captures each task's unique
characteristics and shares insights between them, which boosts performance in
both tasks. Additionally, we conduct a thorough analysis of cross-modal and
cross-lingual patterns and assess the framework's robustness against
adversarial obfuscation techniques. Our findings offer valuable insights into
LLM behavior and the generalization of both detection and authorship
attribution.

链接: http://arxiv.org/pdf/2508.14190v1
