import os
import cv2
import datetime
from pytube import YouTube

# List of YouTube livestream URLs
streams = {
    "Mechelen1": "https://www.youtube.com/watch?v=xQKCnSsATK0",
    "Mechelen2": "https://www.youtube.com/watch?v=m5HWzP2wNGE",
    "Lokeren": "https://www.youtube.com/watch?v=HUeaYuBLNNQ",
    "Krakow": "https://www.youtube.com/watch?v=S2L-hzuRX0g"
}

# Create output directory
os.makedirs("snapshots", exist_ok=True)

def get_stream_url(yt_url):
    yt = YouTube(yt_url)
    return yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first().url

def capture_snapshot(name, url):
    try:
        stream_url = get_stream_url(url)
        cap = cv2.VideoCapture(stream_url)
        ret, frame = cap.read()
        if ret:
            timestamp = datetime.datetime.utcnow().strftime("%m-%d-%H%M")
            filename = f"snapshots/{name}_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Saved: {filename}")
        cap.release()
    except Exception as e:
        print(f"Failed to capture {name}: {e}")

for name, url in streams.items():
    capture_snapshot(name, url)
