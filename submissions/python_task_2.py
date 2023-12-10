import pandas as pd 
import numpy as np 

path1 = 'datasets\dataset-1.csv'
path2 = 'datasets\dataset-2.csv'
path3 = 'datasets\dataset-3.csv'

df1 = pd.read_csv(path1)
df2 = pd.read_csv(path2)
df3 = pd.read_csv(path3)
#print(df1.to_string())

def calculate_distance_matrix(df):

    print(df)
    unique_ids =  list(set(df["id_1"].tolist()+df["id_2"].tolist() ) )
    grid = pd.DataFrame(index=unique_ids, columns=unique_ids)
    np.fill_diagonal(grid.values, 0)

    for i in df.index():
        # grid.at[row['from'], row['to']] = row['distance']
        # grid.at[row['to'], row['from']] = row['distance']  
    
    # for i in unique_ids:
    #     for j in unique_ids:
    #         for k in unique_ids:
    #             if pd.notna(cumulative_distance_grid.at[i, k]) and pd.notna(cumulative_distance_grid.at[k, j]):
    #                 # Update distance if shorter route found
    #                 if pd.isna(cumulative_distance_grid.at[i, j]) or cumulative_distance_grid.at[i, k] + cumulative_distance_grid.at[k, j] < cumulative_distance_grid.at[i, j]:
    #                     cumulative_distance_grid.at[i, j] = cumulative_distance_grid.at[i, k] + cumulative_distance_grid.at[k, j]

    return grid

    
    
    #print(cumulative_distance_grid)




ques1_out = calculate_distance_matrix(df1)
# ques2_out = get_type_count(df1)
# ques3_out = get_bus_indexes(df1)
# ques4_out = filter_routes(df1)