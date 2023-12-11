#!/usr/bin/env python
# coding: utf-8

# #### ##### Distance Matrix Calculation
# Create a function named calculate_distance_matrix that takes the dataset-3.csv as input and generates a DataFrame representing distances between IDs.
# 
# The resulting DataFrame should have cumulative distances along known routes, with diagonal values set to 0. If distances between toll locations A to B and B to C are known, then the distance from A to C should be the sum of these distances. Ensure the matrix is symmetric, accounting for bidirectional distances between toll locations (i.e. A to B is equal to B to A).

# In[1]:


import pandas as pd
import numpy as np
df = pd.read_csv("dataset-3.csv", index_col=0)
df.head()


# In[2]:


''' def calculate_distance_matrix(df):

    df.fillna(0, inplace=True)
    df = df.astype(float)
    df = df + df.T
    np.fill_diagonal(df.values, 0)
    return df

calculate_distance_matrix(df2)'''


# In[5]:


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    distance_matrix =  df.pivot(index="id_start", columns="id_end", values="distance").fillna(0)
    distance_matrix = distance_matrix + distance_matrix.T
    return distance_matrix

calculate_distance_matrix(df)


# #### Unroll Distance Matrix
# 
# Create a function unroll_distance_matrix that takes the DataFrame created in Question 1. The resulting DataFrame should have three columns: columns id_start, id_end, and distance.
# 
# All the combinations except for same id_start to id_end must be present in the rows with their distance values from the input DataFrame.

# In[7]:


def unroll_distance_matrix(df):
    """
    Unroll a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled distance matrix
    """
    df = df.stack().reset_index()
    df.columns = ['id_start', 'id_end', 'distance']
    df = df[df['id_start'] != df['id_end']]
    return df

unroll_distance_matrix(df)


# #### Finding IDs within Percentage Threshold
# 
# Create a function find_ids_within_ten_percentage_threshold that takes the DataFrame created in Question 2 and a reference value from the id_start column as an integer.
# 
# Calculate average distance for the reference value given as an input and return a sorted list of values from id_start column which lie within 10% (including ceiling and floor) of the reference value's average.

# In[ ]:


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here

    return df


# In[ ]:




