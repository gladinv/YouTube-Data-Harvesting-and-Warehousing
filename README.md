# YouTube-Data-Harvesting-and-Warehousing
Python scripting, Data Collection, MongoDB, Streamlit, API integration, Data Managment using MongoDB (Atlas) and SQL

Here's a stepwise walkthrough of the code:

Step 1: Import the required libraries:
```python
import streamlit as st
import pandas as pd
import pymongo
from sqlalchemy import create_engine
from sqlalchemy import text
from googleapiclient.discovery import build
import json
from googleapiclient.errors import HttpError
import numpy as np
```

Step 2: Create a connection to the SQLite database and YouTube API:
```python
engine = create_engine('sqlite:///youtube.db', echo=False)
conn = engine.connect()

api_key = "YOUR_API_KEY"
youtube = build('youtube', 'v3', developerKey=api_key)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.Youtube_Data
```

Step 3: Define functions for fetching and processing YouTube data:
- `check_channel_id(channel_id)`: Checks if a given YouTube channel ID is valid.
- `get_channel_info(channel_id)`: Retrieves information about a YouTube channel.
- `get_channel_details(channel_id)`: Retrieves detailed information about a YouTube channel.
- `get_channel_videos(channel_id)`: Retrieves the video IDs of all videos in a YouTube channel.
- `get_video_details(v_ids)`: Retrieves detailed information about a list of video IDs.
- `get_comments_details(v_id)`: Retrieves details of comments for a given video ID.
- `channels_name()`: Retrieves the names of all channels stored in the MongoDB database.
- `insert_into_channels()`: Inserts channel data into the SQLite database.
- `insert_into_videos()`: Inserts video data into the SQLite database.
- `insert_into_comments()`: Inserts comment data into the SQLite database.
- `execute_query(question_index)`: Executes predefined queries on the SQLite database.
```python
# The functions mentioned above are defined in the provided code.
```

Step 4: Define a list of questions for data analysis.
```python
question_list = [
    "What are the names of all the videos and their corresponding channels?",
    "Which channels have the most number of videos, and how many videos do they have?",
    "What are the top 10 most viewed videos and their respective channels?",
    "How many comments were made on each video, and what are their corresponding video names?",
    "Which videos have the highest number of likes, and what are their corresponding channel names?",
    "What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
    "What is the total number of views for each channel, and what are their corresponding channel names?",
    "What are the names of all the channels that have published videos in the year 2022?",
    "What is the average duration of all videos in each channel, and what are their corresponding channel names?",
    "Which videos have the highest number of comments, and what are their corresponding channel names?"
]
```

Step 5: Define the `execute_query(question_index)` function to execute queries based on the selected question index.
```python
# The execute_query function is already defined in the provided code.
```

Step 6: Create the Streamlit application layout and logic.
```python
# Page Configuration
st.set_page_config(page_title="YouTube Data Harvesting and Warehousing",
                   layout="wide",
                   initial_sidebar_state="expanded")

# Menu selection
selected_menu = st.sidebar.radio("Select a Menu", ("Fetch & Save", "Migrate", "Analyze data!"))

