# NeuralQA Demo: Question Answering with BERT Models

> NeuralQA provides a visual interface for end-to-end question answering (passage retrieval, query expansion, document reading, model explanation), on large datasets.
> Learn more on [Github](https://github.com/victordibia/neuralqa).

This repository provides sample code on how to deploy NeuralQA on Cloudera Machine Learning (CML).

![Neural QA Screenshot](docs/images/manual.jpg)

# Launch the Application on CML

To begin, create a new project on CML (use the Git tab) and provide the link for this repository - https://github.com/fastforwardlabs/cml_neuralqa.
This will clone the repository to your CML workbench session.

> Note: NeuralQA depends on several libraries (Tensorflow, Pytorch, Transformers etc). A minimum of 4GB memory instance is recommended to run this template.

Run the `launch.py` script in the interactive CML python view or via the terminal.

```shell
python3 launch.py
```

Thats it! The script above will create a CML Application and provide a link to the NeuralQA user interface (using default configurations).
