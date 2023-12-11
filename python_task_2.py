import pandas as pd



def calculate_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame): Input DataFrame with columns id, id_2, and distance.

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Create a pivot table to represent the distance matrix
    distance_matrix = df.pivot(index='id', columns='id_2', values='distance')

    distance_matrix = distance_matrix.fillna(0).to_numpy()

    # Make the matrix symmetric by adding its transpose
    distance_matrix += distance_matrix.T

    return pd.DataFrame(distance_matrix, index=df['id'].unique(), columns=df['id'].unique())






def unroll_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame): Input DataFrame representing a distance matrix.

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Create a pivot table to represent the distance matrix
    distance_matrix = df.pivot(index='id', columns='id_2', values='distance')

    distance_matrix_reset = distance_matrix.reset_index()

    
    unrolled_df = pd.melt(distance_matrix_reset, id_vars='id', var_name='id_end', value_name='distance')

    
    unrolled_df.rename(columns={'id': 'id_start'}, inplace=True)

    
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]

    
    unrolled_df.reset_index(drop=True, inplace=True)

    return unrolled_df




def find_ids_within_ten_percentage_threshold(df: pd.DataFrame, reference_id: int) -> pd.DataFrame:
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame): Input DataFrame with columns 'id_start', 'id_end', and 'distance'.
        reference_id (int): Reference ID.

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()

    lower_threshold = reference_avg_distance - (reference_avg_distance * 0.1)
    upper_threshold = reference_avg_distance + (reference_avg_distance * 0.1)

    
    result_df = df.groupby('id_start')['distance'].mean().reset_index()
    result_df = result_df[(result_df['id_start'] != reference_id) & 
                          (result_df['distance'] >= lower_threshold) & 
                          (result_df['distance'] <= upper_threshold)]

    return result_df

=



def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

    return df
