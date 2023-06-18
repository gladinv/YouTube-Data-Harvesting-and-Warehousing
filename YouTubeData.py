#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymongo
import sqlite3
import pandas as pd
import streamlit as st

# Function to store data in a MongoDB data lake
def store_data_in_mongodb(channel_data):
    # Set up the MongoDB client
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    # Select the database and collection to store the data
    db = client["youtube"]
    collection = db["channel_data"]
    # Insert the channel data into the collection
    collection.insert_one(channel_data)

# Function to migrate data from the MongoDB data lake to a SQLite data warehouse
def migrate_data_to_sqlite():
    # Set up the MongoDB client
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    # Select the database and collection to retrieve the data
    db = client["youtube"]
    collection = db["channel_data"]

    # Set up the SQLite connection and cursor
    conn = sqlite3.connect("youtube.db")
    cur = conn.cursor()

    # Create the tables in the SQLite database
    cur.execute('''CREATE TABLE IF NOT EXISTS channels
                   (channel_id text PRIMARY KEY, channel_name text, subscribers integer, video_count integer)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS videos
                   (video_id text PRIMARY KEY, channel_id text, title text, description text, publish_time text,
                    views integer, likes integer, dislikes integer, comments integer)''')

    # Retrieve the data from the MongoDB data lake
    data = list(collection.find())

    # Insert the data into the SQLite tables
    for item in data:
        # Insert data into the channels table
        channel_id = item['channel_id']
        channel_name = item['channel_name']
        subscribers = item['subscribers']
        video_count = item['video_count']

        cur.execute("INSERT INTO channels VALUES (?, ?, ?, ?)", (channel_id, channel_name, subscribers, video_count))

        # Insert data into the videos table
        for video in item['videos']:
            video_id = video['video_id']
            title = video['title']
            description = video['description']
            publish_time = video['publish_time']
            views = video['views']
            likes = video['likes']
            dislikes = video['dislikes']
            comments = video['comments']

            cur.execute("INSERT INTO videos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (video_id, channel_id, title, description, publish_time, views, likes, dislikes, comments))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Data migration to SQLite is complete.")

def query_sqlite_data(selected_channel):
    conn = sqlite3.connect("youtube.db")
    cur = conn.cursor()

    # Join the channel_data and channel_details tables to get the channel details
    cur.execute("""SELECT channel_data.channel_name, channel_data.subscribers, 
                channel_data.video_count, channel_data.playlist_id, 
                channel_data.video_id, channel_data.likes, channel_data.dislikes, 
                channel_data.comments, channel_details.description, 
                channel_details.view_count, channel_details.comment_count, 
                channel_details.published_date 
                FROM channel_data 
                JOIN channel_details ON channel_data.channel_id = channel_details.channel_id 
                WHERE channel_data.channel_name = ?""", (selected_channel,))

    # Fetch the data and store it in a DataFrame
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=["Channel Name", "Subscribers", "Total Videos", 
                                    "Playlist ID", "Video ID", "Likes", "Dislikes", 
                                    "Comments", "Description", "View Count", 
                                    "Comment Count", "Published Date"])

    # Close the connection
    conn.close()

    return df

def app():
    st.set_page_config(page_title="YouTube Data Warehousing App")

    # Set up the sidebar
    st.sidebar.title("YouTube Data Warehouse")
    menu = ["Home", "Data Collection", "SQL Data Warehouse", "About"]
    choice = st.sidebar.selectbox("Select an option", menu)

    # Set up the home page
    if choice == "Home":
        st.title("Welcome to the YouTube Data Warehousing App")
        st.write("This app allows you to collect and analyze data from multiple YouTube channels.")

    # Set up the data collection page
    elif choice == "Data Collection":
        st.title("Data Collection")

        # Get the API key from the user
        api_key = st.text_input("Enter your Google API key")

        # Get the channel IDs from the user
        st.write("Enter the YouTube channel IDs for the channels you want to collect data for:")
        channel_ids = st.text_area("Enter channel IDs, separated by commas")
        channel_list = [x.strip() for x in channel_ids.split(",")]

        # Get the data for each channel and store it in the MongoDB data lake
        if st.button("Collect Data"):
            for channel_id in channel_list:
                data = get_channel_data(api_key, channel_id)
                store_data_in_mongodb(data)

            st.write("Data collection complete.")

        # Display the data in the MongoDB data lake
        if st.button("View Data in MongoDB"):
            data = view_data_in_mongodb()
            st.write(data)

    # Set up the SQL data warehouse page
    elif choice == "SQL Data Warehouse":
        st.title("SQL Data Warehouse")

        # Get the channel names from the user
        st.write("Select a channel to view its data:")
        channels = get_channels_from_mongodb()
        selected_channel = st.selectbox("Select a channel", channels)

        # Migrate data from the MongoDB data lake to the SQLite data warehouse
        if st.button("Migrate Data to SQL"):
            migrate_data_to_sqlite()

        # Query the SQLite data warehouse and display the data
        if st.button("View Data in SQL"):
            data = query_sqlite_data(selected_channel)
            st.write(data)

    # Set up the about page
    elif choice == "About":
        st.title("About")
        st.write("This app was created by [Your Name] as a project for [Course Name].")

