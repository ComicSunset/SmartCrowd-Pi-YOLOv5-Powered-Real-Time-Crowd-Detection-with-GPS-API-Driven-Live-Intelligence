#!/bin/bash

# Define paths and variables
YOLO_MODEL_PATH="D:/YOLO-CROWD/YOLO V5/weights/YOLO-CROWD.pt"
INPUT_FOLDER="D:/YOLO-CROWD/YOLO V5/images1"
OUTPUT_FOLDER="D:/YOLO-CROWD/YOLO V5/outputs"
SERVICE_ACCOUNT_FILE="D:/YOLO-CROWD/YOLO V5/vocal-cyclist-447515-k3-655b08d31c5b.json"
SPREADSHEET_ID="1jhxYxTmwm5mYbmG-BZiPhQOd5dKMczPznj-_yF7nTgc"
GEMINI_API_KEY="your_gemini_api_key_here"

# Function to process images with YOLOv5
process_image() {
    local file=$1
    python3 detect.py --weights $YOLO_MODEL_PATH --img-size 640 --source $file --save-txt --save-img --project $OUTPUT_FOLDER
}

# Function to log the crowd count to Google Sheets
log_to_sheets() {
    local timestamp=$1
    local count=$2
    curl -X POST \
        -H "Content-Type: application/json" \
        -d '{
              "values": [["'"$timestamp"'", "'"$count"'"]]
            }' \
        "https://sheets.googleapis.com/v4/spreadsheets/$SPREADSHEET_ID/values/Sheet1!A2:append?valueInputOption=RAW" \
        -H "Authorization: Bearer $(gcloud auth application-default print-access-token)"
}

# Function to get insight from Gemini API
get_gemini_insight() {
    local prompt=$1
    curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
              "contents": [{
                "parts":[{"text": "'"$prompt"'"}]
              }]
            }'
}

# Main execution loop
for file in $(ls $INPUT_FOLDER/*.jpg); do
    echo "Processing $file"
    
    # Process the image with YOLOv5
    process_image $file
    
    # Assuming your script generates a count.txt or you get the count from another source
    count=$(cat "$OUTPUT_FOLDER/$(basename $file .jpg)/count.txt")
    
    # Get the current timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Log count to Google Sheets
    log_to_sheets "$timestamp" "$count"
    
    # Get insight from Gemini API
    prompt="Give a safety insight for the crowd count of $count at location XYZ."
    insight=$(get_gemini_insight "$prompt")
    
    # Output the insight
    echo "Insight for $file: $insight"
    
    # Optional: Save the insight to a file (if needed)
    echo "$insight" > "$OUTPUT_FOLDER/$(basename $file .jpg)_insight.txt"
done

echo "Finished processing all images."
