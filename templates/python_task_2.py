import pandas as pd


def calculate_distance_matrix(df) -> pd.DataFrame:
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
     'distance' column in your DataFrame
    distance_matrix = df.pivot(index='id_start', columns='id_end', values='distance').fillna(0)
    return distance_matrix


def unroll_distance_matrix(df) -> pd.DataFrame:
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    unrolled_df = df.melt(id_vars='id_start', var_name='id_end', value_name='distance')
    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id) -> pd.DataFrame:
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    reference_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold = 0.1 * reference_distance
    result_df = df.groupby('id_start')['distance'].mean().reset_index()
    result_df = result_df[(result_df['distance'] >= reference_distance - threshold) &
                          (result_df['distance'] <= reference_distance + threshold)]
    return result_df


def calculate_toll_rate(df) -> pd.DataFrame:
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
  'id_start', 'id_end', 'distance', and 'vehicle_type'
    df['toll_rate'] = df['distance'] * df['vehicle_type'].map({'car': 0.1, 'truck': 0.2, 'bus': 0.15})
    return df


def calculate_time_based_toll_rates(df) -> pd.DataFrame:
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    df['hour'] = df['timestamp'].dt.hour
    df['time_based_toll'] = df.apply(lambda row: 0.2 if 8 <= row['hour'] <= 17 else 0.1, axis=1)
    return df

