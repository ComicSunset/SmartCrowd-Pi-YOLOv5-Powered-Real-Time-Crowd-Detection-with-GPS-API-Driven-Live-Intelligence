import os
import cv2
import torch
import numpy as np
from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_coords

# === Configuration ===
weights_path = r'D:\YOLO-CROWD\weights\YOLO-CROWD.pt'
img_size = 640
enable_heatmap = True

# === Load YOLO Model ===
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = attempt_load(weights_path, map_location=device)
model.eval()

# === Video Capture from System Webcam ===
cap = cv2.VideoCapture(0)  # 0 = default camera

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Output video writer (optional)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
fps = int(cap.get(cv2.CAP_PROP_FPS)) or 15
output_video_path = r'D:\YOLO-CROWD\output_video_from_webcam.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame not received from webcam.")
        break

    img0 = frame.copy()
    img = cv2.resize(img0, (img_size, img_size))
    img_rgb = img[:, :, ::-1].transpose(2, 0, 1).copy()
    img_tensor = torch.from_numpy(img_rgb).to(device).float() / 255.0
    img_tensor = img_tensor.unsqueeze(0)

    with torch.no_grad():
        pred = model(img_tensor)[0]
        pred = non_max_suppression(pred, 0.25, 0.45)[0]

    count = 0
    points = []
    if pred is not None and len(pred):
        pred[:, :4] = scale_coords(img_tensor.shape[2:], pred[:, :4], img0.shape).round()
        for *xyxy, conf, cls in pred:
            cx = int((xyxy[0] + xyxy[2]) / 2)
            cy = int((xyxy[1] + xyxy[3]) / 2)
            cv2.circle(img0, (cx, cy), radius=4, color=(0, 0, 255), thickness=-1)
            points.append((cx, cy))
            count += 1

    # === Optional Heatmap ===
    if enable_heatmap and points:
        heatmap = np.zeros((img0.shape[0], img0.shape[1]), dtype=np.float32)
        for cx, cy in points:
            if 0 <= cy < heatmap.shape[0] and 0 <= cx < heatmap.shape[1]:
                heatmap[cy, cx] += 1
        heatmap = cv2.GaussianBlur(heatmap, (15, 15), 0)
        heatmap_color = cv2.applyColorMap(
            cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8),
            cv2.COLORMAP_JET
        )
        img0 = cv2.addWeighted(img0, 0.6, heatmap_color, 0.4, 0)

    # === Display Count ===
    cv2.putText(img0, f"Count: {count}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 2)

    # === Write and Show ===
    out.write(img0)
    cv2.imshow("Live Webcam Count", img0)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === Cleanup ===
cap.release()
out.release()
cv2.destroyAllWindows()
