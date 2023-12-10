#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd


# ## Question 1: Distance Matrix Calculation

# In[10]:


df=pd.read_csv('dataset-3.csv')
df.head()


# In[36]:


def calculate_distance_matrix(d):
    
    pivot_df = d.pivot(index='id_start', columns='id_end', values='distance').fillna(0) # Create a pivot table to calculate the cumulative distances
    
    distance_matrix = pivot_df.add(pivot_df.T, fill_value=0)      # Add the transposed pivot table to itself to get the symmetric matrix

    distance_matrix.values[[range(distance_matrix.shape[0])]*2] = 0   # Set the diagonal values to 0
    
    return distance_matrix

dataset_df = pd.read_csv('dataset-3.csv')

distance_matrix = calculate_distance_matrix(dataset_df) # Apply the function to the dataset
distance_matrix.head()


# ## Question 2: Unroll Distance Matrix

# In[21]:


def unroll_distance_matrix(distance_df):
   
    distance_long_df = distance_df.stack().reset_index()   # Unroll the distance matrix into a long format DataFrame
    distance_long_df.columns = ['id_start', 'id_end', 'distance']
    
    distance_long_df = distance_long_df[distance_long_df['id_start'] != distance_long_df['id_end']]     # Remove rows where id_start is equal to id_end

    return distance_long_df

unrolled_distance_df = unroll_distance_matrix(resulting_distance_matrix)

unrolled_distance_df.head() # Display the head of the unrolled distance DataFrame


# In[ ]:





# ## Question 3: Finding IDs within Percentage Threshold

# In[22]:


def find_ids_within_ten_percentage_threshold(df, reference_id):
    
    avg_distance = df[df['id_start'] == reference_id]['distance'].mean() # Calculate the average distance for the reference ID
   
    threshold = 0.1 * avg_distance   # Calculate the 10% threshold

   
    ids_within_threshold = df[(df['distance'] >= avg_distance - threshold) &
                             (df['distance'] <= avg_distance + threshold)]['id_start'].unique()   # Find IDs within the 10% threshold of the reference ID's average distance
   
    ids_within_threshold.sort()
    return ids_within_threshold.tolist()


reference_id = 1001400
ids_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_distance_df, reference_id)
ids_within_threshold


# In[ ]:





# ## Question 4: Calculate Toll Rate

# In[23]:


unrolled_distance_df.to_csv('new.csv',index=False,encoding='utf-8')
# storing the dataset from question 1 in csv file 


# In[25]:


new= pd.read_csv('new.csv')
new


# In[27]:


def calculate_toll_rate(df):
    
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }  # Define rate coefficients for each vehicle type 
   
    for vehicle, rate in rate_coefficients.items():  # Calculate toll rates for each vehicle type
        df[vehicle] = df['distance'] * rate
    
    return df

result_df = calculate_toll_rate(df)
result_df.head()


# In[ ]:





# ## Question 5: Calculate Time-Based Toll Rates

# In[29]:


result_df.to_csv('news.csv',index=False,encoding='utf-8')
# storing the dataset from question 1 in csv file 


# In[30]:


news=pd.read_csv('news.csv')
news


# In[34]:


from datetime import time
import numpy as np
from tqdm import tqdm

tqdm.pandas()

def calculate_time_based_toll_rates(df):
    discount_weekday = {time(0,0): 0.8, time(10,0): 1.2, time(18,0): 0.8}     # Define the discount factors

    discount_weekend = 0.7

    time_ranges = [(time(0,0), time(9,59,59)), (time(10,0), time(17,59,59)), (time(18,0), time(23,59,59))] # Define the time ranges

    for day in ['start_day', 'end_day']:
        df[day] = np.nan
    for t in ['start_time', 'end_time']:
        df[t] = np.nan

    for index, row in df.iterrows():     # Apply the discount factors based on the time ranges

        for start_time, end_time in time_ranges:
            
            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']: # Weekdays
                df.at[index, 'start_day'] = day
                df.at[index, 'end_day'] = day
                df.at[index, 'start_time'] = start_time
                df.at[index, 'end_time'] = end_time
                for vehicle in ['moto', 'car', 'rv', 'bus', 'truck']:
                    df.at[index, vehicle] *= discount_weekday.get(start_time, 1)
                    
            for day in ['Saturday', 'Sunday']:             # Weekends
                df.at[index, 'start_day'] = day
                df.at[index, 'end_day'] = day
                df.at[index, 'start_time'] = start_time
                df.at[index, 'end_time'] = end_time
                for vehicle in ['moto', 'car', 'rv', 'bus', 'truck']:
                    df.at[index, vehicle] *= discount_weekend

    return df

result_df = calculate_time_based_toll_rates(df)
result_df.head()


# In[ ]:




