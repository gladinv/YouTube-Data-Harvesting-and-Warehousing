# YouTube-Data-Harvesting-and-Warehousing
Python scripting, Data Collection, MongoDB, Streamlit, API integration, Data Managment using MongoDB (Atlas) and SQL

Import the necessary libraries:

Import the build function from googleapiclient.discovery to interact with the YouTube Data API.
Import streamlit for building the web application.
Import pymongo for interacting with MongoDB.
Import sqlite3 for interacting with SQLite.
Import pandas to work with data in tabular format.
Set up the YouTube API client:

Provide the API key obtained from the Google Developers Console.
Set the API service name as "youtube" and the version as "v3".
Use the build function to create a YouTube API client instance.
Define functions:

get_channel_data(channel_id): Retrieves channel data using the YouTube API.

Set up the YouTube API client using OAuth 2.0 authentication.
Call the YouTube API to retrieve the channel data and parse the response.
Store the channel data and video data in a dictionary.
Return the channel data.
store_data_in_mongodb(channel_data): Stores the channel data in a MongoDB data lake.

Set up the MongoDB client connection.
Select the database and collection to store the data.
Insert the channel data into the collection.
migrate_data_to_sqlite(): Migrates data from the MongoDB data lake to a SQLite data warehouse.

Set up the MongoDB client connection.
Set up the SQLite connection and cursor.
Create tables in the SQLite database if they don't exist.
Retrieve data from the MongoDB data lake.
Insert the data into the SQLite tables.
Commit the changes and close the connection.
query_sqlite_data(selected_channel): Executes a SQL query to retrieve data from the SQLite data warehouse.

Set up the SQLite connection and cursor.
Execute a SQL query to join the channel_data and channel_details tables based on the selected channel.
Fetch the data and store it in a DataFrame.
Close the connection.
Return the DataFrame.
Define the Streamlit application:

Define the app() function to set up the Streamlit application.
Use st.set_page_config() to configure the page title.
Set up the sidebar with menu options: Home, Data Collection, SQL Data Warehouse, and About.
Implement the Home page:

If the user selects the "Home" option, display a welcome message.
Implement the Data Collection page:

If the user selects the "Data Collection" option:
Get the API key from the user using st.text_input().
Prompt the user to enter YouTube channel IDs.
Collect data for each channel using the get_channel_data() function and store it in the MongoDB data lake.
Display a message indicating that data collection is complete.
Provide a button to view the data in MongoDB.
Implement the SQL Data Warehouse page:

If the user selects the "SQL Data Warehouse" option:
Display a dropdown menu with the available channels retrieved from the MongoDB data lake.
Provide a button to migrate the data from MongoDB to SQLite using the migrate_data_to_sqlite() function.
Provide a button to view the data in SQLite by executing the query_sqlite_data() function and displaying the result.
Implement the About page:

If the user selects the "About" option, display information about the application.
