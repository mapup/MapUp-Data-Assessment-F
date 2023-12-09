import pandas as pd
import numpy as np
from datetime import datetime as dt
from itertools import product
import warnings
warnings.filterwarnings('ignore')
path = r'C:\Users\ritvi\OneDrive\Documents\GitHub\MapUp-Data-Assessment-F\datasets'
file1 = r'\dataset-1.csv'
file2 = r'\dataset-2.csv'

#Question 1 Car Generation Matrix

def generate_car_matrix(dataset):
    df = pd.read_csv(dataset)

    # Pivot the DataFrame to create a matrix
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # Set diagonal values to 0
    for col in car_matrix.columns.tolist():
        car_matrix.at[col, col] = 0

    return car_matrix

#Question 2 Car Type count calculation

def get_type_count(dataset):
    df=pd.read_csv(dataset)
    #Create the column car_type
    df['car_type']=df['car'].apply(lambda x:'low' if x<=15 else('medium' if 15<x<=25 else 'high'))
    # create a dictionary of value counts of each car type and sort it by alphabetical order
    final_dict=pd.DataFrame(df['car_type'].value_counts()).sort_index(axis=0).to_dict()['count']
    return final_dict
#Question 3 Bus Count Interval index

def get_bus_indexes(dataset):
    df=pd.read_csv(dataset)
    #Returning the list of indexes where bus value > 2* mean of the column
    final_list=df[df['bus']>(df['bus'].mean()*2)].sort_index(axis=0).index.tolist()
    return final_list

#Question 4 Route Filtering

def filter_routes(dataset):
    df=pd.read_csv(dataset)
    df1=df.groupby('route').agg({'truck':'mean'}).sort_index(axis=0)
    final_list=df1[df1['truck']>7].index.tolist()
    return final_list

#Question 5 Matrix value modifciation

def multiply_matrix(result):
    result1=result.applymap(lambda x: x*0.75 if x>20 else x*1.25)
    return result1

#Question 6 Time check

def time_check(dataset):
    df=pd.read_csv(dataset)
    df['startTime']=pd.to_datetime(df['startTime'],format='%H:%M:%S')
    df['endTime']=pd.to_datetime(df['endTime'],format='%H:%M:%S')
    df['incorrect_start_flag'] = np.where(
        (df['startTime'].dt.hour != 0) |
        (df['startTime'].dt.minute != 0) |
        (df['startTime'].dt.second != 0) |
        ~df['startDay'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),1,0
    )

    df['incorrect_end_flag'] = np.where(
            (df['endTime'].dt.hour != 23) |
            (df['endTime'].dt.minute != 59) |
            (df['endTime'].dt.second != 59) |
            ~df['endDay'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),1,0
        )
    df['incorrect_combined']=df[['incorrect_start_flag','incorrect_end_flag']].apply(lambda x:max(x[0],x[1]),axis=1)
    df['incorrect_combined']=df['incorrect_combined'].apply(lambda x:True if x==1 else False)
    final=df.groupby(['id','id_2'])['incorrect_combined'].any()
    return final

def _main_(path,file1,file2):
    result1=generate_car_matrix(path+file1)
    result2=get_type_count(path+file1)
    result3=get_bus_indexes(path+file1)
    result4=filter_routes(path+file1)
    result5=multiply_matrix(result1)
    result6=time_check(path+file2)
    return result1,result2,result3,result4,result5,result6

result1,result2,result3,result4,result5,result6=_main_(path,file1,file2)
