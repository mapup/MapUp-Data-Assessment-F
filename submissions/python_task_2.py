import pandas as pd
import numpy as np
from datetime import datetime as dt
from itertools import product
from datetime import time
import warnings
warnings.filterwarnings('ignore')
path = r'C:\Users\ritvi\OneDrive\Documents\GitHub\MapUp-Data-Assessment-F\datasets'
file = r'\dataset-3.csv'

# Question 1 : Distance Matrix calculation

def calculate_distance_matrix(dataset):
    df = pd.read_csv(dataset)
    df_pivot= df.pivot_table(index='id_start', columns='id_end', values='distance', aggfunc='sum', fill_value=0)

    df_distance = df_pivot.add(df_pivot.T, fill_value=0)
    # Set diagonal values to 0
    np.fill_diagonal(df_distance.values, 0)
    for i in range(len(df_distance)-2):
        for j in range(len(df_distance)-2-i):
            df_distance.iloc[j+2+i,i]=df_distance.iloc[j+1+i,i]+df_distance.iloc[j+2+i,j+1+i]
            df_distance.iloc[i,j+2+i]=df_distance.iloc[j+2+i,i]

    return df_distance

# Question 2 : Unroll distance Matrix

def unroll_distance_matrix(dataset):
    id_start=[]
    id_end=[]
    distance_list=[]
    for i in range(len(dataset.index)):
        for j in range(len(dataset.columns)):
            id_start.append(dataset.index[i])
            id_end.append(dataset.columns[j])
            distance_list.append(dataset.iloc[i,j])
    final=pd.DataFrame({'id_start':id_start,'id_end':id_end,'distance':distance_list})
    final=final[final['id_start']!=final['id_end']]
    return final

#Question 3 : Finding IDs within Percentage threshold

def threshold(result1,value):
    subset=result1[result1['id_start']==value]
    average=subset['distance'].mean()
    final=result1.groupby('id_start').agg({'distance':'mean'})
    final_list=final[(final['distance']>=0.9*average)&(final['distance']<=1.10*average)].sort_index(axis=0).index.tolist()
    return final_list

# Question 4 : Calculate toll rate

def calculate_toll_rate(result1):
    result1['moto']=0.8*result1['distance']
    result1['car']=1.2*result1['distance']
    result1['rv']=1.5*result1['distance']
    result1['bus']=2.2*result1['distance']
    result1['truck']=3.6*result1['distance']
    return result1

# Question 5 : Calculate time based tolls

def calculate_time_based_toll_rates(result4):

    # Define the time ranges
    weekday_time_ranges = [
        (time(0, 0, 0), time(10, 0, 0)),
        (time(10, 0, 0), time(18, 0, 0)),
        (time(18, 0, 0), time(23, 59, 59))
    ]

    # Weekend time ranges
    weekend_time_ranges = [
        (time(0, 0, 0), time(23, 59, 59))
    ]

    # Create a DataFrame with the weekday time ranges
    weekday_time_ranges_df = pd.DataFrame(weekday_time_ranges, columns=['start_time', 'end_time'])

    weekday_time_ranges_df = pd.concat([weekday_time_ranges_df] * len(result4), ignore_index=True)

    # Add 'id' column to the weekday_time_ranges_df
    weekday_time_ranges_df['id_start'] = result4['id_start']
    weekday_time_ranges_df['id_end'] = result4['id_end']

    # Create a DataFrame with the weekend time ranges
    weekend_time_ranges_df = pd.DataFrame(weekend_time_ranges, columns=['start_time', 'end_time'])

    # Repeat the weekend time ranges for each unique id
    weekend_time_ranges_df = pd.concat([weekend_time_ranges_df] * len(result4), ignore_index=True)

    # Add 'id' column to the weekend_time_ranges_df
    weekend_time_ranges_df['id_start'] = result4['id_start']
    weekend_time_ranges_df['id_end'] = result4['id_end']


    result_df = pd.merge(result4, weekday_time_ranges_df, on=['id_start','id_end'])

    from itertools import product

    # Define the days of the week
    weekdays= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']
    weekends=['Saturday','Sunday']
    # Generate all combinations of start and end days
    day_combinations_weekdays = list(product(weekdays, repeat=2))
    day_combinations_weekends = list(product(weekends, repeat=2))

    # Create a DataFrame with the day combinations
    day_combinations_df_weekdays = pd.DataFrame(day_combinations_weekdays, columns=['start_day', 'end_day'])
    day_combinations_df_weekends = pd.DataFrame(day_combinations_weekends, columns=['start_day', 'end_day'])

    # Repeat the day combinations for each unique id
    day_combinations_df_weekdays = pd.concat([day_combinations_df_weekdays] * len(result4), ignore_index=True)
    day_combinations_df_weekdays['id_start'] = result4['id_start']
    day_combinations_df_weekdays['id_end'] = result4['id_end']

    day_combinations_df_weekends = pd.concat([day_combinations_df_weekends] * len(result4), ignore_index=True)
    day_combinations_df_weekends['id_start'] = result4['id_start']
    day_combinations_df_weekends['id_end'] = result4['id_end']

    result_df=pd.merge(result_df,day_combinations_df_weekdays,on=['id_start','id_end'])
    weekend_comb=pd.merge(weekend_time_ranges_df,day_combinations_df_weekends,on=['id_start','id_end'])
    result_df1=pd.merge(result_df[['id_start','id_end','distance','moto','car','rv','bus','truck']],weekend_comb,on=['id_start','id_end'])
    final_df=pd.concat([result_df,result_df1],axis=0)

    #result_df = pd.merge(result_df, day_combinations_df, on=['id_start','id_end'])
    final_df['start_time']=np.where((final_df['start_day'].isin(['Saturday','Sunday']))&(final_df['end_day'].isin(['Saturday','Sunday'])),time(0,0,0),final_df['start_time'])
    final_df['end_time']=np.where((final_df['start_day'].isin(['Saturday','Sunday']))&(final_df['end_day'].isin(['Saturday','Sunday'])),time(23,59,59),final_df['end_time'])

    # Print the resulting DataFrame
    final_df=final_df.drop_duplicates()
    def coeff(x):
        if x[0] in ['Saturday','Sunday']:
            return 0.7
        else:
            if x[1]==time(0,0,0):
                return 0.8
            elif x[1]==time(10,0,0):
                return 1.2
            else:
                return 0.8
    final_df['coeff']=final_df[['start_day','start_time']].apply(coeff,axis=1)
    for col in ['moto','car','rv','bus','truck']:
        final_df[col]=final_df[col]*final_df['coeff']
    del final_df['coeff']
    return final_df

def _main_(path,file,value):
    result1=calculate_distance_matrix(path+file)
    result2= unroll_distance_matrix(result1)
    result3=threshold(result2,value)
    result4=calculate_toll_rate(result2)
    result5=calculate_time_based_toll_rates(result4)
    return result1,result2,result3,result4,result5

result1,result2,result3,result4,result5=_main_(path,file,1001470)

