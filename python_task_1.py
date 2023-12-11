import pandas as pd
df = pd.read_csv('dataset-1.csv')
def generate_car_matrix(data):
    result_df = data.pivot(index='id_1', columns='id_2', values='car')
    result_df.fillna(0, inplace=True)  
    result_df.values[[range(len(result_df))], [range(len(result_df))]] = 0   
    return result_df
new_df = generate_car_matrix(df)
print(new_df)

import pandas as pd
df = pd.read_csv('dataset-1.csv')
def get_type_count(data):
    data['car_type'] = pd.cut(data['car'], bins=[float('-inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])
    type_count = data['car_type'].value_counts().to_dict()
    type_count = dict(sorted(type_count.items()))
    return type_count
result = get_type_count(df)
print(result)

import pandas as pd
def get_bus_indexes(df):
    mean_bus = df['bus'].mean()
    indices = df[df['bus'] > 2 * mean_bus].index.tolist()
    return sorted(indices)

import pandas as pd
def filter_routes(df):
    route_avg = df.groupby('route')['truck'].mean()
    routes_greater_than_7 = route_avg[route_avg > 7].index.tolist()
    return sorted(routes_greater_than_7)

import pandas as pd
def multiply_matrix(result_df):
    modified_df = result_df.copy()
    modified_df = modified_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_df = modified_df.round(1)
    return modified_df

import pandas as pd
def check_time_completeness(df):
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    df['duration'] = df['end_timestamp'] - df['start_timestamp']
    grouped = df.groupby(['id', 'id_2'])
    completeness_check = grouped.apply(lambda x: (
        (x['duration'].min() >= pd.Timedelta(days=1)) and 
        (x['duration'].max() <= pd.Timedelta(days=1, seconds=1)) and 
        (x['start_timestamp'].dt.dayofweek.nunique() == 7)
    ))
    return completeness_check
