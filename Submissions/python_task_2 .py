#!/usr/bin/env python
# coding: utf-8

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
    def calculate_distance_matrix(csv_file):
    # Read the CSV file into a DataFrame
    data = pd.read_csv(csv_file)
    
    # Create an empty dictionary to store distances
    distances = {}
    
    # Iterate through the data to calculate cumulative distances
    for _, row in data.iterrows():
        source = row['Source']
        destination = row['Destination']
        distance = row['Distance']
        
        # Adding distances bidirectionally
        if source not in distances:
            distances[source] = {}
        distances[source][destination] = distance
        
        if destination not in distances:
            distances[destination] = {}
        distances[destination][source] = distance
    
    # Create a DataFrame with cumulative distances
    distance_matrix = pd.DataFrame(distances).fillna(0)
    
    # Calculate cumulative distances along known routes
    for col in distance_matrix.columns:
        for idx in distance_matrix.index:
            if idx != col and distance_matrix.at[idx, col] == 0:
                for intermediate in distance_matrix.index:
                    if intermediate != idx and intermediate != col:
                        if distance_matrix.at[idx, intermediate] != 0 and distance_matrix.at[intermediate, col] != 0:
                            distance_matrix.at[idx, col] = distance_matrix.at[idx, intermediate] + distance_matrix.at[intermediate, col]
                            break
    
    # Set diagonal values to 0
    for i in range(len(distance_matrix)):
        distance_matrix.iat[i, i] = 0
    
    return distance_matrix

# Usage example:
resulting_distance_matrix = calculate_distance_matrix('dataset-3.csv')



def unroll_distance_matrix(df):
    """
    Unroll a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled distance matrix
    """
    def unroll_distance_matrix(distance_matrix):
    # Extract unique IDs from the index/columns of the distance matrix
    ids = distance_matrix.index.tolist()
    
    # Initialize lists to store the unrolled data
    id_start = []
    id_end = []
    distance = []
    
    # Iterate through the distance matrix to get combinations and distances
    for start_id in ids:
        for end_id in ids:
            if start_id != end_id:
                id_start.append(start_id)
                id_end.append(end_id)
                distance.append(distance_matrix.loc[start_id, end_id])
    
    # Create a DataFrame with the unrolled data
    unrolled_data = pd.DataFrame({
        'id_start': id_start,
        'id_end': id_end,
        'distance': distance
    })
    
    return unrolled_data

# Example usage:
# Assuming resulting_distance_matrix is the DataFrame obtained from the previous step
unrolled_distances = unroll_distance_matrix(resulting_distance_matrix)
print(unrolled_distances)



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
    def find_ids_within_ten_percentage_threshold(df, reference_value):
    # Filter the DataFrame based on the reference value in id_start column
    reference_df = df[df['id_start'] == reference_value]
    
    # Calculate the average distance for the reference value
    avg_distance = reference_df['distance'].mean()
    
    # Calculate the threshold values within 10% of the average distance
    lower_threshold = avg_distance - (avg_distance * 0.1)
    upper_threshold = avg_distance + (avg_distance * 0.1)
    
    # Filter the DataFrame to find values within the threshold
    within_threshold = df[(df['id_start'] != reference_value) & 
                          (df['distance'] >= lower_threshold) &
                          (df['distance'] <= upper_threshold)]
    
    # Get unique values from id_start column within the threshold
    unique_ids_within_threshold = sorted(within_threshold['id_start'].unique())
    
    return unique_ids_within_threshold


reference_value = 10100  # Replace this with your desired reference value
result = find_ids_within_ten_percentage_threshold(unrolled_distances, reference_value)
print(result)




def calculate_toll_rate(df):
    
     """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Define rate coefficients for different vehicle types
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    
    # Calculate toll rates for each vehicle type
    for vehicle, coefficient in rate_coefficients.items():
        df[vehicle] = df['distance'] * coefficient
    
    return df


# Assuming unrolled_distances is the DataFrame obtained from the previous step
resulting_dataframe_with_toll_rates = calculate_toll_rate(unrolled_distances)
print(resulting_dataframe_with_toll_rates)




def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

    return df