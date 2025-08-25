# Adaptively Robust LLM Inference Optimization under Prediction   Uncertainty

We study the problem of optimizing Large Language Model (LLM) inference
scheduling to minimize total latency. LLM inference is an online and multi-task
service process and also heavily energy consuming by which a pre-trained LLM
processes input requests and generates output tokens sequentially. Therefore,
it is vital to improve its scheduling efficiency and reduce the power
consumption while a great amount of prompt requests are arriving. A key
challenge in LLM inference scheduling is that while the prompt length is known
upon arrival, the output length, which critically impacts memory usage and
processing time, is unknown. To address this uncertainty, we propose algorithms
that leverage machine learning to predict output lengths, assuming the
prediction provides an interval classification (min-max range) for each
request.
  We first design a conservative algorithm, $\mathcal{A}_{\max}$, which
schedules requests based on the upper bound of predicted output lengths to
prevent memory overflow. However, this approach is overly conservative: as
prediction accuracy decreases, performance degrades significantly due to
potential overestimation. To overcome this limitation, we propose
$\mathcal{A}_{\min}$, an adaptive algorithm that initially treats the predicted
lower bound as the output length and dynamically refines this estimate during
inferencing. We prove that $\mathcal{A}_{\min}$ achieves a log-scale
competitive ratio. Through numerical simulations, we demonstrate that
$\mathcal{A}_{\min}$ often performs nearly as well as the hindsight scheduler,
highlighting both its efficiency and robustness in practical scenarios.
Moreover, $\mathcal{A}_{\min}$ relies solely on the lower bound of the
prediction interval--an advantageous design choice since upper bounds on output
length are typically more challenging to predict accurately.

链接: http://arxiv.org/pdf/2508.14544v1
