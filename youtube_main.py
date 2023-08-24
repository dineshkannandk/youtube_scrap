from  googleapiclient.discovery import build
import mysql.connector as connect
import pymongo
import streamlit as st
import pandas as pd

st.title('Data Analysing with Youtube API')



#Google API key
api_key='AIzaSyCUx0HzmRODWfvrIUF1Q9LJTRG8DTfmzGs'

#cannel-id - unique identifier 
channel_ids=['UCjDnt2b8-I7bu4MRF9Uwf-A','UC26AqprjUnguEQgHIXLSzRg']

#to initalize youtube_services
youtube=build('youtube','v3',developerKey=api_key)



#Get channel details
def get_channel(youtube,channel_ids):
    all_data=[]
    request=youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_ids)
    )
    response=request.execute()

    for i in range(len(response['items'])):           
            data=dict(channel_idd=response['items'][i]['id'],
            channel_name= response['items'][i]['snippet']['title'],
            channel_description=response['items'][i]['snippet']['description'],
            channel_viewCount= response['items'][i]['statistics']['viewCount'] )
            all_data.append(data)
    return all_data

channel=get_channel(youtube,channel_ids)

print(channel)

pf=pd.DataFrame(data=channel)

def get_playlists(youtube,channel_ids):
    for i in channel_ids:
        request = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=i,
        maxResults=25
    )
    
    response = request.execute()
    
    data=dict(play_list_id =response['items'][0]['id'],
    play_list_channelId=response['items'][0]['snippet']['channelId'],
    play_list_title = response['items'][0]['snippet']['title'])
   
    data1=dict(play_list_id =response['items'][1]['id'],
    play_list_channelId=response['items'][1]['snippet']['channelId'],
    play_list_title = response['items'][1]['snippet']['title'])

    data2=dict(play_list_id =response['items'][2]['id'],
    play_list_channelId=response['items'][2]['snippet']['channelId'],
    play_list_title = response['items'][2]['snippet']['title'],)
     
    data3=dict(play_list_id =response['items'][3]['id'],
    play_list_channelId=response['items'][3]['snippet']['channelId'],
    play_list_title = response['items'][3]['snippet']['title'])

    return[data,data1,data2,data3]

play_list=get_playlists(youtube,channel_ids)

print(play_list)

pf = pd.DataFrame(play_list)

   


def video_details(youtube):   
        request = youtube.videos().list(
        part="snippet,contentDetails,statistics",id='5LqQk_kh6t0'
      
    )
        response = request.execute()
        video_data=dict(video_id = response['items'][0]['id'],
                        video_channel_id=response['items'][0]['snippet']['channelId'],
                        description=response['items'][0]['snippet']['description'],
                        tags=response['items'][0]['snippet']['tags'],
                        publishedAt=response['items'][0]['snippet']['publishedAt'],
                        video_likes=response['items'][0]['statistics']['likeCount'],
                        video_count=response['items'][0]['statistics']['viewCount'],
                        comment_count=response['items'][0]['statistics']['commentCount'],
                        favoriteCount=response['items'][0]['statistics']['favoriteCount'],
                        channel_title=response['items'][0]['snippet']['channelId'])
        return video_data

video=video_details(youtube)

print(video)

pf=pd.DataFrame(video)



#connecting data to mongo db

import pymongo

client=pymongo.MongoClient()

datadb=client['project_data']
collections = datadb.channel
collections.insert_one({"channel":channel})


datadb=client['project_data']
collections = datadb.video
collections.insert_one({"video":video})


datadb=client['project_data']
collections = datadb.play_list
collections.insert_one({"play_list":play_list})

st.success('data inserted sucessfully')
print('data inserted sucessfully')

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