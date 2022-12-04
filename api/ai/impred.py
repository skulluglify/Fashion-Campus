#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import os
import torch
import numpy as np
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms
from PIL import Image

pwd = os.path.dirname(__file__)

class Net(nn.Module):

    def __init__(self, in_channels=1, *args, **kwargs):
    
        super(Net, self).__init__()

        self.model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        self.model.conv1 = nn.Conv2d(in_channels, 64, kernel_size=7, stride=2, padding=3, bias=False)
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, 10)

    def forward(self, x):

        return self.model(x)

class Impred:

    ResNetModelPath = os.path.join(pwd, "model.pt")
    classes = [
        "T-shirt", 
        "Trouser", 
        "Pullover", 
        "Dress", 
        "Coat", 
        "Sandal", 
        "Shirt", 
        "Sneaker", 
        "Bag", 
        "Ankle_Boot"
    ]

    model= Net()
    buffer = io.BytesIO(open(ResNetModelPath, "rb").read())
    
    # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    device = torch.device("cpu")
    state = torch.load(buffer, device, encoding="ascii")

    def __init__(self, *args, **kwargs):

        self.model.load_state_dict(self.state)
        self.model.eval()

    def classes_predict_by_image(self, buffer):

        image = Image.open(buffer, "r")

        tensor = torch.unsqueeze(transforms.Compose([
            transforms.Grayscale(),
            transforms.ToTensor()
        ])(image), 0)

        with torch.no_grad():

            tensor = tensor.to(self.device)

            output = self.model.forward(tensor)

            index = np.argmax(output)

            return self.classes[index]

        ##