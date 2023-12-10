#1
import pandas as pd
def generate_car_matrix(file_path):
    df = pd.read_csv('dataset-1.csv')

    pivot_table = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    for col in pivot_table.columns:
        pivot_table.at[col, col] = 0

    return pivot_table

file_path = 'dataset-1.csv'
result_matrix = generate_car_matrix('dataset-1.csv')
print(result_matrix)



#2
import pandas as pd
def get_type_count(file_path):
    df = pd.read_csv(file_path)

    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=choices, right=False, include_lowest=True)

    type_count = df['car_type'].value_counts().to_dict()

    type_count = dict(sorted(type_count.items()))

    return type_count

file_path = 'dataset-1.csv'
result = get_type_count(file_path)
print(result)



#3
import pandas as pd
def get_bus_indexes(file_path):
    df = pd.read_csv(file_path)

    mean_bus = df['bus'].mean()

    bus_indexes = df[df['bus'] > 2 * mean_bus].index.tolist()

    bus_indexes.sort()

    return bus_indexes

file_path = 'dataset-1.csv'
result = get_bus_indexes(file_path)
print(result)



#4
import pandas as pd
def filter_routes(file_path):
  
    df = pd.read_csv(file_path)

    average_truck_by_route = df.groupby('route')['truck'].mean()

    filtered_routes = average_truck_by_route[average_truck_by_route > 7].index.tolist()

    filtered_routes.sort()

    return filtered_routes

file_path = 'dataset-1.csv'
result = filter_routes(file_path)
print(result)




#5
def multiply_matrix(input_matrix):
    # Apply the multiplication logic and round the values to 1 decimal place
    modified_matrix = input_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25).round(1)
    
    return modified_matrix

# Example usage (assuming you have the result_matrix from Question 1):
modified_result = multiply_matrix(result_matrix)
print(modified_result)




#6
import pandas as pd
def verify_timestamp_completeness(df):
    
    df['timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], errors='coerce')
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], errors='coerce')

    df = df.dropna(subset=['timestamp', 'end_timestamp'])

    # Group by (id, id_2)
    grouped = df.groupby(['id', 'id_2'])

    completeness_check = grouped.apply(check_completeness).reset_index(level=[0, 1], drop=True)

    return completeness_check

def check_completeness(group):
    
    full_day_coverage = group['timestamp'].min().hour == 0 and group['end_timestamp'].max().hour == 23

    day_span = len(group['timestamp'].dt.dayofweek.unique()) == 7

    return full_day_coverage and day_span

file_path = 'dataset-2.csv'
df = pd.read_csv(file_path)
result = verify_timestamp_completeness(df)
print(result)
