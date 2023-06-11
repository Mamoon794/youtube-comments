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
    part="snippet",
    videoId=video_id,
    maxResults = 10,
    order="time"

)
response = request.execute()
nextOne = "12"

#Keeps track of comments
new = set()
comment_Num = 0

# While loop which keeps running until all the comments have been surfed through
while nextOne:
    #Gets the next 10 comments
    nextOne = response.get("nextPageToken")
    items = response["items"]  # Gets All the comments
    for item in items:
        info = item['snippet']['topLevelComment']['snippet']         #Gets the top comment
        comment = info["textOriginal"]                               #Gets the text of that comment
        author = info['authorDisplayName']                           #Gets the user that wrote the comment

        # The if satement that will need to be changed according to what the user wants to search for
        if "bot" in comment:
            print(f"{author}: {comment}")                            #Prints out the author and the comment
            print(comment_Num)                                       #Prints the comment number
        comment_Num += 1

    #Gets the next 100 comments in order of time it was commented
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        pageToken=nextOne,
        order="time"

    )
    response = request.execute()
