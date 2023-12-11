import pandas as pd
import numpy as np


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
    index = list(set(df["id_1"]))
    columns = list(set(df["id_2"]))
    cars = df["car"]
    index.sort()
    columns.sort()

    res_df = pd.DataFrame(index=index, columns=columns)

    for x,y,z in zip(df["id_1"], df["id_2"], cars):
        res_df.loc[x, y] = z

    res_df = res_df.fillna(0)
    #print(res_df)
    return res_df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here

    cars = list(df["car"])
    #print(cars)
    type_list = []
    type_dict = {"high" : 0,
                "low":0,
                "medium" : 0}
    

    for value in cars:
        #print(value)
        if value <= 15:
            type_list.append('low')
            type_dict['low'] = type_dict['low'] + 1
        elif value > 15 and value <= 25:
            type_list.append('medium')
            type_dict['medium'] = type_dict['medium'] + 1
        elif value > 25:
            type_list.append('high')
            type_dict['high'] = type_dict['high'] + 1

    df["car_type"] = type_list

    sorted_dict = dict(sorted(type_dict.items()))
    return sorted_dict


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    my_array = np.array(df["bus"])
    mean = np.mean(my_array)
    mean2 = mean*2
    print(mean2)
    buses = list(df["bus"])
    indexes = list(df.index)
    ind_list = []
    for index,value in zip(indexes,buses):
        if value > mean2:
            ind_list.append(index)

    ind_list.sort()
    return ind_list


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    my_array = np.array(df["truck"])
    mean = np.mean(my_array)
    val_list = []
    for value in df["route"]:
        if mean - value > 7:
            val_list.append(value)
    val_list.sort()
    return val_list

def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    for column in matrix.columns:
        for index, value in matrix[column].items():
            if value > 20:
                matrix.at[index, column] = value * (0.75)
            else:
                matrix.at[index, column] = value * (1.25)

    matrix = matrix.round(1)

    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here

    return pd.Series()


# Using the special variable  
# __name__ 
if __name__=="__main__": 
    print("Pratik")
    vehicles = pd.read_csv("/workspaces/MapUp-Data-Assessment-F/datasets/dataset-1.csv")
    vehicle_df = pd.DataFrame(vehicles)
    car_matrix_df = generate_car_matrix(vehicle_df)
    #car_type_dict = get_type_count(vehicle_df)
    #print(car_type_dict)
    #val_list = filter_routes(vehicle_df)
    #print(val_list) 
    #print(len(route_val_list))

    #df_normalised = multiply_matrix(car_matrix_df)
    #print(df_normalised)







