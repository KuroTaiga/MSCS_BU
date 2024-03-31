import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import time

print("Part 1 dataloading")
# Data transformation and normalization
transform = transforms.Compose([transforms.ToTensor(),
                                transforms.Normalize((0.5,), (0.5,))])

# Loading MNIST dataset
train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)
print("Done with dataloading")
# Neural network architecture
class Net(nn.Module):
    def __init__(self, activation_func=nn.ReLU(),use_dropout=False, use_batchnorm=False):
        super(Net, self).__init__()
        self.flatten = nn.Flatten()
        self.layer1 = nn.Linear(28*28, 128)
        self.layer2 = nn.Linear(128, 64)
        self.output = nn.Linear(64, 10)
        self.activation = activation_func

        #Dropout
        self.use_dropout = use_dropout
        self.dropout = nn.Dropout(0.5)

        #Batchnorm
        self.use_batchnorm = use_batchnorm
        self.batchnorm1 = nn.BatchNorm1d(128)
        self.batchnorm2 = nn.BatchNorm1d(64)

    def forward(self, x):
        x = self.flatten(x)
        x = self.layer1(x)
        if self.use_batchnorm:
            x = self.batchnorm1(x)
        x = self.activation(x)
        if self.use_dropout:
            x = self.dropout(x)
        x = self.layer2(x)
        if self.use_batchnorm:
            x = self.batchnorm2(x)
        x = self.activation(x)
        if self.use_dropout:
            x = self.dropout(x)
        x = self.output(x)
        return x

def train_and_evaluate(model, optimizer, epochs=10):
    criterion = nn.CrossEntropyLoss()
    start_time = time.time()

    for epoch in range(epochs):
        model.train()
        for images, labels in train_loader:
            optimizer.zero_grad()
            output = model(images)
            loss = criterion(output, labels)
            loss.backward()
            optimizer.step()

    # Testing the model
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            output = model(images)
            _, predicted = torch.max(output.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    execution_time = time.time() - start_time
    accuracy = correct / total

    return accuracy, execution_time

# Activation functions to experiment with
activation_functions = {
    'Identity': nn.Identity(),
    'ReLU': nn.ReLU(),
    'Sigmoid': nn.Sigmoid()
}
def partTwo():
    print("Running part 2")
    results_activation = {}

    for name, activation in activation_functions.items():
        print("Using activation function, and same optimizer (Adam): ",name)
        model = Net(activation_func=activation)
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        accuracy, execution_time = train_and_evaluate(model, optimizer, epochs=10)
        results_activation[name] = (accuracy, execution_time)

    for name, (accuracy, execution_time) in results_activation.items():
        print(f"{name}: Accuracy = {accuracy:.4f}, Execution Time = {execution_time:.2f} seconds")

# Assuming the Net class and train_and_evaluate function are defined as before
def partThree():
    print("Running part 3")
    # Optimizers to experiment with
    optimizers = ['SGD','Adam','RMSprop','Adagrad']

    results_optimizers = {}

    # Repeating the experiment for each optimizer
    for name in optimizers:
        print("Using optimizer: ",name)
        model = Net(activation_func=nn.ReLU())  # Using ReLU for consistent comparison
        if name == 'SGD':
            optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
        elif name == 'Adgrad':
            optimizer = optim.Adagrad(model.parameters(), lr=0.01)
        elif name == 'RMSprop':
            optimizer = optim.RMSprop(model.parameters(), lr=0.001)
        else:
            #Baseline Adam
            optimizer = optim.Adam(model.parameters(), lr=0.001)

        accuracy, execution_time = train_and_evaluate(model, optimizer, epochs=10)
        results_optimizers[name] = (accuracy, execution_time)

    for name, (accuracy, execution_time) in results_optimizers.items():
        print(f"{name}: Accuracy = {accuracy:.4f}, Execution Time = {execution_time:.2f} seconds")

# part 4
def initialize_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')

def partFour():
    print("Part 4")
    print("Running Baseline")
    # Baseline, using ReLU activation function and Adam optimizer
    model = Net(use_dropout=False,use_batchnorm=False)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    accuracy, execution_time = train_and_evaluate(model, optimizer, epochs=10)
    print(f"Baseline: Accuracy = {accuracy:.4f}, Execution Time = {execution_time:.2f} seconds")

    # Batchnorm
    print("Running Batchnorm")
    model = Net(use_dropout=False,use_batchnorm=True)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    accuracy, execution_time = train_and_evaluate(model, optimizer, epochs=10)
    print(f"Batch Norm: Accuracy = {accuracy:.4f}, Execution Time = {execution_time:.2f} seconds")

    # Dropout
    print("Running Dropout")
    model = Net(use_dropout=True,use_batchnorm=False)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    accuracy, execution_time = train_and_evaluate(model, optimizer, epochs=10)
    print(f"Dropout: Accuracy = {accuracy:.4f}, Execution Time = {execution_time:.2f} seconds")

    # Weighted Init
    print("Running Weighted Init")
    model = Net(use_dropout=False, use_batchnorm=False)
    model.apply(initialize_weights)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    accuracy, execution_time = train_and_evaluate(model, optimizer, epochs=10)
    print(f"Weighted Init: Accuracy = {accuracy:.4f}, Execution Time = {execution_time:.2f} seconds")

partTwo()
partThree()
partFour()