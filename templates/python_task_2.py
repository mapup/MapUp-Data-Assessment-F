import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    distance_matrix = pd.DataFrame(np.sqrt(np.square(df.values[:, np.newaxis] - df.values).sum(axis=2)),
                                   columns=df.index, index=df.index)

    return distance_matrix


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    unrolled_df = distance_matrix.unstack().reset_index(name='distance')
    unrolled_df.columns = ['id_start', 'id_end', 'distance']

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
   reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold = 0.1 * reference_avg_distance
    result_df = df.groupby('id_start')['distance'].mean().abs() <= (reference_avg_distance + threshold)
    return result_df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    unrolled_df['toll_rate'] = 0.1 * unrolled_df['distance']
    return unrolled_df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
   df['toll_rate'] = np.where((df['hour'] >= 6) & (df['hour'] < 12), 0.2,
                               np.where((df['hour'] >= 12) & (df['hour'] < 18), 0.3, 0.1))
    return df
