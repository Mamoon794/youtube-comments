from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
load_dotenv()


api = os.getenv("API_KEY")
video_id = os.getenv("VIDEO_ID")


youtube = build("youtube", "v3", developerKey=api)


request = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    maxResults = 10,
    order="time"

)
response = request.execute()
nextOne = "12"
