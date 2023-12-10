import pandas as pd
# Read the CSV file into a DataFrame
df = pd.read_csv(r'C:\Users\LENOVO\Documents\Assessment\MapUp-Data-Assessment-F\datasets\dataset-1.csv')
def generate_car_matrix(data_set):
# Create a table with id_1 as index, id_2 as columns, and car as value
    tab_df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
# Set diagonal values to 0
    for i in tab_df.columns.intersection(tab_df.index):
        tab_df.loc[i, i] = 0
# Return the result
    return tab_df
matrix_ans = generate_car_matrix(df)
print(matrix_ans)





# Solution 2
def i_car_type(car_value):
    if car_value <= 15:
        return 'low'
    elif car_value <= 25:
        return 'medium'
    else:
        return 'high'
def get_type_count(data_set):
# Read the CSV file into a DataFrame
    df = pd.read_csv(r'C:\Users\LENOVO\Documents\Assessment\MapUp-Data-Assessment-F\datasets\dataset-1.csv')

# Add a new column 'car_type' based on 'car' values
    df['car_type'] = df['car'].apply(i_car_type)
# Count occurrences of each car type
    type_counts = df['car_type'].value_counts().sort_index()
# Convert the result to a dictionary
    result_dict = type_counts.to_dict()
    return result_dict

result = get_type_count(df)
print(result)


def get_bus_indexes(df):
    bus_mean = df['bus'].mean()
    indices = df.loc[df['bus'] > 2 * bus_mean].index.tolist()
    return sorted(indices)

result = get_bus_indexes(df)
print(result)



def filter_routes(df):
    avg_truck_route = df.groupby('route')['truck'].mean()
    route_selection = avg_truck_route [avg_truck_route > 7].index.tolist()
    return sorted(route_selection)

result1 = filter_routes(df)
print(result1)



def multiply_matrix(matrix):
    # Create the copy of the dataframe

    Data_frame_Modified = matrix.copy()
    #Multiply Values greater than 20 by 0.75 & equals to and less than 20 by 1.25
    Data_frame_Modified = Data_frame_Modified.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    #Round values to 1 decimal
    Data_frame_Modified = Data_frame_Modified.round(1)
    return Data_frame_Modified



def time_check(df):
    df_path = pd.read_csv(r'C:\Users\LENOVO\Documents\Assessment\MapUp-Data-Assessment-F\datasets\dataset-2.csv')
    # combine date & time columns to create start and end time
    df['start_time'] = pd.to_datetime(df['start_day'] + '' + df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_day'] + '' + df['end_time'])
    #calculate the duration of each time interval
    df['duration'] = df['end_time'] - df['start_time']
    check_completeness = ((df['duration'] == pd.Timedelta(days = 1) & # 24 hours
    (df['start_time'].dt.dayofweek == 0) & # Monday
    (df['end_time'].dt.dayofweek == 6) )) # Sunday

    complete_series = check_completeness.groupby(['id', 'id_2']).all()
    return complete_series
