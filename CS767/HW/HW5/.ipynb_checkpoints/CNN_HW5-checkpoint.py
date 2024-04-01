import tensorflow as tf
import numpy as np
from datasets import load_dataset
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG19, ResNet50V2, InceptionV3
from tensorflow.keras.preprocessing import image

dataset = load_dataset("zh-plus/tiny-imagenet")
data = dataset['valid']

# Adjust the image size and preprocessing function for each model
image_sizes = {
    'VGG19': (224, 224),
    'ResNet50V2': (224, 224),
    'InceptionV3': (299, 299) # Adjusting for InceptionV3 instead of V4
}

preprocessing_functions = {
    'VGG19': tf.keras.applications.vgg19.preprocess_input,
    'ResNet50V2': tf.keras.applications.resnet_v2.preprocess_input,
    'InceptionV3': tf.keras.applications.inception_v3.preprocess_input
}

# Load the pre-trained models
vgg19 = VGG19(weights='imagenet')
resnet50v2 = ResNet50V2(weights='imagenet')
inceptionv3 = InceptionV3(weights='imagenet')  # Proxy for InceptionV4

vgg19.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
resnet50v2.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
inceptionv3.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

def preprocess_dataset(dataset, model_name):
    """Preprocess images to the required size and format for a given model."""
    new_dataset = dataset
    for i in range(len(new_dataset['valid']['image'])):
        img = new_dataset['valid']['image'][i]
        img_array = image.img_to_array(img)
        img_array_expanded = np.expand_dims(img_array, axis=0)
        preprocess_function = preprocessing_functions[model_name]
        img_preprocessed = preprocess_function(img_array_expanded)
        new_dataset['valid']['image'][i] = img_preprocessed
    return new_dataset

# Example usage: Preprocess the dataset for VGG19


dataset_vgg19 = preprocess_dataset(dataset, 'VGG19')
loss, accuracy = vgg19.evaluate(dataset_vgg19)
print(f"Loss: {loss}, Accuracy: {accuracy}")