#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df = pd.read_csv("dataset-1.csv")
df.head()


# In[3]:


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    car_matrix =  df.pivot(index="id_1", columns="id_2", values="car").fillna(0)

    return car_matrix

generate_car_matrix(df)


# #### Car Type Count Calculation
# Create a Python function named get_type_count that takes the dataset-1.csv as a DataFrame. Add a new categorical column car_type based on values of the column car:
# 
# low for values less than or equal to 15,
# medium for values greater than 15 and less than or equal to 25,
# high for values greater than 25.
# Calculate the count of occurrences for each car_type category and return the result as a dictionary. Sort the dictionary alphabetically based on keys.

# In[4]:


df.head()


# In[5]:


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    labels = ['low','medium','high']

    df['car_type'] = pd.cut(df['car'], bins=[0,15,25,float('inf')], labels=labels)
    count = df['car_type'].value_counts().to_dict()
    alphabetical_count = dict(sorted(count.items(),key = lambda item : item[0]))
    return alphabetical_count

get_type_count(df)


# ##### Bus Count Index Retrieval
# Create a Python function named get_bus_indexes that takes the dataset-1.csv as a DataFrame. The function should identify and return the indices as a list (sorted in ascending order) where the bus values are greater than twice the mean value of the bus column in the DataFrame.

# In[6]:


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    indices = df[df['bus']>(2*df['bus'].mean())].index
    sorted(indices.tolist())
    
    return indices

get_bus_indexes(df)


# #### Route Filtering
# Create a python function filter_routes that takes the dataset-1.csv as a DataFrame. The function should return the sorted list of values of column route for which the average of values of truck column is greater than 7.

# In[7]:


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    routes = df.groupby('route')['truck'].mean()
    sorted_list = routes[routes>7].index.tolist()
    

    return sorted_list

filter_routes(df)


# #### matrix value modification
# 
# Create a Python function named multiply_matrix that takes the resulting DataFrame from Question 1, as input and modifies each value according to the following logic:
# 
# If a value in the DataFrame is greater than 20, multiply those values by 0.75,
# If a value is 20 or less, multiply those values by 1.25.
# The function should return the modified DataFrame which has values rounded to 1 decimal place.

# In[8]:


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    # To apply the conditions to each element in the DataFrame, you'll need to use functions like applymap or nested loops to traverse through the DataFrame properly.
    matrix = generate_car_matrix(df)
    
    matrix = matrix.applymap(lambda x:x*0.75 if x>20 else x*1.25)
    return round(matrix)

multiply_matrix(df)


# #### Time Check
# You are given a dataset, dataset-2.csv, containing columns id, id_2, and timestamp (startDay, startTime, endDay, endTime). The goal is to verify the completeness of the time data by checking whether the timestamps for each unique (id, id_2) pair cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).
# 
# Create a function that accepts dataset-2.csv as a DataFrame and returns a boolean series that indicates if each (id, id_2) pair has incorrect timestamps. The boolean series must have multi-index (id, id_2).

# In[9]:


df1 = pd.read_csv("dataset-2.csv",parse_dates=['startTime','endTime'])
df1.head()


# In[10]:


a = (df1["endTime"]-df1["startTime"])
a


# In[11]:


df1.info()


# In[12]:


df1 = df1.drop_duplicates(subset=['id', 'id_2'])
df1.head()


# In[13]:


# Function to calculate time difference, check 24-hour coverage, and all days coverage
def calculate_time_difference(row):
    start_datetime = pd.to_datetime(row['startDay'] + ' ' + row['startTime'], format='%A %H:%M:%S')
    end_datetime = pd.to_datetime(row['endDay'] + ' ' + row['endTime'], format='%A %H:%M:%S')

    time_difference = end_datetime - start_datetime
    days_difference = time_difference.days
    hours_difference = time_difference.seconds // 3600

    # Check if it covers a full 24-hour period
    full_24_hours = time_difference >= pd.to_timedelta('23:59:59')

    # Check if it spans all 7 days of the week
    unique_days = {timestamp.day_name() for timestamp in [start_datetime, end_datetime]}
    all_days_coverage = len(unique_days) == 7

    return pd.Series([days_difference, hours_difference, full_24_hours, all_days_coverage], index=['Days', 'Hours', 'Full24Hours', 'AllDaysCoverage'])

# Apply the function to each row
result_df = df1.apply(calculate_time_difference, axis=1)

# Combine the results with the original DataFrame
result_df = pd.concat([df1, result_df], axis=1)
print(result_df)


# In[ ]:


get_ipython().system('pip list')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# 

# 

# In[ ]:





# #### Unroll Distance Matrix
# 
# Create a function unroll_distance_matrix that takes the DataFrame created in Question 1. The resulting DataFrame should have three columns: columns id_start, id_end, and distance.
# 
# All the combinations except for same id_start to id_end must be present in the rows with their distance values from the input DataFrame.

# In[ ]:





# 

# In[ ]:





# #### Calculate Toll Rate
# Create a function calculate_toll_rate that takes the DataFrame created in Question 2 as input and calculates toll rates based on vehicle types.
# 
# The resulting DataFrame should add 5 columns to the input DataFrame: moto, car, rv, bus, and truck with their respective rate coefficients. The toll rates should be calculated by multiplying the distance with the given rate coefficients for each vehicle type:
# 
# 0.8 for moto
# 1.2 for car
# 1.5 for rv
# 2.2 for bus
# 3.6 for truck

# In[ ]:





# #### Calculate Time-Based Toll Rates
# Create a function named calculate_time_based_toll_rates that takes the DataFrame created in Question 3 as input and calculates toll rates for different time intervals within a day.
# 
# The resulting DataFrame should have these five columns added to the input: start_day, start_time, end_day, and end_time.
# 
# start_day, end_day must be strings with day values (from Monday to Sunday in proper case)
# start_time and end_time must be of type datetime.time() with the values from time range given below.
# Modify the values of vehicle columns according to the following time ranges:
# 
# Weekdays (Monday - Friday):
# 
# From 00:00:00 to 10:00:00: Apply a discount factor of 0.8
# From 10:00:00 to 18:00:00: Apply a discount factor of 1.2
# From 18:00:00 to 23:59:59: Apply a discount factor of 0.8
# Weekends (Saturday and Sunday):
# 
# Apply a constant discount factor of 0.7 for all times.
# For each unique (id_start, id_end) pair, cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).

# In[ ]:




