import pandas as pd
from datetime import datetime, time

def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # check if required columns are in dataframe
    if 'id_start' not in dataset.columns or 'id_end' not in dataset.columns or 'distance' not in dataset.columns:
        raise ValueError("DataFrame must have 'id', 'start_id', 'end_id', and 'distance' columns.")

    # Create a DataFrame with unique toll locations
    toll_locations = pd.concat([dataset['id_start'], dataset['id_end']]).unique()
    distance_matrix = pd.DataFrame(index=toll_locations, columns=toll_locations)

    # Fill the distance matrix with known distances
    for _, row in dataset.iterrows():
        distance_matrix.loc[row['id_start'], row['id_end']] = row['distance']
        distance_matrix.loc[row['id_end'], row['id_start']] = row['distance']

    # Convert NaN values to 0 (for locations without direct connections)
    distance_matrix = distance_matrix.fillna(0)

    # Iterate through and find cumulative distances
    for i in toll_locations:
      for j in toll_locations:
        for k in toll_locations:
            if distance_matrix.loc[i, k] != 0 and distance_matrix.loc[k, j] != 0:
                if i == j:
                    distance_matrix.loc[i, j] = 0
                elif distance_matrix.loc[i, j] == 0 or distance_matrix.loc[i, k] + distance_matrix.loc[k, j] < distance_matrix.loc[i, j]:
                    distance_matrix.loc[i, j] = distance_matrix.loc[i, k] + distance_matrix.loc[k, j]

    return distance_matrix


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here

    # Create an empty list to store the unrolled data
    unrolled_data = []

    # Iterate through the rows and columns of the distance_matrix
    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            if id_start != id_end:
                distance = distance_matrix.loc[id_start, id_end]
                unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})
    print(unrolled_data)
    # Create a DataFrame from the unrolled data
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df


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
    # Check if required columns are in the dataframe
    if 'id_start' not in df.columns or 'distance' not in df.columns:
        raise ValueError("DataFrame must have 'id_start' and 'distance' columns.")

    # Find average of reference id
    reference_group = df.groupby('id_start').get_group(reference_id)
    reference_avg = reference_group['distance'].mean()

    # Define low and high 10% thresholds of reference average
    low_thresh = reference_avg*0.9
    high_thresh = reference_avg*1.1

    # Find ids with distance within threshold 10%
    result_df = df[(df['distance']>low_thresh) & (df['distance']<high_thresh)].sort_values('id_start')

    # Sort the result
    
    return result_df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    # Check if required columns are in the dataframe
    if 'distance' not in df.columns:
        raise ValueError("DataFrame must have 'distance' column.")

    # Define the toll rates for each vehicle
    toll_rates = {'moto': 0.8, 'car':1.2, 'rv':1.5, 'bus':2.2, 'truck':3.6}

    # Add the columns by multiplying with the toll rates
    for key, value in toll_rates.items():
        df[key] = df['distance'].apply(lambda s : s*value)

    # Drop the distance column
    toll_df = df.drop('distance', axis=1)

    return toll_df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    # Convert the dataframe to a list of dictionaries with each dictionary the rows.
    df_dict = df.to_dict(orient='records')

    # Dictionary with time stamps and corresponding toll rates
    toll_times = [{'start_day':'Monday', 'start_time':'00:00:00', 'end_day':'Friday', 'end_time':'10:00:00','toll_rate':0.8},
              {'start_day':'Tuesday', 'start_time':'10:00:00', 'end_day':'Saturday', 'end_time':'18:00:00','toll_rate':1.2},
              {'start_day':'Wednesday', 'start_time':'18:00:00', 'end_day':'Sunday', 'end_time':'23:59:59','toll_rate':0.8},
              {'start_day':'Saturday', 'start_time':'00:00:00', 'end_day':'Sunday', 'end_time':'23:59:59','toll_rate':0.7}]

    new_df_dict = []
    # Creating the modified rows
    for row in df_dict:
        for toll in toll_times:
            modified_row = row.copy()

            modified_row['start_day'] = toll['start_day']
            modified_row['start_time'] = toll['start_time']
            modified_row['end_day'] = toll['end_day']
            modified_row['end_time'] = toll['end_time']

            keys = ['moto', 'car', 'rv', 'bus', 'truck']

            for key in keys:
                modified_row[key] = row[key]*toll['toll_rate']

            # Append the modified row to the new data list
            new_df_dict.append(modified_row.copy())

    new_df = pd.DataFrame(new_df_dict)

    # Converting the time trings to datetime objects.
    new_df['start_time'] = new_df['start_time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time())
    new_df['end_time'] = new_df['end_time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time())

    # Rearranging the columns as required

    columns = new_df.columns.tolist()

    new_columns = columns[:3] + columns[8:12] + columns[3:8]
    new_df = new_df[new_columns]
    return new_df
