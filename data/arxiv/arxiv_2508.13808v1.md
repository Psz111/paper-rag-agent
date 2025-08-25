# Is-NeRF: In-scattering Neural Radiance Field for Blurred Images

Neural Radiance Fields (NeRF) has gained significant attention for its
prominent implicit 3D representation and realistic novel view synthesis
capabilities. Available works unexceptionally employ straight-line volume
rendering, which struggles to handle sophisticated lightpath scenarios and
introduces geometric ambiguities during training, particularly evident when
processing motion-blurred images. To address these challenges, this work
proposes a novel deblur neural radiance field, Is-NeRF, featuring explicit
lightpath modeling in real-world environments. By unifying six common light
propagation phenomena through an in-scattering representation, we establish a
new scattering-aware volume rendering pipeline adaptable to complex lightpaths.
Additionally, we introduce an adaptive learning strategy that enables
autonomous determining of scattering directions and sampling intervals to
capture finer object details. The proposed network jointly optimizes NeRF
parameters, scattering parameters, and camera motions to recover fine-grained
scene representations from blurry images. Comprehensive evaluations demonstrate
that it effectively handles complex real-world scenarios, outperforming
state-of-the-art approaches in generating high-fidelity images with accurate
geometric details.

链接: http://arxiv.org/pdf/2508.13808v1
