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





df1 = pd.read_csv("dataset-2.csv",parse_dates=['startTime','endTime'])
df1.head()



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

