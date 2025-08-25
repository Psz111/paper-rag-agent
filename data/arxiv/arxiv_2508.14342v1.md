# Generative AI Against Poaching: Latent Composite Flow Matching for   Wildlife Conservation

Poaching poses significant threats to wildlife and biodiversity. A valuable
step in reducing poaching is to forecast poacher behavior, which can inform
patrol planning and other conservation interventions. Existing poaching
prediction methods based on linear models or decision trees lack the
expressivity to capture complex, nonlinear spatiotemporal patterns. Recent
advances in generative modeling, particularly flow matching, offer a more
flexible alternative. However, training such models on real-world poaching data
faces two central obstacles: imperfect detection of poaching events and limited
data. To address imperfect detection, we integrate flow matching with an
occupancy-based detection model and train the flow in latent space to infer the
underlying occupancy state. To mitigate data scarcity, we adopt a composite
flow initialized from a linear-model prediction rather than random noise which
is the standard in diffusion models, injecting prior knowledge and improving
generalization. Evaluations on datasets from two national parks in Uganda show
consistent gains in predictive accuracy.

链接: http://arxiv.org/pdf/2508.14342v1
