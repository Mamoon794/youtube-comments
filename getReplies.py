from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

#The id's for the google api and the youtube id
api = os.getenv("API_KEY")
video_id = os.getenv("VIDEO_ID")

#Builds the youtube video and gets it ready for extraction
youtube = build("youtube", "v3", developerKey=api)

# requesting the comments 10 at a time in order of when they were commented
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