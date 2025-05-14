import os
import cv2
import torch
import numpy as np
from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_coords
from utils.plots import plot_one_box

# Folder paths (use raw strings to avoid escape issues)
input_folder = r'D:\YOLO-CROWD\images'
output_folder = r'D:\YOLO-CROWD\outputs'
weights_path = r'D:\YOLO-CROWD\weights\YOLO-CROWD.pt'
img_size = 640

# Load model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = attempt_load(weights_path, map_location=device)  # If error occurs, set weights_only=False in torch.load
model.eval()

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process all images in the input folder
for file in os.listdir(input_folder):
    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
        path = os.path.join(input_folder, file)
        img0 = cv2.imread(path)

        # Resize image for model input
        img = cv2.resize(img0, (img_size, img_size))
        img_rgb = img[:, :, ::-1].transpose(2, 0, 1).copy()  # BGR to RGB with positive strides
        img_tensor = torch.from_numpy(img_rgb).to(device).float() / 255.0
        img_tensor = img_tensor.unsqueeze(0)

        # Inference
        with torch.no_grad():
            pred = model(img_tensor)[0]
            pred = non_max_suppression(pred, 0.25, 0.45)[0]

        count = 0
        if pred is not None and len(pred):
            pred[:, :4] = scale_coords(img_tensor.shape[2:], pred[:, :4], img0.shape).round()
            for *xyxy, conf, cls in pred:
                plot_one_box(xyxy, img0, label=f'{int(conf*100)}%', color=(255, 0, 0), line_thickness=2)
                count += 1

        # Add count label
        cv2.putText(img0, f"Count: {count}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 2)

        # Save output image
        out_path = os.path.join(output_folder, file)
        cv2.imwrite(out_path, img0)
        print(f"Processed: {file} | Count: {count}")
