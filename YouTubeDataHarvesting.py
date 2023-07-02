#!/usr/bin/env python
# coding: utf-8

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pymongo
import psycopg2
import pandas as pd
import streamlit as st

## api connection
api_key="AIzaSyD36RL4YEksFi5SrPO3JHsMizI3QfqoyQA"
api_service_name="youtube"
api_version="v3"
youtube = build(api_service_name, api_version, developerKey=api_key)

## postgresql connection
ytproject=psycopg2.connect(host='localhost',user='postgres',password='1234',database='youtube')   #enter your connection details
cursor=ytproject.cursor()
## mongodb atlas connection
project=pymongo.MongoClient("mongodb://localhost:27017/")


# # get channel details

def youtube_channel(youtube,channel_id):

    request= youtube.channels().list(
        id=channel_id,
        part="snippet,contentDetails,statistics"
       )
    response=request.execute()

    for item in response['items']:                                        # iterate through every item in "items" element in responce
        data={'channelName':item['snippet']['title'],                       #displaying only reqired items nested in snippet-->title
              'channel_id':item['id'],
              'subscribers':item['statistics']['subscriberCount'],
              'views':item['statistics']['viewCount'],
              'totalVideos':item['statistics']['videoCount'],
              'playlistId':item['contentDetails']['relatedPlaylists']['uploads'],
              'channel_description':item['snippet']['description']
            }
   
    return(data)


# # get play list details

def get_playlists(youtube,channel_id):
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=channel_id,
        maxResults=25
        )
    response = request.execute()
    All_data=[]
    for item in response['items']: #these are the details we are getting about the playlist
        data={'PlaylistId':item['id'],
              'Title':item['snippet']['title'],
              'ChannelId':item['snippet']['channelId'],
              'ChannelName':item['snippet']['channelTitle'],
              'PublishedAt':item['snippet']['publishedAt'],
              'VideoCount':item['contentDetails']['itemCount']
              }
        All_data.append(data)

        next_page_token = response.get('nextPageToken')

        while next_page_token is not None:
                
                request = youtube.playlists().list(
                    part="snippet,contentDetails",
                    channelId="UCmXkiw-1x9ZhNOPz0X73tTA",
                    maxResults=25)
                response = request.execute()  
                      
                for item in response['items']:
                    data={'PlaylistId':item['id'],
                           'Title':item['snippet']['title'],
                           'ChannelId':item['snippet']['channelId'],
                           'PublishedAt':item['snippet']['publishedAt'],
                           'VideoCount':item['contentDetails']['itemCount']}
                    All_data.append(data)
                next_page_token = response.get('nextPageToken')
    return All_data


# # get video id

def channel_videoId(youtube,playlist_Id):
    video_Ids=[]
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=50,
        playlistId=playlist_Id
        )
    response = request.execute()

    for i in range(len(response['items'])):
        video_Ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    more_pages = True

    while  more_pages:
        if next_page_token is None:
            more_pages=False
        else:
            request = youtube.playlistItems().list(
                      part='contentDetails',
                      playlistId = playlist_Id,
                      maxResults = 50,
                      pageToken = next_page_token)
            response = request.execute()

            for i in range(len(response['items'])):
                video_Ids.append(response['items'][i]['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')
    return video_Ids


# # get individual video details

def video_details(youtube, video_Id):
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_Id,
    )
    response = request.execute()
    video_info = {}
    for video in response['items']:
        stats_to_keep = {
            'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt', 'channelId'],
            'statistics': ['viewCount', 'likeCount', 'favoriteCount', 'commentCount'],
            'contentDetails': ['duration', 'definition', 'caption']
        }
        
        video_info['video_id'] = video['id']
        for key in stats_to_keep.keys():
            for value in stats_to_keep[key]:
                try:
                    video_info[value] = video[key][value]
                except KeyError:
                    video_info[value] = None

    return video_info


# # get comment details

def get_comments_in_videos(youtube, video_id):
    all_comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id
        )
        response = request.execute()

        for item in response['items']:
            data={'comment_id':item['snippet']['topLevelComment']['id'],
                  'comment_txt':item['snippet']['topLevelComment']['snippet']['textOriginal'],
                  'videoId':item['snippet']['topLevelComment']["snippet"]['videoId'],
                  'author_name':item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                  'published_at':item['snippet']['topLevelComment']['snippet']['publishedAt'],
            }

            all_comments.append(data)

    except:
        
        return 'Could not get comments for video '

    return all_comments


# # import data to pymongo

db=project["youtube_project"]

@st.cache_data       #to use cache data on re runs of functions

def channel_Details(channel_id):
    det = youtube_channel(youtube, channel_id)
    col = db["Channels"]
    col.insert_one(det)

    playlist = get_playlists(youtube, channel_id)
    col = db["playlists"]
    for i in playlist:
        col.insert_one(i)
        Playlist = i.get('PlaylistId')  # Use the playlist ID from the current playlist item
        videos = channel_videoId(youtube, Playlist)

    for video in videos:
        v = video_details(youtube, video)
        col = db["videos"]
        col.insert_one(v)
        com = get_comments_in_videos(youtube, video)
        if com != 'Could not get comments for video ':
            for comment in com:
                col = db["comments"]
                col.insert_one(comment)

    return "Process for " + channel_id + " is completed"

# # channel ids

ThuVu_data_analytics="UCJQJAI7IjbLcpsjWdSzYz0Q"
adrascentral="UCGBnz-FR3qaowYsyIEh2-zw"
kennysebastian="UCzNq9i-DlDDBLjPerVzJW-A"
hiphopthamizha="UC3Izrk2fUSIEwdcH0kNdzeQ"
fiver="UCZOWiLLJ2QzS4Z0g7L1mtgw"
evamtamasha="UCY6S78uy7ViTx5-Wc029oqA"
eastindiacompany="UCpU9EZn1Ll9kPpSuBsn4VyA"
coinstatics="UCB7BryuXaMe1pUMznYAq4Jg"
beingthamizha="CF1wPTEdK3RZclxruliajcg"
manojmaddy="UC_6StvbTS_SIl70mqubrwvw"



# # channel table creation

def channel_table():
    
    try:
        cursor.execute("""create table if not exists channel 
                        (channelName varchar(50),
                        channelId varchar(100) primary key,
                        subscribers bigint,
                        views bigint, 
                        totalVideos int,
                        playlistId varchar(80),
                        channel_description text)"""
                      )
        ytproject.commit()
    except:
        ytproject.rollback()

    db=project["youtube_project"]
    col=db["Channels"]
    data=col.find()
    doc=list(data)
    df=pd.DataFrame(doc)
    try:
        for _, row in df.iterrows():
            insert_query = '''
                INSERT INTO channel (channelName, channelId, subscribers, views, totalVideos, playlistId, channel_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            values = (
                row['channelName'],
                row['channel_id'],
                row['subscribers'],
                row['views'],
                row['totalVideos'],
                row['playlistId'],
                row['channel_description']
            )
            try:
                cursor.execute(insert_query, values)
                ytproject.commit()
            except:
                ytproject.rollback()

    except:
        st.write("values already exist in channels table")


# # table for playlist

def playlist_table():
    try:
        cursor.execute("""create table if not exists playlists
               (PlaylistId varchar(80) primary key,
                Title varchar(100),
                ChannelId varchar(100),
                ChannelName varchar(50),
                PublishedAt timestamp,
                VideoCount int)""")
        ytproject.commit()
    except:
        project.rollback()
        
    col=db["playlists"]
    data1=col.find()
    doc1=list(data1)
    df1=pd.DataFrame(doc1)
    try:
        for _, row in df1.iterrows():
            insert_query = '''
                            INSERT INTO playlists (PlaylistId, Title, ChannelId, ChannelName, PublishedAt, VideoCount)
                            VALUES (%s, %s, %s, %s, %s, %s)  '''       
                           
            values = (
                row['PlaylistId'],
                row['Title'],
                row['ChannelId'],
                row['ChannelName'],
                row['PublishedAt'],
                row['VideoCount']
                )
            try:
                cursor.execute(insert_query,values)
                ytproject.commit()
            except:
                ytproject.rollback()
    except:
        st.write("values already exist in playlist table") 


# # table for videos

def videos_table():
    try:
        cursor.execute("""create table if not exists videos
                        (video_id varchar(50)  primary key,
                        channelTitle varchar(150),
                        title varchar(150),
                        description text,
                        tags text,
                        publishedAt timestamp,
                        viewCount bigint,
                        likeCount bigint,
                        favoriteCount bigint,
                        commentCount int,
                        duration varchar(15),
                        definition varchar(10),
                        caption varchar(10),
                        ChannelId varchar(100))""")
        ytproject.commit()
    except:
        ytproject.rollback()
        
    col2=db["videos"]
    data2=col2.find()
    doc2=list(data2)
    df2=pd.DataFrame(doc2)
    try:
        for _, row in df2.iterrows():
            insert_query = '''
                INSERT INTO videos (video_id, channelTitle,  title, description, tags, publishedAt, 
                viewCount, likeCount, favoriteCount, commentCount, duration, definition, caption, channelId)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

            '''
            values = (
                row['video_id'],
                row['channelTitle'],
                row['title'],
                row['description'],
                row['tags'],
                row['publishedAt'],
                row['viewCount'],
                row['likeCount'],
                row['favoriteCount'],
                row['commentCount'],
                row['duration'],
                row['definition'],
                row['caption'],
                row['channelId']
            )
            try:
                cursor.execute(insert_query,values)
                ytproject.commit()
            except:
                ytproject.rollback()
    except:
        st.write("values aready exists in the videos table")


# # table for comments

def comments_table():
    try:
        cursor.execute("""create table if not exists comments
               (comment_id varchar(100)  primary key,
               comment_txt text,
               videoId varchar(80),
               author_name varchar(150),
               published_at timestamp)""")
        ytproject.commit()
    except:
        project.rollback()
        
    col3=db["comments"]
    data3=col3.find()
    doc3=list(data3)
    df3=pd.DataFrame(doc3)
    try:
        for _, row in df3.iterrows():
            insert_query = '''
                INSERT INTO comments (comment_id, comment_txt, videoId, author_name, published_at)
                VALUES (%s, %s, %s, %s, %s)
                '''
            values = (
            row['comment_id'],
            row['comment_txt'],
            row['videoId'],
            row['author_name'],
            row['published_at']
            )
            try:
                cursor.execute(insert_query,values)
                ytproject.commit()
            except:
                ytproject.rollback() 
    except:
           st.write("values already exist in comments table")        

            
            
def tables():
    channel_table()
    playlist_table()
    videos_table()
    comments_table()
    return ("done")   

def display_channels():
    try:
        cursor.execute("select * from channel;")
        channeltb=cursor.fetchall()
        channeltb=st.dataframe(channeltb)
        return channeltb
    except:
        ytproject.rollback()
        cursor.execute("select * from channel;")
        channeltb=cursor.fetchall()
        channeltb=st.dataframe(channeltb)
        return channeltb

def display_videos():
    try:
        cursor.execute("select * from videos;")
        videotb=cursor.fetchall()
        videotb=st.dataframe(videotb)
        return videotb
    except:
        ytproject.rollback()
        cursor.execute("select * from videos;")
        videotb=cursor.fetchall()
        videotb=st.dataframe(videotb)
        return videotb
    
def display_playlists():
    try:
        cursor.execute("select * from playlists;")
        playlisttb=cursor.fetchall()
        playlisttb=st.dataframe(playlisttb)
        return playlisttb
        
    except:
        ytproject.rollback()
        cursor.execute("select * from playlists;")
        playlisttb=cursor.fetchall()
        playlisttb=st.dataframe(playlisttb)
        return playlisttb
          
def display_comments():
    try:
        cursor.execute("select * from comments;")
        commentstb=cursor.fetchall()
        commentstb=st.dataframe(commentstb)
        return commentstb
    except:
        ytproject.rollback()
        cursor.execute("select * from comments;")
        commentstb=cursor.fetchall()
        commentstb=st.dataframe(commentstb)
        return commentstb   

# # required data to view   
    
def q1():
    cursor.execute("select title as videos, channeltitle as chanel_name from videos;")
    ytproject.commit()
    t1=cursor.fetchall()
    t1=st.dataframe(t1)
    return t1

def q2():
    cursor.execute("select channelName as ChannelName,totalvideos No_Videos from channel order by totalvideos desc limit 1;")
    ytproject.commit()
    t2=cursor.fetchall()
    t2=st.dataframe(t2)
    return t2

def q3():
    cursor.execute('''select viewcount views , channeltitle as ChannelName,title as Name from videos 
                    where viewcount is not null order by viewcount desc limit 10;''')
    ytproject.commit()
    t3=cursor.fetchall()
    t3=st.dataframe(t3)
    return t3

def q4():
    cursor.execute("select commentcount as No_comments ,title as Name from videos where commentcount is not null;") 
    ytproject.commit()
    t4=cursor.fetchall()
    t4=st.dataframe(t4)
    return t4

def q5():
    cursor.execute('''select title as Videeo, channeltitle as ChannekName, likecount as Likes from videos 
                   where likecount is not null order by likecount desc;''')
    ytproject.commit()
    t5=cursor.fetchall()
    t5=st.dataframe(t5)
    return t5

def q6():
    cursor.execute('''select likeCount as likes from videos;''')
    ytproject.commit()
    t6=cursor.fetchall()
    t6=st.dataframe(t6)
    return t6

def q7():
    cursor.execute("select channelName as ChannelName, views as Channelviews from channel;")
    ytproject.commit()
    t7=cursor.fetchall()
    t7=st.dataframe(t7)
    return t7

def q8():
    cursor.execute('''select title as name, publishedat as VideoRelease, channeltitle as ChannelName from videos 
                   where extract(year from publishedat) = 2022;''')
    ytproject.commit()
    t8=cursor.fetchall()
    t8=st.dataframe(t8)
    return t8

def q9():
    cursor.execute('''select title as Name, channelTitle as ChannelName, commentCount as Comments from videos 
                   where commentCount is not null order by commentCount desc;''')
    ytproject.commit()
    t10=cursor.fetchall()
    t10=st.dataframe(t10)
    return t10        

# # streamlit # #

st.title("YOUTUBE DATA HARVESTING AND WAREHOUSING")
st.caption("you can get all the data of the channel you want" )

options=st.multiselect(
    "select the channel here",
[ThuVu_data_analytics,adrascentral,kennysebastian,hiphopthamizha,fiver,evamtamasha,eastindiacompany,coinstatics,beingthamizha,manojmaddy],
[])
          
st.write("You selected:", options)
          
if st.button("collect and store data"):
    for i in options:
        output=channel_Details(i)
        st.write(output)
             
st.write("click here to migrate the data in sql tables")
if st.button("migrate"):
    display=tables()
    st.write(display)
             
             
frames=st.radio(
    "select the table you want to view", 
    ("none","Channel" ,"Playlist", "video", "Comment"))

st.write("You selected:", frames)
     
if frames=="none":
    st.write( "select a table")
elif frames=="Channel":
    display_channels()
elif frames=="Playlist":
     display_playlists()
elif frames=="video":
     display_videos()
elif frames=="Comment":
     display_comments()
             
query=st.selectbox(
    "To view data",
    ("none","to view a channel and all it's videos","channels with highest no. of videos",
     "top 10 most viewed videos","comments in each video","videos with most no. of views",
     "no. of likes of all videos","views of each channel","videos published in year 2022",
     "videos with highest no. of comments"))

if query=="none":
    st.write("select a option")
if query=="to view a channel and all it's videos":
    q1()
elif query=="channels with highest no. of videos":
    q2()
elif query=="top 10 most viewed videos":
    q3()
elif query=="comments in each video":
    q4()
elif query=="videos with most no. of views":
    q5()
elif query=="no. of likes of all videos":
    q6()
elif query=="views of each channel":
    q7()
elif query=="videos published in year 2022":
    q8()
elif query=="videos with highest no. of comments":
    q9()
