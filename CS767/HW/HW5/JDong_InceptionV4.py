# # Import Python Standard Library dependencies
import inception_v4
#from keras import backend as K
#

model_v4 = inception_v4.create_model(weights='imagenet', include_top=True)












# from copy import copy
# import datetime
# from glob import glob
# import json
# import math
# import multiprocessing
# import os
# from pathlib import Path
# import random
# import urllib.request

# # Import utility functions
# from cjm_pandas_utils.core import markdown_to_pandas
# from cjm_pil_utils.core import resize_img, get_img_files
# from cjm_psl_utils.core import download_file, file_extract
# from cjm_pytorch_utils.core import set_seed, pil_to_tensor, tensor_to_pil, get_torch_device, denorm_img_tensor
# from cjm_torchvision_tfms.core import ResizeMax, PadSquare

# # Import matplotlib for creating plots
# import matplotlib.pyplot as plt

# # Import numpy 
# import numpy as np

# # Import pandas module for data manipulation
# import pandas as pd

# # Do not truncate the contents of cells and display all rows and columns
# pd.set_option('max_colwidth', None, 'display.max_rows', None, 'display.max_columns', None)

# # Import PIL for image manipulation
# from PIL import Image

# # Import timm library
# import timm

# # Import PyTorch dependencies
# import torch
# import torch.nn as nn
# from torch.amp import autocast
# from torch.cuda.amp import GradScaler
# from torch.utils.data import Dataset, DataLoader

# import torchvision
# torchvision.disable_beta_transforms_warning()
# import torchvision.transforms.v2  as transforms
# from torchvision.transforms.v2 import functional as TF

# from torchtnt.utils import get_module_summary
# from torcheval.metrics import MulticlassAccuracy

# # Import tqdm for progress bar
# from tqdm.auto import tqdm
# #from torchvision.models import resnet50, vgg19, Inceptionv4, ResNet50_Weights, VGG16_Weights, Inception_v4


# dataset = load_dataset("zh-plus/tiny-imagenet")

# inceptionV4_model = timm.create_model('inception_v4', pretrained=True, num_classes=200)
# inceptionV4_model.eval()



# # def adapt_model(model_base, input_shape=(64, 64, 3), num_classes=200):
# #     base_model = model_base(include_top=False, weights='imagenet', input_shape=input_shape)
# #     x = base_model.output
# #     x = GlobalAveragePooling2D()(x)
# #     x = Dense(1024, activation='relu')(x)
# #     predictions = Dense(num_classes, activation='softmax')(x)
    
# #     model = Model(inputs=base_model.input, outputs=predictions)
# #     model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
    
# #     return model

# # # Adapting each model
# # vgg19_model = adapt_model(VGG19)
# # resnet50v2_model = adapt_model(ResNet50V2)
# # inceptionv3_model = adapt_model(InceptionV3)  # Using InceptionV3 as a stand-in for InceptionV4
