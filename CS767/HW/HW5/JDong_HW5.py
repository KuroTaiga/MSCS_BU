import timm
import torch
import os
from datasets import load_dataset
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
from torchvision.models import resnet50, vgg19, inception_v3, ResNet50_Weights, VGG19_Weights, Inception_V3_Weights
import urllib
from PIL import Image
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform
# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Define preprocessing transformations
# transform = transforms.Compose([
#     transforms.Resize(256),
#     transforms.CenterCrop(224),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
# ])

# Load dataset
# first, download the dataset
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
tipath = os.path.join(__location__, 'tiny-imagenet-200/val')
# test_dataset = datasets.ImageFolder(root=tipath, transform=transform)
# test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64, shuffle=False)

# Load a pre-trained model, for example, VGG-19
VGG_19_model = vgg19(weights=VGG19_Weights.DEFAULT).to(device)
RESNET_50_model = resnet50(weights=ResNet50_Weights.DEFAULT).to(device)
inceptionV3_model = inception_v3(weights = Inception_V3_Weights.DEFAULT).to(device)
inceptionV4_model = timm.create_model('inception_v4', pretrained=True)
# Switch model to evaluation mode
VGG_19_model.eval()
RESNET_50_model.eval()
inceptionV4_model.eval()
model_dict = {'VGG_19':VGG_19_model,'Resnet_50':RESNET_50_model, 'Inception_V3':inception_v3}
model_weights = {'VGG_19':VGG19_Weights.DEFAULT,'Resnet_50':ResNet50_Weights.DEFAULT,'Inception_V3':Inception_V3_Weights.DEFAULT}
# Define loss function
criterion = torch.nn.CrossEntropyLoss()

# Evaluate the model for VGG_19 and resnet_50 and inception_v3

# with torch.no_grad():
#     for name in model_dict:
#         total = 0
#         correct = 0
#         print("For model ", name)
#         model = model_dict[name]
#         weights = model_weights[name]
#         preprocess = weights.transforms()
#         test_dataset =  datasets.ImageFolder(root=tipath, transform=preprocess)
#         test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64, shuffle=False)
#         for images, labels in test_loader:
#             images, labels = images.to(device), labels.to(device)
#             outputs = model(images)
#             _, predicted = torch.max(outputs.data, 1)
#             total += labels.size(0)
#             correct += (predicted == labels).sum().item()
#             print(correct)
#         print(f'Accuracy of the network on the test images: {100 * correct / total}%')

# for inception_V4: using timm 
model = timm.create_model('inception_v4', pretrained=True)
model.eval()
config = resolve_data_config({}, model=model)
transform = create_transform(**config)
test_dataset = datasets.ImageFolder(root=tipath, transform=transform)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64, shuffle=False)
total = 0
correct = 0
print("For model inception_V4: ")
for images, labels in test_loader:
    images, labels = images.to(device), labels.to(device)
    outputs = model(images)
    _, predicted = torch.max(outputs.data, 1)
    total += labels.size(0)
    correct += (predicted == labels).sum().item()
    print(predicted)
print(f'Accuracy of the network on the test images: {100 * correct / total}%')