#!/usr/bin/env python3
r"""Meetup 182 - Beginners' Python and Machine Learning - 10 May 2023 - Using a pretrained model

Colab:   https://colab.research.google.com/drive/1bljw1KcD5bCgyCaMKitz-W6huTVjYMUu
Youtube: https://youtube.com/live/N2bPnxTyRxE
Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/293248323/
Github:  https://github.com/timcu/bpaml-sessions/tree/master/online

@author D Tim Cummings

This lesson can be run using Python on your own computer or in Google Colab using nothing but a web browser.

To use Python on your own computer you will need to install Python and some third party libraries. (described here)
Alternatively install Anaconda which will install both. (not described here)

# 1. Download and install Python 3.11 from https://python.org

# 2. Create a virtual environment
mkdir bpaml182
cd bpaml182

python3 -m venv venv182         # Mac or Linux
source venv182/bin/activate     # Mac or Linux

py -m venv venv182              # Windows
venv182\Scripts\Activate.bat    # Windows

# Create a file called requirements.txt
torch
torchvision
Pillow
beautifulsoup4

# Install third party libraries listed in requirements.txt
pip install -U pip
pip install -r requirements.txt

# Run this script
python3 meetup182_tim_using_a_pretrained_model.py  # Mac or Linux
py meetup182_tim_using_a_pretrained_model.py       # Windows


## Artificial Intelligence

*the science and engineering of making intelligent machines, especially intelligent computer programs*

## Machine Learning

*branch of Artificial Intelligence which focuses on the use of data and algorithms to imitate the way humans learn, gradually improving accuracy*

## Neural Networks

*artificial neural networks mimic the human brain through a set of algorithms*

Neurons are capable of quite simple formula (linear equation) 

$output = w_1 x_1 + w_2 x_2 + w_3 x_3 + bias$

These are the weights ($w_1,w_2,w_3)$ and $bias$ of a layer that change as the model learns. 

The features $(x_1,x_2,x_3)$ are the input data to the algorithm and the $output$ is the decision made by the algorithm

## Deep Learning

*Any neural network with more than 3 layers is considered a deep learning neural network*

Output from one layer is the input to another layer. Non-linear transformations occur between layers otherwise any mix of layers could be replaced with one linear equation (layer).

GPUs are very good at thousands of parallel simple calculations and so are used extensively in deep learning. Other forms of machine learning don't need so much computing power but the input data needs to be better structured.

### References
- https://course.fast.ai
- https://pytorch.org/
"""
# Import third party libraries
# We can use standard Python libraries or 3rd party libraries.
# torchvision is part of the PyTorch library provided by Facebook,
# tensorflow is provided by Google
import torch
from torchvision import models
from torchvision import transforms
import PIL
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Python gives us a powerful free language for running scripts
w1 = 7
bias = 3
x1 = 2
y = w1 * x1 + bias
print('Contents of y where y = w1 * x1 + bias:', y)


# Values are remembered from one line to the next
# We can even define functions which are remembered
def my_algorithm(x):
    return w1 * x + bias


# Display results using python f strings
print(f"Results from calling function: {my_algorithm(3)=}")
print(f"Results from calling function: {my_algorithm(4)=}")


# Training models can take a long time. Fortunately we can use pretrained models
# resnet50 is a 50 layer neural network trained on more than 1 million images
# we can use the model and its trained weights
# Remember that we have already imported the 'models' third party library above
my_resnet50 = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)

# Tell it we want to start evaluating images
my_resnet50.eval()

# Let us get an image and see how it goes.
# https://www.abc.net.au/news/2023-01-03/pomeranian-rescued-from-python-by-owner-on-sunshine-coast-beach/101823438

url_snake = "https://live-production.wcms.abc-cdn.net.au/551b5e3c441c18f273038e47032f336b"
urllib.request.urlretrieve(url_snake, "snake.jpg")
hires_snake = PIL.Image.open('snake.jpg')
hires_snake.show()

# This image is much higher resolution than the ResNet image set so let's
# transform the image to be similar to the ones the model was trained on. 

# https://learnopencv.com/pytorch-for-beginners-image-classification-using-pre-trained-models/
rn50_mean = [0.485, 0.456, 0.406]
rn50_std = [0.229, 0.224, 0.225]
transform = transforms.Compose([
  transforms.Resize(256),
  transforms.CenterCrop(224),
  transforms.ToTensor(),
  transforms.Normalize(mean=rn50_mean, std=rn50_std)])

# Get data in the right form for model

snake224 = transform(hires_snake)
batch_unknowns = torch.unsqueeze(snake224, 0) 
print(f"{snake224.shape=}", ' = lists of reds per pixel, greens per pixel, blues per pixel')
print(f"{batch_unknowns.shape=}", ' = 1 image, 3 colours, 224 pixels x 224 pixels')

# Calculate the score of each class
out = my_resnet50(batch_unknowns)
print(f"{out.shape=}", '1 image identified, 1000 classes with their probability')
score_for_first_10 = str(out[0, :10]).replace('\n', '')
print(f"{score_for_first_10=}")

# Numbers don't tell us much so let us grab the list of classes used in resnet
# Learn how to webscrape in meetup 133 
# https://github.com/timcu/bpaml-sessions/blob/master/online/meetup133_tim_xml_html_beautifulsoup.py
url_class_names = 'https://deeplearning.cms.waikato.ac.nz/user-guide/class-maps/IMAGENET/'
page = urlopen(url_class_names)
soup = BeautifulSoup(page, 'html.parser')
list_tr = soup.find('table').tbody.find_all('tr', recursive=False)
list_class_names = [tr.td.find_next_sibling('td').string for tr in list_tr]
print(f"{list_class_names[:10]=}")

# Find the index of the class with the maximum probability
_, index = torch.max(out, 1)
probability = torch.nn.functional.softmax(out, dim=1)[0]
index[0], probability[index[0]].item(), list_class_names[index[0]]

# How good were the other guesses
_, indices = torch.sort(out, descending=True)
best_guesses = [(idx, probability[idx].item(), list_class_names[idx]) for idx in indices[0][:10]]
print("Best guesses")
print(f" IDX   Prob Class")
for g in best_guesses:
    print(f"{g[0]:>4} {g[1]:>6.3f} {g[2]}")
