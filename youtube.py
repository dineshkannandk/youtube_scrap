import pandas as pd
from googleapiclient.discovery import  build
import json
import streamlit as st

st.title(' *Scraping of data from youtube* ')
#Google API key
api_key ="AIzaSyCUx0HzmRODWfvrIUF1Q9LJTRG8DTfmzGs" 

#cannel-id - unique identifier 
channel_id=["UCXhbCCZAG4GlaBLm80ZL-iA"]

for id in channel_id:
    st.subheader('Channel_id')
    st.write(id)

#to initalize youtube_services
youtube=build('youtube','v3',developerKey=api_key)

#send a request to youtube API
def get_details(youtube,channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",id=channel_id)
    response1 = request.execute()
    return response1

channel_details=get_details(youtube,channel_id)



#print(type(channel_details))
#result=get_details['items'][0]['snippet']['title']

#getting commands


def get_response(youtube, channel_id):
    # Use the 'search' API to retrieve comments
    request = youtube.commentThreads().list(
        part="snippet",
        allThreadsRelatedToChannelId=channel_id
    )
    response = request.execute()
    return response

comment=get_response(youtube,channel_id)   

def get_video(youtube):
    request = youtube.videos().list(
    part='snippet,statistics',  id="Ks-_Mh1QhMc" # Include both snippet (metadata) and statistics
    )
    response = request.execute()
    return response

video_details=get_video(youtube)

def get_playlists(youtube, channel_id):
    request = youtube.playlists().list(
        part="snippet",
        channelId=channel_id,
        maxResults=5  # You can adjust the number of results you want
    )
    response = request.execute()
    return response

playlists=get_playlists(youtube,channel_id)

#converting dict into json format

#channel_json = json.dumps(channel_details)



# moving data to MongoDB
#import pymango
#create cilent by using pymongo.Mongocilent()
#connect to mongodatabase
#connect to collections
 


import pymongo


client = pymongo.MongoClient()

prodb=client['project_webscraping']
pro_collection=prodb.channel
pro_collection.insert_one({"channel_details":channel_details})

prodb=client['project_webscraping']
pro_collection=prodb.comment
pro_collection.insert_one({"comment":comment})


prodb=client['project_webscraping']
pro_collection=prodb.video
pro_collection.insert_one({'video':video_details})

prodb=client['project_webscraping']
pro_collection=prodb.playlists
pro_collection.insert_one({'play_list':playlists})

st.success('data inserted sucessfully')

client.close()





