#!/usr/bin/env python
# coding: utf-8

# Question 1: Distance Matrix Calculation

# In[3]:


import pandas as pd
import networkx as nx
df=pd.read_csv("dataset-3.csv")

def calculate_distance_matrix(df) -> pd.DataFrame:
    G = nx.Graph()
    for index, row in df.iterrows():
        G.add_edge(row['id_start'], row['id_end'], weight=row['distance'])
    toll_locations = list(set(df['id_start'].tolist() + df['id_end'].tolist()))
    distance_matrix = pd.DataFrame(index=toll_locations, columns=toll_locations)
    for i in toll_locations:
        for j in toll_locations:
            if i == j:
                distance_matrix.loc[i, j] = 0
            elif not pd.isna(distance_matrix.loc[i, j]):
                continue
            else:
                try:
                    distance = nx.shortest_path_length(G, i, j, weight='weight')
                    distance_matrix.loc[i, j] = distance
                    distance_matrix.loc[j, i] = distance
                except nx.NetworkXNoPath:
                    distance_matrix.loc[i, j] = float('nan')
                    distance_matrix.loc[j, i] = float('nan')

    return distance_matrix

resulting_distance_matrix = calculate_distance_matrix(df)
print(resulting_distance_matrix)


# Question 2: Unroll Distance Matrix

# In[24]:


def unroll_distance_matrix(df)->pd.DataFrame():
    unrolled_data = []
    for index, row in df.iterrows():
        id_start = index
        for id_end, distance in row.items():
            if id_start != id_end:
                unrolled_data.append([id_start, id_end, distance])
    unrolled_df = pd.DataFrame(unrolled_data, columns=['id_start', 'id_end', 'distance'])
    return unrolled_df


unrolled_result = unroll_distance_matrix(resulting_distance_matrix) #input from 1st question
print(unrolled_result)


# Question 3: Finding IDs within Percentage Threshold

# In[28]:


def find_ids_within_ten_percentage_threshold(df, reference_id):
    reference_rows = unrolled_result[unrolled_result['id_start'] == reference_value]
    reference_avg_distance = reference_rows['distance'].mean()
    threshold_lower = reference_avg_distance - 0.1 * reference_avg_distance
    threshold_upper = reference_avg_distance + 0.1 * reference_avg_distance
    within_threshold_ids = unrolled_result[(unrolled_result['distance'] >= threshold_lower) & (unrolled_result['distance'] <= threshold_upper)]['id_start']
    result_ids_within_threshold = within_threshold_ids.sort_values().tolist()
    return result_ids_within_threshold

reference_value = 1001472
result_ids_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_result, reference_value)
print(result_ids_within_threshold)


# Question 4: Calculate Toll Rate

# In[30]:


def calculate_toll_rate(df)->pd.DataFrame():
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        unrolled_result[vehicle_type] = unrolled_result['distance'] * rate_coefficient
    return unrolled_result

result_with_toll_rates = calculate_toll_rate(unrolled_result)
print(result_with_toll_rates)


# Question 5: Calculate Time-Based Toll Rates

# In[55]:


from datetime import datetime, time

def calculate_time_based_toll_rates(result_ids_within_threshold):
    time_ranges = [(time(0, 0), time(10, 0), 0.8), (time(10, 0), time(18, 0), 1.2), (time(18, 0), time(23, 59, 59), 0.8)]
    weekend_discount_factor = 0.7
    data = []
    for pair in result_ids_within_threshold:
        for day in range(7):
                data.append([
                    pair, 
                    pair,
                    datetime.strptime(str(day), '%w').strftime('%A'),  
                    start_time,  
                    datetime.strptime(str((day + 1) % 7), '%w').strftime('%A'), 
                    end_time, 
                    0.8 * discount_factor,  
                    1.2 * discount_factor,  
                    1.5 * discount_factor,  
                    2.2 * discount_factor,  
                    3.6 * discount_factor   
                ])

    columns = ['id_start', 'id_end', 'start_day', 'start_time', 'end_day', 'end_time', 'moto', 'car', 'rv', 'bus', 'truck']
    time_based_rates_df = pd.DataFrame(data, columns=columns)
    return time_based_rates_df

result_with_time_based_rates = calculate_time_based_toll_rates(result_ids_within_threshold)
print(result_with_time_based_rates)


# In[ ]:




