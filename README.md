## 🚀 SmartCrowd Pi: YOLOv5-Powered 🔍 Real-Time Crowd Detection 👥 with GPS 📍 & API-Driven Live Intelligence 🤖📡

SmartCrowd Pi is an advanced, smart surveillance system that utilizes **YOLOv5**, **Stereo Vision**, and a **Raspberry Pi 4B** mounted on a drone for **real-time crowd detection** and **density estimation**. Integrated with **GPS** and **external APIs**, the system provides **live intelligence**, visual overlays, and automatic reporting to services like **Google Sheets** or cloud dashboards.

---

## 📌 Key Features

- 🎯 **Real-Time Crowd Detection** using YOLOv5 on Raspberry Pi 4B
- 📷 **Stereo Camera Input** for improved area-based density estimation
- 🌐 **GPS Integration** for location-aware data
- 📊 **API Logging** to Google Sheets or cloud dashboards
- 🛰️ **Drone-Mounted Setup** for aerial surveillance
- 🔥 **Heatmap Overlay** and live video stream with count display
- 🧠 **Gemini API Integration** for randomized location-based crowd intelligence

---

## 🛠️ Tech Stack

| Component        | Technology Used                    |
|------------------|-------------------------------------|
| Object Detection | YOLOv5 (Ultralytics)                |
| Device           | Raspberry Pi 4B + Stereo Camera     |
| Language         | Python 3.x                          |
| GPS              | NMEA Parser / GPS Module Integration|
| APIs             | Google Sheets API, Gemini API       |
| Visual Overlay   | OpenCV                              |
| Drone Mounting   | Compatible with Pi and Stereo Setup |
| Dashboard (optional) | Blynk / Firebase / Custom UI     |

---

## 🚀 How It Works

1. **Capture live video** using stereo cameras mounted on the drone.
2. **YOLOv5 detects people** in real-time from the camera feed.
3. **Count data and density** are estimated based on bounding boxes and area.
4. **GPS coordinates** are fetched in real-time using a connected GPS module.
5. **Crowd statistics** (count + location) are sent via:
   - Google Sheets API
   - Custom RESTful API
   - Gemini AI-based crowd estimation on random coordinates
6. **Display live feed** with count and heatmaps overlaid.


