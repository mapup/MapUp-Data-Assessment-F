#!/usr/bin/env python
# coding: utf-8

# # Importing Basic Libraries

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt


# ### Loading the dataset

# In[45]:


df=pd.read_csv('dataset-1.csv')
df


# In[3]:


df.isna().sum()  # checking for null values


# In[4]:


sb.heatmap(df.isnull())
plt.show()  # checking for null values through heatmap


# In[5]:


df.dtypes # checking for data types


# ## Question 1: Car Matrix Generation

# In[6]:


def generate_car_matrix(data):
    new_data = df.pivot(index='id_1',columns='id_2',values='car')
    #print(new_data)
    
    # there is nan values so filling nan we are replacing it with zero
    new_data = new_data.fillna(0)
    #print(new_data)
    
    # filling the diagonal values to 0
    for i in new_data.index:
        new_data.at[i,i] = 0
    return new_data
    
generate_car_matrix(df)


# ## Question 2: Car Type Count Calculation

# In[9]:


def get_type_count(data):
    new = [(df['car'] <= 15),(df['car'] >15) & (df['car']<=25), (df['car']>25)]
    value = ['low','medium','high']
    df['car_type'] = np.select(new,value) # adding values
    
    new_type = df['car_type'].value_counts().to_dict() # framing the new dataset in dictionary type
    
    car_type = {x :new_type[x] for x in sorted(new_type)} # sorting it in list comprehension method
    
    return car_type
 
get_type_count(df)


# ## Question 3: Bus Count Index Retrieval

# In[10]:


def get_bus_indexes(data):
    mean = data['bus'].mean()  # print(mean) # for finding the respective mean values
    
    indices = data[data['bus']>2 * mean].index.tolist() # storing in indicies variable where bus column are greater then 2
    #print(indices)
    
    indices.sort() # sorting in ascending order
    
    return indices
    
bus_count =get_bus_indexes(df)
print('Bus values which are greater then 2 are:',bus_count) # printing in list method


# In[ ]:





# ## Question 4: Route Filtering

# In[46]:


def filter_routes(data):
   
    route_means = data.groupby('route')['truck'].mean()  # Group by 'route' and calculate the mean of 'truck' values
   
    filtered_routes = route_means[route_means > 7].index.tolist()     # Filter routes where the average 'truck' value is greater than 7
    
    sorted_filtered_routes = sorted(filtered_routes)   # Sort the list of routes
    return sorted_filtered_routes


filter_routes(df)                   # Apply the function to the dataframe
#print(sorted_routes)               # Display the sorted list of routes


# In[ ]:





# ## Question 5: Matrix Value Modification

# In[15]:


generate_car_matrix(df).to_csv('nw.csv',index=False,encoding='utf-8')
# storing the dataset from question 1 in csv file 


# In[16]:


new= pd.read_csv('nw.csv')
new


# In[17]:


def multiply_matrix(data):
    copied_data = data.copy() # storing the orginal dataset into another variable 

    copied_data = copied_data.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    copied_data = copied_data.round(1)   # Round the values to 1 decimal place 

    return copied_data

dataframe = multiply_matrix(new)
dataframe


# ## Question 6: Time Check

# In[ ]:


You are given a dataset, dataset-2.csv, containing columns id, id_2, and timestamp
(startDay, startTime, endDay, endTime). 
The goal is to verify the completeness of the time data by checking whether 
the timestamps for each unique (id, id_2) pair cover a full 24-hour period 
(from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week 
(from Monday to Sunday).

Create a function that accepts dataset-2.csv as a DataFrame and returns a boolean
series that indicates if each (id, id_2) pair has incorrect timestamps.
The boolean series must have multi-index (id, id_2).


# In[18]:


time_check = pd.read_csv('dataset-2.csv')
time_check   #loading the dataset


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




