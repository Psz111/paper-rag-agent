# TransLLM: A Unified Multi-Task Foundation Framework for Urban   Transportation via Learnable Prompting

Urban transportation systems encounter diverse challenges across multiple
tasks, such as traffic forecasting, electric vehicle (EV) charging demand
prediction, and taxi dispatch. Existing approaches suffer from two key
limitations: small-scale deep learning models are task-specific and
data-hungry, limiting their generalizability across diverse scenarios, while
large language models (LLMs), despite offering flexibility through natural
language interfaces, struggle with structured spatiotemporal data and numerical
reasoning in transportation domains. To address these limitations, we propose
TransLLM, a unified foundation framework that integrates spatiotemporal
modeling with large language models through learnable prompt composition. Our
approach features a lightweight spatiotemporal encoder that captures complex
dependencies via dilated temporal convolutions and dual-adjacency graph
attention networks, seamlessly interfacing with LLMs through structured
embeddings. A novel instance-level prompt routing mechanism, trained via
reinforcement learning, dynamically personalizes prompts based on input
characteristics, moving beyond fixed task-specific templates. The framework
operates by encoding spatiotemporal patterns into contextual representations,
dynamically composing personalized prompts to guide LLM reasoning, and
projecting the resulting representations through specialized output layers to
generate task-specific predictions. Experiments across seven datasets and three
tasks demonstrate the exceptional effectiveness of TransLLM in both supervised
and zero-shot settings. Compared to ten baseline models, it delivers
competitive performance on both regression and planning problems, showing
strong generalization and cross-task adaptability. Our code is available at
https://github.com/BiYunying/TransLLM.

链接: http://arxiv.org/pdf/2508.14782v1
