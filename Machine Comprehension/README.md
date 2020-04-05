# Machine Comprehension

Also called Quetion Answering, Machine Comprehension is a model that takes the context and question as the inputs and outputs the answer. This repository supports the code for the app https://dkedar.com/apps/machinecomprehension
In the current implementation, I used a pretrained BiDAF, available for download on https://github.com/onnx/models. 
I utilized Google Build to containerize my application, Google Container Registry for storing and managing my container and Google Cloud Run to deploy it as a web endpoint.

### About BiDAF
Researchers from the University of Washington and Allen Institute of Artificial Intelligence published a neural network model called BiDAF, short for Bi-Directional Attention Flow in 2016. This model stood at the top of the Stanford Question and Answering Dataset (SQuAD) leaderboard for several weeks. Although many newer models beat it eventually, BiDAF was instrumental in laying down the work for some other pathbreaking models like BERT and ELMo.

This app uses the pretrained weights of the model as found here in the ONNX format. A simpler implementation can also be found in this notebook.


### Aboout the implementation
Python 3.7 code takes context and text inputs and returns answer using the pretrained ONNX model. I made a REST API and web app using Flask that listens for POST requests on the localhost:8080 port.

<img src="https://github.com/dkedar7/NaturalLanguageProcessing/blob/master/Machine%20Comprehension/architecture.png" alt="Cloud Run Architecture">
<a href="https://cloud.google.com/run/docs/" target="_blank">Source</a>

### Installing and running the app

```bash
git clone https://github.com/dkedar7/NaturalLanguageProcessing
cd Machine\ Comprehension/
python3 -m venv bidaf
source bidaf/bin/activate
pip3 install -r requirements.txt
python3 main.py
```