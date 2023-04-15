import cv2
import torch
import torchvision.transforms as transforms

class_labels = ['Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema',
                'Effusion', 'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration',
                'Mass', 'Nodule', 'Pleural_Thickening', 'Pneumonia',
                'Pneumothorax']

def inference(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    test_transforms = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((256, 256)),
        transforms.ToTensor()
    ])
    img = torch.unsqueeze(test_transforms(img), dim=0 )
    
    # Load the saved model
    model = torch.jit.load('model/nih.ts')

    # Set the model to evaluation mode
    model.eval()

    # Make a prediction
    with torch.no_grad():
        output = model(img)[0]
    
    # Get the top-5 predicted classes
    topk = torch.topk(output, k=3)

    topk_values = topk.values.squeeze(0)
    topk_indices = topk.indices.squeeze(0)

    # Filter out values less than 0.01
    mask = topk_values >= 0.01
    topk_values = topk_values[mask]
    topk_indices = topk_indices[mask]

    # Get the corresponding class labels
    topk_labels = [class_labels[i] for i in topk_indices.tolist()]
    
    return topk_labels