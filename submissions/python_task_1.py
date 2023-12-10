import os
import pandas as pd
import numpy as np 

def generate_car_matrix(df: pd.DataFrame) -> pd.DataFrame:
    car_matrix = pd.pivot_table(df, values='car', index='id_1', columns='id_2', fill_value=0)
    car_matrix.values[np.diag_indices_from(car_matrix)] = 0
    return car_matrix


def get_type_count(df: pd.DataFrame) -> dict:
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])
    type_count = df['car_type'].value_counts().to_dict()
    return dict(sorted(type_count.items()))


def get_bus_indexes(df: pd.DataFrame) -> list:
    mean_bus = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.tolist()
    return sorted(bus_indexes)


def filter_routes(df: pd.DataFrame) -> list:
    avg_truck_by_route = df.groupby('route')['truck'].mean()
    selected_routes = avg_truck_by_route[avg_truck_by_route > 7].index.tolist()
    return sorted(selected_routes)


def multiply_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    modified_matrix = matrix.apply(lambda x: x.map(lambda y: y * 0.75 if y > 20 else y * 1.25)).round(1)
    return modified_matrix


def time_check(df: pd.DataFrame) -> pd.Series:
    df['start_time'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%A %H:%M:%S')
    df['end_time'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%A %H:%M:%S')
    df['duration'] = df['end_time'] - df['start_time']

    completeness_check = df.groupby(['id', 'id_2'])['duration'].agg(
        lambda x: (x.max() - x.min()) >= pd.Timedelta(days=7) and (x.max().time() == pd.Timestamp('23:59:59').time())
    )

    return completeness_check


# Apply the functions using shared dataset-1
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the CSV file in the subdirectory
csv_file_path_1 = os.path.join(script_dir, 'dataset', 'dataset-1.csv')

# Read the CSV file using the relative path
df_shared_1 = pd.read_csv(csv_file_path_1)
#df_shared_1 = pd.read_csv('C:/Users/anshu/Desktop/Assesement/MapUp-Data-Assessment-F/datasets/dataset-1.csv')
car_matrix_shared = generate_car_matrix(df_shared_1)
type_count_shared = get_type_count(df_shared_1)
bus_indexes_shared = get_bus_indexes(df_shared_1)
selected_routes_shared = filter_routes(df_shared_1)
modified_matrix_shared = multiply_matrix(car_matrix_shared)

# Apply the functions using shared dataset-2 for time_check
# Construct the relative path to the CSV file in the subdirectory
csv_file_path_2 = os.path.join(script_dir, 'dataset', 'dataset-2.csv')

# Read the CSV file using the relative path
df_shared_2 = pd.read_csv(csv_file_path_2)
#df_shared_2 = pd.read_csv('C:/Users/anshu/Desktop/Assesement/MapUp-Data-Assessment-F/datasets/dataset-2.csv')
time_completeness_check_shared = time_check(df_shared_2)

# Print or use the results as needed
print("Car Matrix:")
print(car_matrix_shared)
print("\nCar Type Count:")
print(type_count_shared)
print("\nBus Indexes:")
print(bus_indexes_shared)
print("\nSelected Routes:")
print(selected_routes_shared)
print("\nModified Matrix:")
print(modified_matrix_shared)
print("\nTime Completeness Check:")
print(time_completeness_check_shared)
