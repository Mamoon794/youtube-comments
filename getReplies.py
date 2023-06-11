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

#Keeps track of comments
length = 0
new = set()

# While loop which keeps running until all the replies have been surfed through
while nextOne:
    nextOne = response.get("nextPageToken")
    items = response["items"]  # Gets All the comments
    index = 0
    for item in items:

        # Gets the information for the actual replies
        reple = item.get("replies")
        if reple:
            reple = reple.get("comments")  # Gets all the replies of that comment
            for comment in reple:

                info = comment.get("snippet")                # The main snippet that gives the information of that reply
                text = info.get("textDisplay")               #Gets the text of that comment
                name = info.get("authorDisplayName")         #Gets the user that wrote the comment

                # The if satement that will need to be changed according to what the user wants to search for
                if "bot" in text.lower:
                    new.add(name)

                    # Not sure what this is for, I'll change it later but feel free to change the next 3-4 lines of
                    # code if needed
                    if len(new) > length:
                        print(name + ": " + text)

                    length = len(new)

    # Gets the next 100 comments in order of time
    request = youtube.commentThreads().list(
        part="replies",
        videoId=video_id,
        maxResults=100,
        pageToken=nextOne,
        order="time"

    )
    response = request.execute()

print(new)