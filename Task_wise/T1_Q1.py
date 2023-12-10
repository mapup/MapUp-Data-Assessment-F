import pandas as pd

file_path1 = "https://raw.githubusercontent.com/mapup/MapUp-Data-Assessment-F/main/datasets/dataset-1.csv"
df1 = pd.read_csv(file_path1)

file_path2 = "https://raw.githubusercontent.com/mapup/MapUp-Data-Assessment-F/main/datasets/dataset-2.csv"
df2 = pd.read_csv(file_path2)

def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    car_mat = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    
    for index in car_mat.index:
        if index in car_mat.columns:
            car_mat.loc[index, index] = 0
    return car_mat

print("ANSWER FOR Q1 : ")
result_1 = generate_car_matrix(df1)
print(result_1)