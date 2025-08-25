# TransLight: Image-Guided Customized Lighting Control with Generative   Decoupling

Most existing illumination-editing approaches fail to simultaneously provide
customized control of light effects and preserve content integrity. This makes
them less effective for practical lighting stylization requirements, especially
in the challenging task of transferring complex light effects from a reference
image to a user-specified target image. To address this problem, we propose
TransLight, a novel framework that enables high-fidelity and high-freedom
transfer of light effects. Extracting the light effect from the reference image
is the most critical and challenging step in our method. The difficulty lies in
the complex geometric structure features embedded in light effects that are
highly coupled with content in real-world scenarios. To achieve this, we first
present Generative Decoupling, where two fine-tuned diffusion models are used
to accurately separate image content and light effects, generating a newly
curated, million-scale dataset of image-content-light triplets. Then, we employ
IC-Light as the generative model and train our model with our triplets,
injecting the reference lighting image as an additional conditioning signal.
The resulting TransLight model enables customized and natural transfer of
diverse light effects. Notably, by thoroughly disentangling light effects from
reference images, our generative decoupling strategy endows TransLight with
highly flexible illumination control. Experimental results establish TransLight
as the first method to successfully transfer light effects across disparate
images, delivering more customized illumination control than existing
techniques and charting new directions for research in illumination
harmonization and editing.

链接: http://arxiv.org/pdf/2508.14814v1
