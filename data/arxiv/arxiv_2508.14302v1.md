# GLASS: Test-Time Acceleration for LLMs via Global-Local Neural   Importance Aggregation

Deploying Large Language Models (LLMs) on edge hardware demands aggressive,
prompt-aware dynamic pruning to reduce computation without degrading quality.
Static or predictor-based schemes either lock in a single sparsity pattern or
incur extra runtime overhead, and recent zero-shot methods that rely on
statistics from a single prompt fail on short prompt and/or long generation
scenarios. We introduce A/I-GLASS: Activation- and Impact-based Global-Local
neural importance Aggregation for feed-forward network SparSification, two
training-free methods that dynamically select FFN units using a
rank-aggregation of prompt local and model-intrinsic global neuron statistics.
Empirical results across multiple LLMs and benchmarks demonstrate that GLASS
significantly outperforms prior training-free methods, particularly in
challenging long-form generation scenarios, without relying on auxiliary
predictors or adding any inference overhead.

链接: http://arxiv.org/pdf/2508.14302v1
