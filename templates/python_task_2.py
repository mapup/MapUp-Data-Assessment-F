import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    pivot_table = pd.read_csv(df).pivot(index='id_start', columns='id_end', values='distance').fillna(0)
    data_frame = pivot_table.add(pivot_table.T, fill_value=0)
    for index in data_frame.index:
        data_frame.loc[index, index] = 0
    return data_frame
distance_matrix=calculate_distance_matrix('/Users/HP/Downloads/dataset-3.csv')
print(distance_matrix)

    


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    unrolled_distances = df.stack().reset_index()
    unrolled_distances.columns = ['id_start', 'id_end', 'distance']
    unrolled_distances = unrolled_distances[unrolled_distances['id_start'] != unrolled_distances['id_end']]
    unrolled_distances.reset_index(drop=True, inplace=True)
    return unrolled_distances
print(unroll_distance_matrix(distance_matrix))


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    average_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold = 0.1 * average_distance
    within_threshold = df[(df['id_start'] != reference_id) & 
                                 (df['distance'] >= average_distance - threshold) & 
                                 (df['distance'] <= average_distance + threshold)]
    result = within_threshold['id_start'].unique().tolist()
    result.sort()
    return result
reference_values = unrolled_df['id_start'].unique()
for i in reference_values:
  print(find_ids_within_ten_percentage_threshold(unrolled_df, int(i)))


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    df['moto'] = df['distance'] * 0.8
    df['car'] = df['distance'] * 1.2
    df['rv'] = df['distance'] * 1.5
    df['bus'] = df['distance'] * 2.2
    df['truck'] = df['distance'] * 3.6
    return df
toll_rate=calculate_toll_rate(unrolled_df)
print(toll_rate)



def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    df['start_day'] = df['start_time'].dt.day_name()
    df['end_day'] = df['end_time'].dt.day_name()
    df['start_time'] = df['start_time'].dt.time
    df['end_time'] = df['end_time'].dt.time
    weekday_discounts = {
        (time(0, 0, 0), time(10, 0, 0)): 0.8,
        (time(10, 0, 0), time(18, 0, 0)): 1.2,
        (time(18, 0, 0), time(23, 59, 59)): 0.8
    }
    weekend_discount = 0.7
    for key, value in weekday_discounts.items():
        mask = (df['start_time'].dt.time >= key[0]) & (df['start_time'].dt.time < key[1])
        df.loc[mask & df['start_time'].dt.weekday.isin([0, 1, 2, 3, 4]), ['moto', 'car', 'rv', 'bus', 'truck']] *= value

    mask = df['start_time'].dt.weekday.isin([5, 6])
    df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= weekend_discount
    return df
print(calculate_time_based_toll_rates(toll_rate))
