import timm
from tensorflow.keras.applications import VGG19, ResNet50V
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from datasets import load_dataset
#from torchvision.models import resnet50, vgg19, Inceptionv4, ResNet50_Weights, VGG16_Weights, Inception_v4


dataset = load_dataset("zh-plus/tiny-imagenet")

inceptionV4_model = timm.create_model('inception_v4', pretrained=True)
inceptionV4_model.eval()



def adapt_model(model_base, input_shape=(64, 64, 3), num_classes=200):
    base_model = model_base(include_top=False, weights='imagenet', input_shape=input_shape)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model

# Adapting each model
vgg19_model = adapt_model(VGG19)
resnet50v2_model = adapt_model(ResNet50V2)
inceptionv3_model = adapt_model(InceptionV3)  # Using InceptionV3 as a stand-in for InceptionV4
