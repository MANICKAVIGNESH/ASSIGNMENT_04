'''
import pymongo
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import missingno as msno
import folium
import streamlit as st

with st.sidebar:
    st.title(":orange[Airbnb Analysis]")
    st.header("Notes")
    st.caption("The all data get from airbnb website")

question = st.selectbox("select your question",("1. Missing values in price column",
                                                "2. A list of the Availability of room type",
                                                "3. A list of the Occupation on each year",
                                                "4. A list of the short-Term rental",
                                                "5. A list of the top host Listings Count",
                                                "6. A list of the top 20 host with Entire Home/Apartments Listings",
                                                "7. A list of the top 20 hosts with most Private Rooms",
                                                "8. A list of the neighborhood average prices map"))

#to get data from momgoDB

#import mongoClient parameter to take values
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

airbon_list = []
db = client["airbnb_database"]
collection_1 = db['listings']
for airbon_data in collection_1.find():                   #"{}" is used all channel details mongo db
    airbon_list.append(airbon_data)
df1 = pd.DataFrame(airbon_list)

if question == "1. Missing values in price column":


    # Assuming your DataFrame is called 'airbnb_df'

    # Define price ranges or bins (you can adjust these as needed)
    price_bins = [0, 50, 100, 150, 200, 250, 300, float('inf')]
    price_labels = ['missing data (%)', '50-100', '100-150', '150-200', '200-250', '250-300', '300+']

    # Categorize prices into bins
    df1['price_range'] = pd.cut(df1['price'], bins=price_bins, labels=price_labels)

    # Count the number of listings in each price range
    price_distribution = df1['price_range'].value_counts()

    # Plot pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(price_distribution, labels=price_distribution.index, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Prices')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


elif question == "2. A list of the Availability of room type":

        #to get data from momgoDB

    #import mongoClient parameter to take values
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)

    airbon_list = []
    db = client["airbnb_database"]
    collection_1 = db['listings']
    for airbon_data in collection_1.find():                   #"{}" is used all channel details mongo db
        airbon_list.append(airbon_data)
    df1 = pd.DataFrame(airbon_list)

    # Assuming df1 is your DataFrame containing the two columns 'room_type' and 'availability_365'

    # Create a new DataFrame with the desired columns
    df_room_type = pd.DataFrame({
        'room_type': df1['room_type'],
        'availability_365': df1['availability_365']
    })
    
    # Display the new DataFrame
    #print(df_room_type)


    # Assuming df_new is your DataFrame containing the 'room_type' and 'availability_365' columns

    # Group by room type and sum the availability
    df_sum = df_room_type.groupby('room_type')['availability_365'].agg(['sum', 'count']).reset_index()

    # Calculate the percentage availability for each room type
    df_sum['availability_percentage'] = (df_sum['sum'] / df_sum['sum'].sum()) * 100

    # Sort the DataFrame in descending order based on total availability
    df_sum = df_sum.sort_values(by='sum', ascending=False)

    # Create a bar chart with color-coded bars and percentage labels
    fig = px.bar(df_sum, x='room_type', y='sum', color='room_type',
                title='Availability of Room Types',
                text=df_sum.apply(lambda row: f"{row['count']} - {row['availability_percentage']:.2f}%", axis=1))

    # Customize layout
    fig.update_traces(textposition='outside')  # Set the text position
    fig.update_layout(yaxis=dict(title='Total Availability (days)'), xaxis=dict(title='Room Type'))  # Set axis titles
    fig.show()

elif question == "3. A list of the Occupation on each year":

        #to get data from momgoDB

    #import mongoClient parameter to take values
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)

    airbon_list = []
    db = client["airbnb_database"]
    collection_1 = db['listings']
    for airbon_data in collection_1.find():                   #"{}" is used all channel details mongo db
        airbon_list.append(airbon_data)
    df1 = pd.DataFrame(airbon_list)

    # Create a new DataFrame with the desired columns
    df_activity = pd.DataFrame({
        'id': df1['id'],    
        'name': df1['name'],
        'minimum_nights': df1['minimum_nights'].fillna(0),  # Replace NaN with 0 in 'minimum_nights'
        'price': df1['price'].fillna(0),  # Replace NaN with 0 in 'price'
        'number_of_reviews': df1['number_of_reviews'].fillna(0),  # Replace NaN with 0 in 'number_of_reviews'
        'last_review': pd.to_datetime(df1['last_review'])  # Convert 'last_review' to datetime format
    })

    # Extract year from 'last_review'
    df_activity['year'] = df_activity['last_review'].dt.year

    # Calculate occupation for each listing
    df_activity['occupation'] = df_activity['minimum_nights'] * df_activity['number_of_reviews']

    # Group by year and sum the occupation across all listings
    yearly_occupation = df_activity.groupby('year')['occupation'].sum().reset_index()

    # Sort the DataFrame by year in descending order
    yearly_occupation = yearly_occupation.sort_values(by='year', ascending=False)

    # Create a bar chart using Plotly
    fig = px.bar(yearly_occupation, x='year', y='occupation',
                labels={'year': 'Year', 'occupation': 'Occupation'},
                title='Occupation for Each Year')

    # Update layout for better readability
    fig.update_layout(
        xaxis=dict(title='Year', type='category'),
        yaxis=dict(title='Occupation')
    )

    # Show the plot
    fig.show()

elif question == "4. A list of the short-Term rental":

        #to get data from momgoDB

    #import mongoClient parameter to take values
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)

    airbon_list = []
    db = client["airbnb_database"]
    collection_1 = db['listings']
    for airbon_data in collection_1.find():                   #"{}" is used all channel details mongo db
        airbon_list.append(airbon_data)
    df1 = pd.DataFrame(airbon_list)

    # Create a new DataFrame with the desired columns
    df_short_term_rental = pd.DataFrame({
        'id': df1['id'],
        'minimum_nights': df1['minimum_nights'],
        'neighbourhood': df1['neighbourhood'],
        'price': df1['price'],
        'room_type': df1['room_type'],
        'availability_365': df1['availability_365']
    })
    # Display the new DataFrame
    #print(df_short_term_rental)

    # Filter the DataFrame to include only short-term rentals (if minimum_nights <= 30)
    short_term_rentals = df_short_term_rental[df_short_term_rental['minimum_nights'] <= 30]

    # Create a bar chart using Plotly
    fig = px.histogram(short_term_rentals, x='minimum_nights', title="Distribution of Minimum Nights for Short-Term Rentals",
                    color_discrete_sequence=px.colors.qualitative.Dark24)
    fig.update_layout(xaxis_title="Minimum Nights", yaxis_title="Count")
    fig.update_traces(text=short_term_rentals.groupby('minimum_nights').size().values, textposition='outside')
    fig.show()

elif question == "5. A list of the top host Listings Count":

        #to get data from momgoDB

    #import mongoClient parameter to take values
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)

    airbon_list = []
    db = client["airbnb_database"]
    collection_1 = db['listings']
    for airbon_data in collection_1.find():                   #"{}" is used all channel details mongo db
        airbon_list.append(airbon_data)
    df1 = pd.DataFrame(airbon_list)

    # Assuming your data is stored in a variable named 'airbnb_data'

    # Top Hosts
    top_hosts_df = df1[['host_id', 'host_name', 'calculated_host_listings_count']]


    # Assuming you have created DataFrames named top_hosts_df, home_apts_df, private_rooms_df, shared_rooms_df, and listings_df

    # Sort the DataFrames in descending order by the specified column(s)
    top_hosts_df_sorted = top_hosts_df.sort_values(by='calculated_host_listings_count', ascending=False)

    # Remove rows where all cells have the same value
    top_hosts_df_sorted.drop_duplicates(inplace=True)

    # Print the sorted and cleaned DataFrame
    #print("Top Hosts:")
    #print(top_hosts_df_sorted)

    # Assuming your DataFrame of top hosts is named 'top_hosts_df_sorted'

    # Select the top 20 hosts
    top_20_hosts = top_hosts_df_sorted.head(20)

    # Plot the bar chart
    fig = px.bar(top_20_hosts, x='host_name', y='calculated_host_listings_count', 
                title='Top 20 Hosts by Calculated Host Listings Count',
                labels={'host_name': 'Host Name', 'calculated_host_listings_count': 'Listings Count'})

    fig.show()

elif question == "6. A list of the top 20 host with Entire Home/Apartments Listings":


        #to get data from momgoDB

    #import mongoClient parameter to take values
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)

    airbon_list = []
    db = client["airbnb_database"]
    collection_1 = db['listings']
    for airbon_data in collection_1.find():                   #"{}" is used all channel details mongo db
        airbon_list.append(airbon_data)
    df1 = pd.DataFrame(airbon_list)

    # Assuming your DataFrame is called 'airbnb_df'

    # Filter the data for listings with room type 'Entire home/apt'
    entire_home_df = df1[df1['room_type'] == 'Entire home/apt']

    # Count the occurrences of each host name
    host_counts = entire_home_df['host_name'].value_counts()

    # Select the top 20 hosts
    top_20_hosts = host_counts.head(20)

    # Convert the counts to a DataFrame
    host_counts_df = top_20_hosts.reset_index()
    host_counts_df.columns = ['Host Name', 'Listing Count']

    # Sort the DataFrame by listing count (not necessary since the counts are already sorted)
    # host_counts_df = host_counts_df.sort_values(by='Listing Count', ascending=False)

    # Create a bar chart using Plotly
    fig = px.bar(host_counts_df, x='Host Name', y='Listing Count', title='Top 20 Hosts with Entire Home/Apartments Listings')
    fig.update_layout(xaxis_title='Host Name', yaxis_title='Number of Listings')
    fig.show()

elif question == "7. A list of the top 20 hosts with most Private Rooms":


        #to get data from momgoDB

    #import mongoClient parameter to take values
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)

    airbon_list = []
    db = client["airbnb_database"]
    collection_1 = db['listings']
    for airbon_data in collection_1.find():                   #"{}" is used all channel details mongo db
        airbon_list.append(airbon_data)
    df1 = pd.DataFrame(airbon_list)

    # Assuming your Airbnb dataset is stored in a DataFrame called 'airbnb_df'

    # Filter the data to include only private rooms
    private_room_df = df1[df1['room_type'] == 'Private room']

    # Group the data by host name and count the number of private rooms for each host
    host_private_room_count = private_room_df['host_name'].value_counts().reset_index()
    host_private_room_count.columns = ['Host Name', 'Private Room Count']

    # Select the top 20 hosts with the most private rooms
    top_20_hosts = host_private_room_count.head(20)

    # Plot the bar chart
    fig = px.bar(top_20_hosts, x='Host Name', y='Private Room Count',  
                title='Top 20 Hosts with Most Private Rooms',
                labels={'Host Name': 'Host Name', 'Private Room Count': 'Private Room Count'})

    fig.show()

elif question == "8. A list of the neighborhood prices map":

        #to get data from momgoDB

    #import mongoClient parameter to take values
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)

    airbon_list = []
    db = client["airbnb_database"]
    collection_1 = db['listings']
    for airbon_data in collection_1.find():                   #"{}" is used all channel details mongo db
        airbon_list.append(airbon_data)
    df1 = pd.DataFrame(airbon_list)

    #A list of the neighborhood average prices map

    # Assuming your DataFrame is named 'airbnb_data'

    # Group the data by neighbourhood and calculate the average price for each neighbourhood
    neighborhood_prices = df1.groupby('neighbourhood').agg({'latitude':'mean', 'longitude':'mean', 'price':'mean', 'name':'first', 'host_name':'first'}).reset_index()

    # Create a map centered around London
    london_map = folium.Map(location=[51.5074, -0.1278], zoom_start=10)

    # Add markers for each neighborhood with the average price
    for index, row in neighborhood_prices.iterrows():
        popup_content = f"Neighborhood: {row['neighbourhood']}<br>Average Price: {row['price']}<br>Name: {row['name']}<br>Host Name: {row['host_name']}"
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup_content,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(london_map)

    # Display the map
    london_map
'''
import pymongo
import pandas as pd
import plotly.express as px
import folium
import streamlit as st
from streamlit_folium import st_folium


with st.sidebar:
    st.title(":orange[Airbnb Analysis]")
    st.header("Notes")
    st.caption("The all data get from airbnb website")

question = st.selectbox("select your question",("1. Missing values in price column",
                                                "2. A list of the Availability of room type",
                                                "3. A list of the Occupation on each year",
                                                "4. A list of the short-Term rental",
                                                "5. A list of the top host Listings Count",
                                                "6. A list of the top 20 host with Entire Home/Apartments Listings",
                                                "7. A list of the top 20 hosts with most Private Rooms",
                                                "8. A list of the neighborhood average prices map"))

# Create MongoDB client
client = pymongo.MongoClient('localhost', 27017)
db = client["airbnb_database"]
collection_1 = db['listings']
airbnb_listings = list(collection_1.find())
df1 = pd.DataFrame(airbnb_listings)

if question == "1. Missing values in price column":
    # Define price ranges or bins
    price_bins = [0, 50, 100, 150, 200, 250, 300, float('inf')]
    price_labels = ['missing data (%)', '50-100', '100-150', '150-200', '200-250', '250-300', '300+']
    # Categorize prices into bins
    df1['price_range'] = pd.cut(df1['price'], bins=price_bins, labels=price_labels)
    # Count the number of listings in each price range
    price_distribution = df1['price_range'].value_counts()
    # Plot pie chart
    fig = px.pie(price_distribution, names=price_distribution.index, title='Distribution of Prices')
    st.plotly_chart(fig)

elif question == "2. A list of the Availability of room type":
    # Create a new DataFrame with the desired columns
    df_room_type = df1[['room_type', 'availability_365']]
    # Group by room type and sum the availability
    df_sum = df_room_type.groupby('room_type')['availability_365'].agg(['sum', 'count']).reset_index()
    # Calculate the percentage availability for each room type
    df_sum['availability_percentage'] = (df_sum['sum'] / df_sum['sum'].sum()) * 100
    # Sort the DataFrame in descending order based on total availability
    df_sum = df_sum.sort_values(by='sum', ascending=False)
    # Create a bar chart
    fig = px.bar(df_sum, x='room_type', y='sum', color='room_type',
                 title='Availability of Room Types',
                 text=df_sum.apply(lambda row: f"{row['count']} - {row['availability_percentage']:.2f}%", axis=1))
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig)

elif question == "3. A list of the Occupation on each year":
    # Create a new DataFrame with the desired columns
    df_activity = df1[['id', 'minimum_nights', 'price', 'number_of_reviews', 'last_review']]
    df_activity['last_review'] = pd.to_datetime(df_activity['last_review'])
    df_activity['year'] = df_activity['last_review'].dt.year
    df_activity['occupation'] = df_activity['minimum_nights'] * df_activity['number_of_reviews']
    yearly_occupation = df_activity.groupby('year')['occupation'].sum().reset_index()
    yearly_occupation = yearly_occupation.sort_values(by='year', ascending=False)
    # Create a bar chart
    fig = px.bar(yearly_occupation, x='year', y='occupation', labels={'year': 'Year', 'occupation': 'Occupation'},
                 title='Occupation for Each Year')
    fig.update_layout(xaxis=dict(title='Year', type='category'), yaxis=dict(title='Occupation'))
    st.plotly_chart(fig)

elif question == "4. A list of the short-Term rental":
    # Filter the DataFrame to include only short-term rentals
    short_term_rentals = df1[df1['minimum_nights'] <= 30]
    # Create a histogram
    fig = px.histogram(short_term_rentals, x='minimum_nights', title="Distribution of Minimum Nights for Short-Term Rentals",
                       color_discrete_sequence=px.colors.qualitative.Dark24)
    fig.update_layout(xaxis_title="Minimum Nights", yaxis_title="Count")
    fig.update_traces(text=short_term_rentals.groupby('minimum_nights').size().values, textposition='outside')
    st.plotly_chart(fig)

elif question == "5. A list of the top host Listings Count":
    top_hosts_df = df1[['host_id', 'host_name', 'calculated_host_listings_count']]
    top_hosts_df_sorted = top_hosts_df.sort_values(by='calculated_host_listings_count', ascending=False)
    top_hosts_df_sorted.drop_duplicates(inplace=True)
    top_20_hosts = top_hosts_df_sorted.head(20)
    fig = px.bar(top_20_hosts, x='host_name', y='calculated_host_listings_count',
                 title='Top 20 Hosts by Calculated Host Listings Count',
                 labels={'host_name': 'Host Name', 'calculated_host_listings_count': 'Listings Count'})
    st.plotly_chart(fig)

elif question == "6. A list of the top 20 host with Entire Home/Apartments Listings":
    entire_home_df = df1[df1['room_type'] == 'Entire home/apt']
    host_counts = entire_home_df['host_name'].value_counts()
    top_20_hosts = host_counts.head(20).reset_index()
    top_20_hosts.columns = ['Host Name', 'Listing Count']
    fig = px.bar(top_20_hosts, x='Host Name', y='Listing Count',
                 title='Top 20 Hosts with Entire Home/Apartments Listings')
    fig.update_layout(xaxis_title='Host Name', yaxis_title='Number of Listings')
    st.plotly_chart(fig)

elif question == "7. A list of the top 20 hosts with most Private Rooms":
    private_room_df = df1[df1['room_type'] == 'Private room']
    host_private_room_count = private_room_df['host_name'].value_counts().reset_index()
    host_private_room_count.columns = ['Host Name', 'Private Room Count']
    top_20_hosts = host_private_room_count.head(20)
    fig = px.bar(top_20_hosts, x='Host Name', y='Private Room Count',
                 title='Top 20 Hosts with Most Private Rooms',
                 labels={'Host Name': 'Host Name', 'Private Room Count': 'Private Room Count'})
    st.plotly_chart(fig)

elif question == "8. A list of the neighborhood average prices map":
    # Group the data by neighbourhood and calculate the average price for each neighbourhood
    neighborhood_prices = df1.groupby('neighbourhood').agg({'latitude':'mean', 'longitude':'mean', 'price':'mean', 'name':'first', 'host_name':'first'}).reset_index()
    # Create a map centered around London
    london_map = folium.Map(location=[51.5074, -0.1278], zoom_start=10)
    # Add markers for each neighborhood with the average price
    for index, row in neighborhood_prices.iterrows():
        popup_content = f"Neighborhood: {row['neighbourhood']}<br>Average Price: {row['price']}<br>Name: {row['name']}<br>Host Name: {row['host_name']}"
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup_content,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(london_map)
    # Display the map using st_folium
    st_folium(london_map)

