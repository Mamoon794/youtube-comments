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

new = set()
comment_Num = 0

while nextOne:
    nextOne = response.get("nextPageToken")
    items = response["items"]  # Gets All the replies
    for item in items:
        info = item['snippet']['topLevelComment']['snippet']
        comment = info["textOriginal"]
        author = info['authorDisplayName']
        if "bot" in comment:
            print(f"{author}: {comment}")
            print(comment_Num)
        comment_Num += 1


    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        pageToken=nextOne,
        order="time"

    )
    response = request.execute()
