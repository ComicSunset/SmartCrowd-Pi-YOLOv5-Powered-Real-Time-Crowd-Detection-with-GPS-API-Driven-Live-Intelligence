import os
import cv2
import time
import torch
import numpy as np
from datetime import datetime
import pytz

from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_coords

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# ========== CONFIGURATIONS ==========

# Google Sheets API Setup
SERVICE_ACCOUNT_FILE = r'D:\YOLO-CROWD\YOLO V5\ee-jaikrishna2403-6c01ffb9b198.json'
SPREADSHEET_ID = '183-jkoXD4OUmMYTlfWVKkO2s3o0FDqbF-VOmrs0UQFk'
RANGE_NAME = 'Sheet1!A2'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Time zone setting
timezone = pytz.timezone('Asia/Kolkata')  # Adjust as needed

# YOLO Model Setup
weights_path = r'D:\YOLO-CROWD\YOLO V5\weights\YOLO-CROWD.pt'
img_size = 640
enable_heatmap = True

# Folder paths
input_folder = r'D:\YOLO-CROWD\YOLO V5\images1'
output_folder = r'D:\YOLO-CROWD\YOLO V5\outputs'
os.makedirs(output_folder, exist_ok=True)

# ========== GOOGLE SHEETS AUTHENTICATION ==========

try:
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    print(f"✔️ Connected to Google Sheet: {spreadsheet['properties']['title']}")
except Exception as e:
    print(f"❌ Google Sheets Error: {e}")
    exit()

# ========== YOLO MODEL LOAD ==========

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = attempt_load(weights_path, map_location=device)
model.eval()
print(f"✔️ YOLO Model loaded on {device}")

# ========== PROCESS IMAGES ==========

for file in sorted(os.listdir(input_folder)):
    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
        path = os.path.join(input_folder, file)
        img0 = cv2.imread(path)
        original_shape = img0.shape[:2]

        # Preprocess image
        img = cv2.resize(img0, (img_size, img_size))
        img_rgb = img[:, :, ::-1].transpose(2, 0, 1).copy()
        img_tensor = torch.from_numpy(img_rgb).to(device).float() / 255.0
        img_tensor = img_tensor.unsqueeze(0)

        # YOLO Inference
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

        # Heatmap overlay
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

        # Draw count
        cv2.putText(img0, f"Count: {count}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 2)

        # Save output image
        output_path = os.path.join(output_folder, file)
        cv2.imwrite(output_path, img0)
        print(f"🖼️ Processed: {file} | Count: {count}")

        # Log to Google Sheets
        timestamp = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
        values = [[timestamp, count]]
        body = {"values": values}

        try:
            service.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME,
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            print(f"📊 Logged to Google Sheets: {count} at {timestamp}")
        except Exception as e:
            print(f"❌ Failed to log to Google Sheets at {timestamp}: {e}")

        # Optional delay
        time.sleep(2)
