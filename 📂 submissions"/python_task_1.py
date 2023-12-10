import pandas as pd

### Question 1: Car Matrix Generation

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
    pivot_df=df.pivot(index='id_1',columns='id_2',values='car')
    df=pivot_df.fillna(0).astype(int)
    for i in range(min(df.shape[0],df.shape[1])):
        df.iloc[i,i]=0
    

    return df

### using the function
df=pd.read_csv('dataset-1.csv')
final_result=generate_car_matrix(df)
print(final_result)


### Question 2: Car Type Count Calculation
def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df['car_type']=pd.cut(df['car'],bins=[-float('inf'),15,25,float('inf')],
                          labels=['low','medium','high'],right=False)
    type_count=df['car_type'].value_counts().to_dict()
    sorted_type_Count={k:type_count[k] for k in sorted(type_count)}
    
    return sorted_type_Count

### using the function
final_result=get_type_count(df)
print(final_result)


### Question 3: Bus Count Index Retrieval
def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    bus_mean=df['bus'].mean()
    bus_indices=df[df['bus']>2*bus_mean].index.tolist()
    bus_indices.sort()
    return bus_indices

### Using function
final_result=get_bus_indexes(df)
print(final_result)


### Question 4: Route Filtering
def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    route_avg_truck=df.groupby('route')['truck'].mean()
    selected_routes=route_avg_truck[route_avg_truck>7].index.tolist()
    selected_routes.sort()
    
    return selected_routes

#### using the function
final_result=filter_routes(df)
print(final_result)

### Question 5: Matrix Value Modification

def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    df=generate_car_matrix(matrix)
    modified_matrix=df.applymap(lambda x:x * 0.75 if x > 20 else x * 1.25)
    return modified_matrix

### using the function
final_result=multiply_matrix(df)
print(final_result)

#### Question 6: Time Check

def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    weekday_mapping = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}

    # Map 'startDay' and 'endDay' to numeric values
    df['start_day_numeric'] = df['startDay'].map(weekday_mapping)
    df['end_day_numeric'] = df['endDay'].map(weekday_mapping)
    df['start_timestamp'] = pd.to_datetime(df['start_day_numeric'].astype(str) + ' ' + df['startTime'], errors='coerce')

    # Combine 'end_day_numeric' and 'endTime' to create 'end_timestamp'
    df['end_timestamp'] = pd.to_datetime(df['end_day_numeric'].astype(str) + ' ' + df['endTime'], errors='coerce')

    # Extract day of the week and time from start and end timestamps
    df['start_day_of_week'] = df['start_timestamp'].dt.dayofweek
    df['end_day_of_week'] = df['end_timestamp'].dt.dayofweek
    df['start_time'] = df['start_timestamp'].dt.time
    df['end_time'] = df['end_timestamp'].dt.time

    # Check if each (id, id_2) pair covers a full 24-hour period and spans all 7 days
    completeness_check = (
            df.groupby(['id', 'id_2'])
            .apply(lambda group: (group['start_time'].min() == pd.Timestamp('00:00:00')) and
                                (group['end_time'].max() == pd.Timestamp('23:59:59')) and
                                (set(group['start_day_of_week']).union(set(group['end_day_of_week'])) == set(range(7))))
        )
    return completeness_check


# using the function 
df1=pd.read_csv('dataset-2.csv')
final_result=time_check(df1)
print(final_result)