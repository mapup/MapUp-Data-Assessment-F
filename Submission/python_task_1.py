import pandas as pd

# Load the datasets
df_task1 = pd.read_csv('/workspaces/MapUp-Data-Assessment-F/datasets/dataset-1.csv')
df_task2 = pd.read_csv('/workspaces/MapUp-Data-Assessment-F/datasets/dataset-2.csv')

def generate_car_matrix(df: pd.DataFrame) -> pd.DataFrame:
    matrix_data = df[['id_1', 'id_2', 'car']].copy()
    car_matrix = matrix_data.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    car_matrix.values[(range(len(car_matrix)), range(len(car_matrix)))] = 0
    return car_matrix

def get_type_count(df: pd.DataFrame) -> dict:
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)
    type_counts = df['car_type'].value_counts().to_dict()
    sorted_type_counts = dict(sorted(type_counts.items()))
    return sorted_type_counts

def get_bus_indexes(df: pd.DataFrame) -> list:
    bus_mean = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    sorted_bus_indexes = sorted(bus_indexes)
    return sorted_bus_indexes

def filter_routes(df: pd.DataFrame) -> list:
    route_avg_truck = df.groupby('route')['truck'].mean()
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    sorted_filtered_routes = sorted(filtered_routes)
    return sorted_filtered_routes

def multiply_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    modified_matrix = matrix.applymap(lambda x: x * 1.25 if x <= 20 else x * 0.75)
    modified_matrix = modified_matrix.round(1)
    return modified_matrix

def is_complete(timestamps):
    # Check if there are any missing values in timestamps
    if pd.isnull(timestamps).any():
        return False

    # Check if timestamps cover a full 24-hour period
    hourly_check = len(timestamps) == 24

    # Check if timestamps span all 7 days of the week
    duration_check = (timestamps.max() - timestamps.min()) >= pd.Timedelta(days=7)

    return hourly_check and duration_check

def time_check(df):
    # Convert startDay and endDay to datetime with the correct format
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%A %I:%M:%S', errors='coerce')
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%A %I:%M:%S', errors='coerce')

    # Group by id and id_2 and apply the completeness check
    grouped = df.groupby(['id', 'id_2'])[['start_datetime', 'end_datetime']]
    
    # Apply the is_complete function and convert the result to a boolean series
    completeness_check = grouped.apply(lambda group: is_complete(group.values.flatten())).astype(bool)
    
    return completeness_check

# Assuming df_task1 and df_task2 are your datasets
result_question_1 = generate_car_matrix(df_task1)
print("Task 1 - Question 1 Result:")
print(result_question_1)
print()

result_question_2 = get_type_count(df_task1)
print("Task 1 - Question 2 Result:")
print(result_question_2)
print()

result_question_3 = get_bus_indexes(df_task1)
print("Task 1 - Question 3 Result:")
print(result_question_3)
print()

result_question_4 = filter_routes(df_task1)
print("Task 1 - Question 4 Result:")
print(result_question_4)
print()

result_question_5_input = generate_car_matrix(df_task1)
result_question_5 = multiply_matrix(result_question_5_input)
print("Task 1 - Question 5 Result:")
print(result_question_5)
print()

result_question_6 = time_check(df_task2)
print("Task 2 - Question 6 Result:")
print(result_question_6)