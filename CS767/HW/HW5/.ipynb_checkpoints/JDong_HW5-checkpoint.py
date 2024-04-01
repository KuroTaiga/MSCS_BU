import timm
import torch
import os
from datasets import load_dataset
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
#from torchvision.models import resnet50, vgg19, Inceptionv4, ResNet50_Weights, VGG16_Weights, Inception_v4

# Set device
device = torch.device("cuda")

# Define preprocessing transformations
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Load dataset
# first, download the dataset
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
tipath = os.path.join(__location__, 'iny-imagenet-200/val')
test_dataset = datasets.ImageFolder(root=tipath, transform=transform)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64, shuffle=False)

# Load a pre-trained model, for example, VGG-19
VGG_19_model = models.vgg19(pretrained=True).to(device)
RESNET_50_model = models.resnet50(pretrained=True).to(device)
inceptionV4_model = timm.create_model('inception_v4', pretrained=True)
# Switch model to evaluation mode
VGG_19_model.eval()
RESNET_50_model.eval()
inceptionV4_model.eval()
model_dict = {'VGG_19':VGG_19_model,'Resnet_50':RESNET_50_model,'InceptionV4':inceptionV4_model}
# Define loss function
criterion = torch.nn.CrossEntropyLoss()

# Evaluate the model
total = 0
correct = 0
with torch.no_grad():
    for name,model in model_dict:
        print("For model ", name)
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        print(f'Accuracy of the network on the test images: {100 * correct / total}%')

