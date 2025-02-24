import torch.nn as nn
import torch.nn.functional as F
import torch


class FNet(nn.Module):
    # Extra TODO: Comment the code with docstrings
    """Fruit Net
            
    """
    def __init__(self,num_classes=5):
        # make your convolutional neural network here
        # use regularization
        # batch normalization

        super(FNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.fc = nn.Linear(7*7*32, num_classes)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        return out
        

if __name__ == "__main__":
    net = FNet()
