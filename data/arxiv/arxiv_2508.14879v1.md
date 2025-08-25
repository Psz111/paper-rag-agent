# MeshCoder: LLM-Powered Structured Mesh Code Generation from Point Clouds

Reconstructing 3D objects into editable programs is pivotal for applications
like reverse engineering and shape editing. However, existing methods often
rely on limited domain-specific languages (DSLs) and small-scale datasets,
restricting their ability to model complex geometries and structures. To
address these challenges, we introduce MeshCoder, a novel framework that
reconstructs complex 3D objects from point clouds into editable Blender Python
scripts. We develop a comprehensive set of expressive Blender Python APIs
capable of synthesizing intricate geometries. Leveraging these APIs, we
construct a large-scale paired object-code dataset, where the code for each
object is decomposed into distinct semantic parts. Subsequently, we train a
multimodal large language model (LLM) that translates 3D point cloud into
executable Blender Python scripts. Our approach not only achieves superior
performance in shape-to-code reconstruction tasks but also facilitates
intuitive geometric and topological editing through convenient code
modifications. Furthermore, our code-based representation enhances the
reasoning capabilities of LLMs in 3D shape understanding tasks. Together, these
contributions establish MeshCoder as a powerful and flexible solution for
programmatic 3D shape reconstruction and understanding.

链接: http://arxiv.org/pdf/2508.14879v1
