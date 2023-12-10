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
    unique_ids = sorted( list(set(df["id_start"].tolist()+df["id_end"].tolist() ) ))
    df = df.sort_values("id_start")
    df = df.groupby("id_start").agg(id_end=('id_end', 'min'), distance=('distance', 'min') ).reset_index()

    grid = pd.DataFrame(index=unique_ids, columns=unique_ids)
    np.fill_diagonal(grid.values, 0)
    k = 0
    print(df)
    # print(len(df.index), len(unique_ids))
    for i in df.index:
        grid[df["id_start"][i]][df["id_end"][i]] = df['distance'][i]
        grid[df["id_end"][i]][df["id_start"][i]] = df['distance'][i]
        
        for j in range(k-1, -1, -1):
            # print("haha")
            # print(k+1, j, unique_ids[k+1], unique_ids[j], unique_ids[k],  unique_ids[j],       grid[unique_ids[k]][unique_ids[j]],grid[unique_ids[k+1]][unique_ids[j+1]] )
            grid[unique_ids[k+1]][unique_ids[j]] = grid[unique_ids[k]][unique_ids[j]] + grid[unique_ids[k+1]][unique_ids[j+1]]
            grid[unique_ids[j]][unique_ids[k+1]] = grid[unique_ids[k+1]][unique_ids[j]]
        k+=1
    print(grid)

ques1_out = calculate_distance_matrix(df3)
# ques2_out = get_type_count(df1)
# ques3_out = get_bus_indexes(df1)
# ques4_out = filter_routes(df1)

# print(ques1_out)