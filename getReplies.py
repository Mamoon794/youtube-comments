from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()
api = os.getenv("API_KEY")
video_id = os.getenv("VIDEO_ID")


youtube = build("youtube", "v3", developerKey=api)


request = youtube.commentThreads().list(
    part="replies",
    videoId=video_id,
    maxResults = 100,
    order="time"

)
response = request.execute()
nextOne = "12"

length = 0
new = set()


while nextOne:
    nextOne = response.get("nextPageToken")
    items = response["items"]  # Gets All the replies
    index = 0
    for item in items:

        # Gets the information for the actual replies
        reple = item.get("replies")
        if reple:
            reple = reple.get("comments")  # Gets the comments of that reply
            for comment in reple:

                info = comment.get("snippet")   # The main snippet that gives the information of that reply
                text = info.get("textDisplay")
                name = info.get("authorDisplayName")

                if ("winner" in text.lower() or "congrat" in text.lower()) \
                        and "telegram" not in name.lower() and "telegraph" not in name.lower():
                    new.add(name)
                    if len(new) > length:
                        print(name + ": " + text)

                    length = len(new)
                    # print("================================\n")

    request = youtube.commentThreads().list(
        part="replies",
        videoId=video_id,
        maxResults=100,
        pageToken=nextOne,
        order="time"

    )
    response = request.execute()

print(new)