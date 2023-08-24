import pandas as pd
from googleapiclient.discovery import  build
import json

#Google API key
api_key = 'AIzaSyCUx0HzmRODWfvrIUF1Q9LJTRG8DTfmzGs'

#cannel-id - unique identifier 
channel_id='UCXhbCCZAG4GlaBLm80ZL-iA'

#to initalize youtube_services
youtube=build('youtube','v3',developerKey=api_key)



def get_response(youtube, channel_id):
    # Use the 'search' API to retrieve comments
    request = youtube.commentThreads().list(
        part="snippet",
        allThreadsRelatedToChannelId=channel_id
    )
    response = request.execute()
    return response

g=get_response(youtube,channel_id)    
print('hello world')
print(g)