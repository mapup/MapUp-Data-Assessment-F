import pandas as pd
import numpy as np

# Task 1: Car Matrix Generation
def generate_car_matrix(df):
    df_pivot = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    np.fill_diagonal(df_pivot.values, 0)
    return pd.DataFrame(df_pivot, dtype=int)

# Task 2: Car Type Count Calculation
def get_type_count(df):
    df['car_type'] = pd.cut(df['car'], bins=[-np.inf, 15, 25, np.inf], labels=['low', 'medium', 'high'])
    type_count = df['car_type'].value_counts().to_dict()
    return dict(sorted(type_count.items()))

# Task 3: Bus Count Index Retrieval
def get_bus_indexes(df):
    mean_bus = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.tolist()
    return sorted(bus_indexes)

# Task 4: Route Filtering
def filter_routes(df):
    avg_truck_by_route = df.groupby('route')['truck'].mean()
    selected_routes = avg_truck_by_route[avg_truck_by_route > 7].index.tolist()
    return sorted(selected_routes)

# Task 5: Matrix Value Modification
def multiply_matrix(df):
    modified_df = df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    return modified_df.round(1)

# Task 6: Time Check
def check_time_completeness(df):
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    
    time_check = df.groupby(['id', 'id_2']).apply(lambda x: x.set_index('start_timestamp')
                                                  .resample('H').asfreq().isna().any())
    return ~time_check

# Example usage:
dataset1 = pd.read_csv('dataset-1.csv')
dataset2 = pd.read_csv('dataset-2.csv')

# Task 1
result_df_task1 = generate_car_matrix(dataset1)
print(result_df_task1)

# Task 2
result_task2 = get_type_count(dataset1)
print(result_task2)

# Task 3
result_task3 = get_bus_indexes(dataset1)
print(result_task3)

# Task 4
result_task4 = filter_routes(dataset1)
print(result_task4)

# Task 5
result_df_task5 = multiply_matrix(result_df_task1)
print(result_df_task5)

# Task 6
time_completeness_check = check_time_completeness(dataset2)
print(time_completeness_check)
