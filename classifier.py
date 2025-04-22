import os
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image


# Define the ResNet50-based model architecture
class FacialParalysisDetector(nn.Module):
    def __init__(self, num_classes=2):
        super(FacialParalysisDetector, self).__init__()
        self.model = models.resnet50(pretrained=True)  # Load ResNet-50
        for param in self.model.parameters():
            param.requires_grad = False  # Freeze lower layers
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)
        for param in self.model.fc.parameters():
            param.requires_grad = True  # Unfreeze final layer

    def forward(self, x):
        return self.model(x)


# Set up device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Create model instance
model = FacialParalysisDetector(num_classes=2).to(device)

# Load the trained model
model_path = "model/model_final.pth"
if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()  # Set model to evaluation mode
    print(f"Model loaded from {model_path}")
else:
    print(f"Warning: Model file not found at {model_path}. Using untrained model.")

# Define preprocessing transformation
preprocess = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


# Function to load and preprocess image
def load_and_preprocess_image(image_path):
    image = Image.open(image_path).convert("RGB")  # Open image and convert to RGB
    image = preprocess(image).unsqueeze(0)  # Add batch dimension
    return image.to(device)


# Function to predict from an image file
def predict_image_file(image_path):
    image = Image.open(image_path).convert("RGB")
    image = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)

    class_labels = ["No Paralysis", "Paralysis"]
    return class_labels[predicted.item()]


# Example usage
if __name__ == "__main__":
    test_image = "input/12_happiness9.jpg"
    if os.path.exists(test_image):
        result = predict_image_file(test_image)
        print(f"Classification result: {result}")
