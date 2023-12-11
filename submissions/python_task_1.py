#!/usr/bin/env python
# coding: utf-8

# Question 1: Car Matrix Generation

# In[12]:


import pandas as pd
df=pd.read_csv("dataset-1.csv")

def generate_car_matrix(df)->pd.DataFrame:
    matrix=df.pivot(index='id_1',columns='id_2',values='car')
    matrix=matrix.fillna(0)
    for index in matrix.index:
        matrix.at[index,index]=0
    return matrix

result_matrix = generate_car_matrix(df)
print(result_matrix)


# Question 2: Car Type Count Calculation

# In[13]:


def get_type_count(df)->dict:
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],labels=choices, right=False)
    car_type_counts = df['car_type'].value_counts()
    car_type_counts_dict = car_type_counts.to_dict()
    sorted_car_type_counts = dict(sorted(car_type_counts_dict.items()))
    return sorted_car_type_counts

result_counts = get_type_count(df)
print(result_counts)


# Question 3: Bus Count Index Retrieval

# In[15]:


def get_bus_indexes(df)->list:
    
    mean_bus_value = df['bus'].mean()
    bus_condition = df['bus'] > 2 * mean_bus_value
    bus_indexes = df[bus_condition].index.tolist()
    bus_indexes.sort()
    return bus_indexes

result_indexes = get_bus_indexes(df)
print(result_indexes)


# Question 4: Route Filtering

# In[16]:


def filter_routes(df):
    average_truck_value = df['truck'].mean()
    selected_routes = df[df['truck'] > 7]['route']
    sorted_routes = sorted(selected_routes.unique().tolist())
    return sorted_routes


result_routes = filter_routes(df)
print(result_routes)


# Question 5: Matrix Value Modification

# In[17]:


def multiply_matrix(matrix)->pd.DataFrame:
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_matrix = modified_matrix.round(1)
    return modified_matrix


modified_matrix_result = multiply_matrix(result_matrix)
print(modified_matrix_result)


# Question 6: Time Check

# In[20]:


import pandas as pd
from datetime import timedelta

df = pd.read_csv("dataset-2.csv")

def verify_timestamps(df):
    valid_rows = pd.DataFrame()
    for index, row in df.iterrows():
        try:
            if (
                len(row['startDay']) >= 10 and
                len(row['startTime']) >= 8 and
                len(row['endDay']) >= 10 and
                len(row['endTime']) >= 8
            ):
                start_timestamp = pd.to_datetime(row['startDay'] + ' ' + row['startTime'])
                end_timestamp = pd.to_datetime(row['endDay'] + ' ' + row['endTime'])
                valid_rows = valid_rows.append(row)
            else:
                print(f"Skipped row {index} due to invalid timestamp values: {row}")
        except pd.errors.OutOfBoundsDatetime as e:
            print(f"Skipped row {index} due to error: {e}")

    is_valid = (
        (valid_rows['duration'] == timedelta(days=1)) &  
        (valid_rows['start_timestamp'].dt.dayofweek == 0) &  
        (valid_rows['end_timestamp'].dt.dayofweek == 6) 
    )
    result_series = is_valid.groupby(['id', 'id_2']).all()
    return result_series

verification_result = verify_timestamps(df)
print(verification_result)


# In[ ]:





# In[ ]:




