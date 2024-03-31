import timm
from datasets import load_dataset
#from torchvision.models import resnet50, vgg19, Inceptionv4, ResNet50_Weights, VGG16_Weights, Inception_v4


dataset = load_dataset("zh-plus/tiny-imagenet")

inceptionV4_model = timm.create_model('inception_v4', pretrained=True)
inceptionV4_model.eval()