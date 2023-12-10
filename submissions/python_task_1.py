import pandas as pd 
import numpy as np 



# importing module 
import pyspark 
  
# # import sum, min,avg,count,mean and max functions 
# from pyspark.sql.functions import sum, max, min, avg, count, mean 
  
# # importing sparksession from pyspark.sql module 
# from pyspark.sql import SparkSession 
  
# # creating sparksession and giving an app name 
# spark = SparkSession.builder.getOrCreate() 
path1 = 'datasets\dataset-1.csv'
path2 = 'datasets\dataset-2.csv'
path3 = 'datasets\dataset-3.csv'

df1 = pd.read_csv(path1)
df2 = pd.read_csv(path2)
df3 = pd.read_csv(path3)
#print(df1.to_string())

def generate_car_matrix( path ):
    df = pd.read_csv(path)
    solution_df = pd.pivot_table(df, values ='car', index =['id_1'], 
                         columns =['id_2'])
    np.fill_diagonal(solution_df.values, 0)
    return solution_df
def get_type_count(path):
    df = pd.read_csv(path)
    df["car_type"] = np.where ( df ['car'] <= 15,   "low", 
                    np.where (df['car'] <= 25,  "medium" , "high"))
    return df
def get_bus_indexes(path):
    df = pd.read_csv(path)
    mean_value = np.average(df["bus"])
    indices = []
    for i in df.index:
        if df["bus"][i]> 2* mean_value:
            indices.append(i)
    return indices
def filter_routes(path):
    df = pd.read_csv(path)
    grouped_routes = df.groupby('route').agg(mean_truck_value=('truck', 'mean')).reset_index()
    filtered_data = grouped_routes[grouped_routes['mean_truck_value'] > 7]
    routes = sorted( filtered_data['route'].tolist() )
    return routes
def multiply_matrix(path):
    df = pd.read_csv(path)
    new_df = df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    new_df = new_df.round(1)
    return new_df  
def Time_Check (path):
    df = pd.read_csv(path)

    df = df.groupby( by = ["id", "id_2"]).agg(count =('name', 'count')).reset_index()
    print(df.head(10))





    # # Combine 'startDay' and 'startTime' columns to create a datetime column
    # df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    
    # # Combine 'endDay' and 'endTime' columns to create a datetime column
    # df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    
    # # Group by (id, id_2) pairs
    # grouped = df.groupby(['id', 'id_2'])
    
    # # Define a function to check timestamps completeness
    # def check_timestamps(group):
    #     # Check if the timestamps cover a full 24-hour period
    #     full_day_coverage = (
    #         (group['end_datetime'].max() - group['start_datetime'].min()).total_seconds() == 24 * 60 * 60
    #     )
        
    #     # Check if the timestamps span all 7 days of the week
    #     all_days_coverage = set(group['start_datetime'].dt.day_name()) == set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        
    #     return full_day_coverage and all_days_coverage

    # # Apply the check_timestamps function to each group and create a boolean series
    # completeness_series = grouped.apply(check_timestamps)

    # return completeness_series
    # #assuming endtimestamp - starttimestamp is less than 7 day and endtimestamp > starttimestamp for all rows
    
    # return df

#print(df1)
#Q1df = generate_car_matrix(df1)
print(Time_Check(path2))
