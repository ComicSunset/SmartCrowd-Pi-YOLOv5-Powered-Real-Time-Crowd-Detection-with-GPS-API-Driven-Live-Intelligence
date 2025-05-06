## 🚀 SmartCrowd Pi: YOLOv5-Powered 🔍 Real-Time Crowd Detection 👥 with GPS 📍 & API-Driven Live Intelligence 🤖📡

SmartCrowd Pi is an advanced, smart surveillance system that utilizes **YOLOv5**, **Stereo Vision**, and a **Raspberry Pi 4B** mounted on a drone for **real-time crowd detection** and **density estimation**. Integrated with **GPS** and **external APIs**, the system provides **live intelligence**, visual overlays, and automatic reporting to services like **Google Sheets** or cloud dashboards.

---

## 🔑 Key Features

✅ Real-time person detection using YOLOv5  
📡 Live GPS-based crowd localization  
📊 Crowd count, density heatmaps, and timestamp logging  
🚁 Drone-compatible lightweight hardware  
📤 Logs sent to Google Sheets / Firebase / Gemini API  
🧠 Location-based AI queries with Gemini integration  
💻 Portable Python-based implementation  
🌐 Future-ready for dashboard/web integration  

---

## 🧠 Core Technologies Used

| Component           | Technology Stack & Explanation                                                                 |
|---------------------|------------------------------------------------------------------------------------------------|
| 🧠 Object Detection  | **YOLOv5 (You Only Look Once v5)** - Ultralight, real-time CNN-based detection model            |
| 🎛️ Edge Device       | **Raspberry Pi 4B** - Quad-core ARM Cortex-A72 SoC, runs Python scripts & inference on-device   |
| 👁️ Stereo Vision     | **Stereo Pi / Dual Camera Module** - Provides binocular vision for depth estimation & area calc |
| 🛰️ Positioning       | **GPS (NMEA Protocol / GY-NEO6MV2)** - Acquires real-time geo-coordinates for tagging locations |
| 🔌 API Integration   | **Google Sheets API, Firebase REST API, Gemini AI API** - For logging and querying smart data   |
| 🔁 Communication     | **HTTP Requests & JSON Payloads** - Data transmitted securely to cloud or analytics platforms    |
| 🚁 Aerial Platform   | **Quadcopter Drone Mount** - Mobile surveillance platform with wide area coverage               |
| 🧰 Programming       | **Python, OpenCV, NumPy, Requests, Torch** - Core software stack for deployment and visualization|

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
   
-----

## 🛸 Drone Deployment Instructions

1.Mount Raspberry Pi & camera module onto quadcopter

2.Power Pi via drone’s onboard battery or Li-Po pack

3.Establish remote SSH or telemetry connection

4.Use onboard Wi-Fi or 4G dongle for API logging (optional)

5.Run yolo_detect.py remotely via SSH or cronjob

----

## 📍 Use Cases
📦 Smart City Surveillance

🧑‍🤝‍🧑 Crowd Flow Monitoring

🧯 Disaster Management & Rescue

🎉 Event Safety

🛰️ Aerial Mapping of Congested Zones

## 🛠️ System Architecture

```mermaid
graph TD;
    Camera[Stereo Camera 📷]
    Pi[Raspberry Pi 4B 💻]
    YOLO[YOLOv5 Inference Engine 🧠]
    GPS[GPS Module 📡]
    Heatmap[Heatmap Generator 🌡️]
    API[API Integration 🔗]
    Drone[Quadcopter Frame 🚁]

    Camera --> Pi
    Pi --> YOLO
    Pi --> GPS
    YOLO --> Heatmap
    YOLO --> API
    GPS --> API
    Heatmap --> API
    Pi --> Drone


