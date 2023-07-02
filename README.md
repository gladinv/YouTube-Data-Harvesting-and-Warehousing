# YouTube-Data-Harvesting-and-Warehousing
Python scripting, Data Collection, MongoDB, Streamlit, API integration, Data Managment using MongoDB (Atlas) and SQL

Here's a stepwise walkthrough of the code:

1. Importing necessary libraries:
```python
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pymongo
import psycopg2
import pandas as pd
import streamlit as st
```
The code imports the required libraries for working with the YouTube API (using `googleapiclient`), MongoDB (using `pymongo`), PostgreSQL (using `psycopg2`), data manipulation (using `pandas`), and building web apps (using `streamlit`).

2. API and database connections:
```python
api_key = "YOUR_API_KEY"
api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=api_key)

ytproject = psycopg2.connect(host='localhost', user='postgres', password='1234', database='youtube')  # PostgreSQL connection
project = pymongo.MongoClient("mongodb://localhost:27017/")  # MongoDB connection
```
The code sets up a connection to the YouTube API using the provided API key. It also establishes connections to a PostgreSQL database (`ytproject`) and a MongoDB database (`project`).

3. Functions for retrieving channel, playlist, video, and comment details:
The code defines several functions that make API requests and retrieve specific details from the YouTube API. These functions include:
- `youtube_channel(youtube, channel_id)`: Retrieves details about a YouTube channel.
- `get_playlists(youtube, channel_id)`: Retrieves details about playlists belonging to a channel.
- `channel_videoId(youtube, playlist_Id)`: Retrieves video IDs from a playlist.
- `video_details(youtube, video_Id)`: Retrieves details about a video.
- `get_comments_in_videos(youtube, video_id)`: Retrieves comments for a video.

4. Functions for importing data to MongoDB and PostgreSQL:
The code defines functions for importing data retrieved from the YouTube API into MongoDB and PostgreSQL databases. These functions include:
- `channel_Details(channel_id)`: Retrieves channel details, playlists, videos, and comments using the API functions and stores them in the respective collections in MongoDB.
- `channel_table()`, `playlist_table()`, `videos_table()`, `comments_table()`: Create tables in the PostgreSQL database and insert data from the corresponding collections in MongoDB.

5. Channel IDs:
The code defines several channel IDs for which the data will be retrieved and imported into the databases.

6. Functions for displaying data:
The code defines several functions for displaying the data stored in the PostgreSQL database. These functions include:
- `display_channels()`: Retrieves and displays data from the "channel" table.
- `display_videos()`: Retrieves and displays data from the "videos" table.
- `display_playlists()`: Retrieves and displays data from the "playlists" table.
- `display_comments()`: Retrieves and displays data from the "comments" table.

7. Required data to view:
The code defines a function (`q1()`) that executes a SQL query to retrieve specific data from the "videos" table.

8. The code ends with function calls to perform the required operations:
- `tables()`: Creates tables and imports data into the PostgreSQL database.
- `display_channels()`, `display_videos()`, `display_playlists()`, `display_comments()`: Displays the data from the corresponding tables in the PostgreSQL database.

Note: The code provided here assumes that you have set up the required API key, database connections, and have the necessary databases and collections available. You may need to modify the code to fit your specific setup and requirements.
