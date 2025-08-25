# A Real-world Display Inverse Rendering Dataset

Inverse rendering aims to reconstruct geometry and reflectance from captured
images. Display-camera imaging systems offer unique advantages for this task:
each pixel can easily function as a programmable point light source, and the
polarized light emitted by LCD displays facilitates diffuse-specular
separation. Despite these benefits, there is currently no public real-world
dataset captured using display-camera systems, unlike other setups such as
light stages. This absence hinders the development and evaluation of
display-based inverse rendering methods. In this paper, we introduce the first
real-world dataset for display-based inverse rendering. To achieve this, we
construct and calibrate an imaging system comprising an LCD display and stereo
polarization cameras. We then capture a diverse set of objects with diverse
geometry and reflectance under one-light-at-a-time (OLAT) display patterns. We
also provide high-quality ground-truth geometry. Our dataset enables the
synthesis of captured images under arbitrary display patterns and different
noise levels. Using this dataset, we evaluate the performance of existing
photometric stereo and inverse rendering methods, and provide a simple, yet
effective baseline for display inverse rendering, outperforming
state-of-the-art inverse rendering methods. Code and dataset are available on
our project page at https://michaelcsj.github.io/DIR/

链接: http://arxiv.org/pdf/2508.14411v1
