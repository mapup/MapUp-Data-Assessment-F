import pandas as pd 
import numpy as np 

path1 = 'datasets\dataset-1.csv'
path2 = 'datasets\dataset-2.csv'
path3 = 'datasets\dataset-3.csv'

df1 = pd.read_csv(path1)
df2 = pd.read_csv(path2)
df3 = pd.read_csv(path3)
#print(df1.to_string())

def generate_car_matrix( df ):
    #df = pd.read_csv(path)
    solution_df = pd.pivot_table(df, values ='car', index =['id_1'], 
                         columns =['id_2'])
    np.fill_diagonal(solution_df.values, 0)
    return solution_df
def get_type_count(df):
    #df = pd.read_csv(path)
    df["car_type"] = np.where ( df ['car'] <= 15,   "low", 
                    np.where (df['car'] <= 25,  "medium" , "high"))
    return df
def get_bus_indexes(df):
    #df = pd.read_csv(path)
    mean_value = np.average(df["bus"])
    indices = []
    for i in df.index:
        if df["bus"][i]> 2* mean_value:
            indices.append(i)
    return indices
def filter_routes(df):
    #df = pd.read_csv(path)
    grouped_routes = df.groupby('route').agg(mean_truck_value=('truck', 'mean')).reset_index()
    filtered_data = grouped_routes[grouped_routes['mean_truck_value'] > 7]
    routes = sorted( filtered_data['route'].tolist() )
    return routes
def multiply_matrix(df):
    #df = pd.read_csv(path)
    new_df = df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    new_df = new_df.round(1)
    return new_df  
def Time_Check (df):
    #df = pd.read_csv(path)
    df = df.groupby( by = ["id", "id_2"]).agg(count =('name', 'count')).reset_index()
    print(df.head(10))
    return df

ques1_out = generate_car_matrix(df1)
ques2_out = get_type_count(df1)
ques3_out = get_bus_indexes(df1)
ques4_out = filter_routes(df1)
ques5_out = multiply_matrix(df1)
ques6_out = Time_Check(df2)


