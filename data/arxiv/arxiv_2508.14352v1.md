# SBGD: Improving Graph Diffusion Generative Model via Stochastic Block   Diffusion

Graph diffusion generative models (GDGMs) have emerged as powerful tools for
generating high-quality graphs. However, their broader adoption faces
challenges in \emph{scalability and size generalization}. GDGMs struggle to
scale to large graphs due to their high memory requirements, as they typically
operate in the full graph space, requiring the entire graph to be stored in
memory during training and inference. This constraint limits their feasibility
for large-scale real-world graphs. GDGMs also exhibit poor size generalization,
with limited ability to generate graphs of sizes different from those in the
training data, restricting their adaptability across diverse applications. To
address these challenges, we propose the stochastic block graph diffusion
(SBGD) model, which refines graph representations into a block graph space.
This space incorporates structural priors based on real-world graph patterns,
significantly reducing memory complexity and enabling scalability to large
graphs. The block representation also improves size generalization by capturing
fundamental graph structures. Empirical results show that SBGD achieves
significant memory improvements (up to 6$\times$) while maintaining comparable
or even superior graph generation performance relative to state-of-the-art
methods. Furthermore, experiments demonstrate that SBGD better generalizes to
unseen graph sizes. The significance of SBGD extends beyond being a scalable
and effective GDGM; it also exemplifies the principle of modularization in
generative modeling, offering a new avenue for exploring generative models by
decomposing complex tasks into more manageable components.

链接: http://arxiv.org/pdf/2508.14352v1
