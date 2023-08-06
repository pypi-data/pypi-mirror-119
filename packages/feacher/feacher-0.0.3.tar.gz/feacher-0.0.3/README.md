<p></p>
<p></p>

<p align="center">
    <img src="https://github.com/qpochlabs/feacher/blob/main/assets/logo.png" width="85" alt="feacher-logo"/>
</p>

<h1 align="center">Feacher</h1>
<p align="center">Feacher is a light-weight Image feature extraction library that can help in transfer learning applications.</p>
<p align="center">
    <img src="https://github.com/qpochlabs/feacher/workflows/Python%20package/badge.svg" alt="Python-Package"/>
    <img src="https://badge.fury.io/py/feacher.svg" alt="PyPi"/>
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT-Licence"/>
    <img src="https://pepy.tech/badge/feacher/month" alt="PePy-Downloads"/>
</p>

<p></p>
<p></p>

## Requirements
-   PyTorch
-   Torchvision
-   PIL

## Installation
```python
pip install feacher
```

## Usage
```python
import feacher

# Path/Directory containg images 
path_to_images = 'images/'

# Extract features using Feacher
image_features = feacher.extract(path_to_images)

print(image_features[0])
```

### ResNet18 with other parameters example
```python
import feacher

# Path/Directory containg images 
path_to_images = 'images/'

# Extract features using Feacher
# Default values -
#   pretrained_model = 'resnet18'
#   resize_dim       = 256
#   layer            = 'avgpool'
image_features = feacher.extract(path_to_images,
                                 pretrained_model='resnet18',
                                 resize_dim=256,
                                 layer=None)

print(image_features[0])
```

### VGG16 features from features layer 30
```python
import feacher

# Path/Directory containg images 
path_to_images = 'images/'

# Extract features using Feacher
image_features = feacher.extract(path_to_images,
                                 pretrained_model='vgg16',
                                 resize_dim=256,
                                 layer=features[30])

print(image_features[0])
```

### Alexnet features from features layer 24
```python
import feacher

# Path/Directory containg images 
path_to_images = 'images/'

# Extract features using Feacher
image_features = feacher.extract(path_to_images,
                                 pretrained_model='alexnet',
                                 resize_dim=256,
                                 layer=features[12])

print(image_features[0])
```