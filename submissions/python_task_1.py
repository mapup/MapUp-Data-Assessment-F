#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
df = pd.read_csv("dataset-1.csv")
df.head(20)


# # Question 1: Car Matrix Generation
# ## Under the function named generate_car_matrix write a logic that takes the dataset-1.csv as a DataFrame. Return a new DataFrame that follows the following rules:
# 
# * values from id_2 as columns
# * values from id_1 as index
# * dataframe should have values from car column
# * diagonal values should be 0.

# In[2]:


import pandas as pd

def generate_car_matrix(data):
    # Create a new DataFrame with id_2 as columns and id_1 as index
    car_matrix = pd.pivot_table(data, values='car', index='id_1', columns='id_2', fill_value=0)

    # Set diagonal values to 0
    for i in car_matrix.index:
        if i in car_matrix.columns:
            car_matrix.at[i, i] = 0

    return car_matrix

# Load the CSV file into a DataFrame
data = pd.read_csv(r"C:\Users\abhi1\OneDrive\Desktop\MapUp-Data-Assessment-F\datasets\dataset-1.csv")

# Generate the car matrix using the function
car_matrix = generate_car_matrix(data)

# Display the resulting DataFrame
print(car_matrix)


# # Question 2: Car Type Count Calculation
# ## Create a Python function named get_type_count that takes the dataset-1.csv as a DataFrame. Add a new categorical column car_type based on values of the column car:
# 
# * low for values less than or equal to 15,
# * medium for values greater than 15 and less than or equal to 25,
# * high for values greater than 25.
# * Calculate the count of occurrences for each car_type category and return the result as a dictionary. Sort the dictionary alphabetically based on keys.

# In[3]:


def get_type_count(df):
    # Add a new categorical column 'car_type'
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    # Calculate the count of occurrences for each 'car_type' category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts

# Load the CSV file into a DataFrame
df = pd.read_csv("dataset-1.csv")

# Call the function and print the result
result = get_type_count(df)
print(result)


# # Question 3: Bus Count Index Retrieval
# ## Create a Python function named get_bus_indexes that takes the dataset-1.csv as a DataFrame. The function should identify and return the indices as a list (sorted in ascending order) where the bus values are greater than twice the mean value of the bus column in the DataFrame.

# In[4]:


def get_bus_indexes(df):
    # Calculate the mean value of the 'bus' column
    mean_bus = df['bus'].mean()
    
    # Filter rows where the 'bus' values are greater than twice the mean value
    filtered_rows = df[df['bus'] > 2 * mean_bus]
    
    # Get the indices of the filtered rows and return as a sorted list
    result = sorted(filtered_rows.index.tolist())
    
    return result

# Load the dataset
df = pd.read_csv('dataset-1.csv')

# Call the function and print the result
bus_indexes = get_bus_indexes(df)
print("Indices where bus values are greater than twice the mean:", bus_indexes)


# # Question 4: Route Filtering
# ## Create a python function filter_routes that takes the dataset-1.csv as a DataFrame. The function should return the sorted list of values of column route for which the average of values of truck column is greater than 7.

# In[5]:


def filter_routes(data):
    # Calculate the average of the "truck" column for each unique value in the "route" column
    avg_truck_per_route = data.groupby('route')['truck'].mean()
    
    # Filter routes where the average truck value is greater than 7
    filtered_routes = avg_truck_per_route[avg_truck_per_route > 7].index.tolist()
    
    # Sort the list of routes
    filtered_routes.sort()
    
    return filtered_routes

# Assuming df is your DataFrame
df = pd.read_csv('dataset-1.csv')
result = filter_routes(df)
print(result)


# # Question 5: Matrix Value Modification
# ## Create a Python function named multiply_matrix that takes the resulting DataFrame from Question 1, as input and modifies each value according to the following logic:
# 
# * If a value in the DataFrame is greater than 20, multiply those values by 0.75,
# * If a value is 20 or less, multiply those values by 1.25.
# * The function should return the modified DataFrame which has values rounded to 1 decimal place.

# In[8]:


def multiply_matrix(dataframe):
    # Copy the input DataFrame to avoid modifying the original
    result_df = dataframe.copy()

    # Apply the specified logic to each value in the DataFrame
    for col in result_df.columns:
        result_df[col] = result_df[col].apply(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the values to 1 decimal place
    result_df = result_df.round(1)

    return result_df

# Read the CSV file into a DataFrame
file_path = "dataset-1.csv"
df = pd.read_csv(file_path)

# Call the function and print the result
result = multiply_matrix(df)
print(result)


# In[9]:


result.head()


# # Question 6: Time Check
# ## You are given a dataset, dataset-2.csv, containing columns id, id_2, and timestamp (startDay, startTime, endDay, endTime). The goal is to verify the completeness of the time data by checking whether the timestamps for each unique (id, id_2) pair cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).
# 
# * Create a function that accepts dataset-2.csv as a DataFrame and returns a boolean series that indicates if each (id, id_2) pair has incorrect timestamps. The boolean series must have multi-index (id, id_2).

# In[10]:


import pandas as pd
from datetime import timedelta

def check_timestamp_completeness(df):
    # Combine 'startDay' and 'startTime' columns to create a 'start_timestamp' column
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format="%A %H:%M:%S")
    
    # Combine 'endDay' and 'endTime' columns to create an 'end_timestamp' column
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format="%A %H:%M:%S")
    
    # Create a mask for rows with incorrect timestamps
    mask = (
        (df['start_timestamp'] != df['start_timestamp'].apply(lambda x: x.floor('D'))) |
        (df['end_timestamp'] != df['end_timestamp'].apply(lambda x: x.ceil('D') - timedelta(microseconds=1)))
    )
    
    # Group by 'id' and 'id_2' and check if any row in the group has incorrect timestamps
    result = df[mask].groupby(['id', 'id_2']).any().any(axis=1)
    
    return result

# Load the dataset into a DataFrame
df = pd.read_csv('dataset-2.csv')

# Call the function with the DataFrame
result = check_timestamp_completeness(df)

# Print the result
print(result)

