from  googleapiclient.discovery import build
import mysql.connector as connect
import pymongo
import streamlit as st
import pandas as pd
import pymongo
import sqlalchemy
from sqlalchemy import create_engine,String,Integer,MetaData,Text,Column




# Set Streamlit page configuration
st.set_page_config(
    page_title="youtube_scraping",
    page_icon='🚇'
)

# Title for the app
st.title('Data Analysis with YouTube API')

# Options for user selection
options = ["channel_Analysis", "playlist_Analysis", "video_Analysis"]
selected_option = st.sidebar.radio("Select an option:", options)

# Google API key
api_key = 'AIzaSyCUx0HzmRODWfvrIUF1Q9LJTRG8DTfmzGs'
# Channel IDs
channel_ids = ['UCjDnt2b8-I7bu4MRF9Uwf-A', 'UC26AqprjUnguEQgHIXLSzRg','UCD6cIMMWwBeFT1RSsOXBOJg','UCiT9RITQ9PW6BhXK0y2jaeg','UCwnjkBGhMfrNjDBA3BjwVeA']
# Initialize YouTube service
youtube = build('youtube', 'v3', developerKey=api_key)
client=pymongo.MongoClient()



if selected_option == "channel_Analysis":
    # Function to get channel data
    def get_channel(youtube, channel_ids):
        all_data = []
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=','.join(channel_ids)
        )
        response = request.execute()

        for item in response['items']:
            data = {
                'channel_id': item['id'],
                'channel_name': item['snippet']['title'],
                'channel_description': item['snippet']['description'],
                'channel_viewCount': item['statistics']['viewCount']
            }
            all_data.append(data)
        return all_data

    channel_data = get_channel(youtube, channel_ids)
    df = pd.DataFrame(data=channel_data)
    st.write(df)
    st.bar_chart(df,x="channel_name",y="channel_viewCount")

    channel = channel_data
    datadb=client['project_data']
    collections = datadb.channel
    collections.insert_one({"channel":channel})
    st.success('data inserted sucessfully')
    print('data inserted sucessfully')


elif selected_option == "playlist_Analysis":
    # Function to get playlist data
    def get_playlists(youtube, channel_ids):
        playlist_data = []
        for channel_id in channel_ids:
            request = youtube.playlists().list(
                part="snippet,contentDetails",
                channelId=channel_id,
                maxResults=25
            )
            response = request.execute()

            for item in response['items']:
                data = {
                    'play_list_id': item['id'],
                    'play_list_channelId': item['snippet']['channelId'],
                    'play_list_title': item['snippet']['title']
                }
                playlist_data.append(data)
        return playlist_data

    playlist_data = get_playlists(youtube, channel_ids)
    ppf = pd.DataFrame(playlist_data)
    st.write(ppf)
    st.bar_chart(data=ppf , x="play_list_id", y="play_list_title")

    play_list=playlist_data
    datadb=client['project_data']
    collections = datadb.play_list
    collections.insert_one({"play_list":play_list})
    st.success('data inserted sucessfully')
    print('data inserted sucessfully')
    


elif selected_option == "video_Analysis":
    # Function to get video data
    def get_video_details(youtube):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=['5LqQk_kh6t0','u003dvNHE7YOosU4']
        )
        response = request.execute()
        item = response['items'][0]
        video_data = {
            'video_id': item['id'],
            'video_channel_id': item['snippet']['channelId'],
            'description': item['snippet']['description'],
            'tags': item['snippet']['tags'],
            'publishedAt': item['snippet']['publishedAt'],
            'video_likes': item['statistics']['likeCount'],
            'video_count': item['statistics']['viewCount'],
            'comment_count': item['statistics']['commentCount'],
            'favoriteCount': item['statistics']['favoriteCount'],
            'channel_title': item['snippet']['channelTitle']
        }
        return video_data

    video_data = get_video_details(youtube)
    df=pd.DataFrame(video_data)
    st.write(df)
    video=video_data
    datadb=client['project_data']
    collections = datadb.video
    collections.insert_one({"video":video})
    st.success('data inserted sucessfully')
    print('Data inserted sucessfully')
    
    

client.close()





#inserting data into sql

import mysql.connector as connect
import streamlit as st

mydb=connect.connect(
    host='localhost',
    user='root',
    password='1234',
    database='project'
)

mycursor=mydb.cursor()
print('connection started')

