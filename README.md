# NeuralQA Demo: Question Answering with BERT Models

> NeuralQA provides a visual interface for end-to-end question answering (passage retrieval, query expansion, document reading, model explanation), on large datasets.
> Learn more on [Github](https://github.com/victordibia/neuralqa) or from the blog series [FF14 Automated Question Answering](https://qa.fastforwardlabs.com/)

This repository provides sample code on how to deploy NeuralQA on Cloudera Machine Learning (CML).

![Neural QA Screenshot](docs/images/manual.jpg)

# Launch the Application on CML

There are two ways to launch the NeuralQA prototype on CML:

1. **From Prototype Catalog** - Navigate to the Prototype Catalog on a CML workspace, select the "Neural Question Answering" tile, click "Launch as Project", click "Configure Project"
2. **As ML Prototype** - In a CML workspace, click "New Project", add a Project Name, select "ML Prototype" as the Initial Setup option, copy in the [repo URL](https://github.com/cloudera/CML_AMP_NeuralQA), click "Create Project", click "Configure Project"

> Note: NeuralQA depends on several heavy libraries (Tensorflow, Pytorch, Transformers etc). A minimum of 6GB memory instance is recommended to run this template.
