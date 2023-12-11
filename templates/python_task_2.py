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
    # Extract data points for distance calculation
    data_points = df.drop(columns=["id"]).to_numpy()

    # Calculate the distance matrix using scipy
    distance_matrix = distance_matrix(data_points, data_points)

    # Convert the distance matrix to a DataFrame
    distance-df = pd.DataFrame(distance_matrix, columns=df["id"], index=df["id"])


    return distance-df


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here

    # Extract data into separate DataFrames for easier manipulation
    upper_triangle = df.where(~df.isna()).stack()
    lower_triangle = df.T.where(~df.T.isna()).stack()

    # Combine both triangles and rename columns
    unrolled_df = pd.concat([upper_triangle, lower_triangle], ignore_index=True)
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
    # Write your logic here

    # Calculate average distance for each ID
    average_distances = df.mean(axis=1)

    # Calculate the reference ID's average distance
    reference_average_distance = average_distances.loc[reference_id]

    # Calculate the 10% threshold
    threshold_distance = reference_average_distance * 0.1

    # Find IDs within the threshold range
    filtered_ids = average_distances[(average_distances >= (reference_average_distance - threshold_distance)) &
                                    (average_distances <= (reference_average_distance + threshold_distance))]

    return filtered_ids.to_frame(name="distance").reset_index().rename(columns={"index": "id"})



def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here

   # Define distance ranges
    distance_ranges = [(0, 5), (5, 10), (10, None)]

    # Initialize an empty dictionary to store toll rates
    toll_rates = {}

    # Loop through each vehicle type
    for vehicle_type in df["vehicle_type"].unique():
        # Filter data for the current vehicle type
        filtered_df = df[df["vehicle_type"] == vehicle_type]

        # Calculate toll rates for each distance range within the vehicle type
        for distance_min, distance_max in distance_ranges:
            # Filter data for the current distance range
            filtered_by_distance = filtered_df[(filtered_df["distance"] >= distance_min) &
                                               (filtered_df["distance"] < distance_max)]

            # Calculate average distance within the range
            average_distance = filtered_by_distance["distance"].mean()

            # Define a formula for calculating toll rate based on average distance
            toll_rate_formula = lambda distance: (0.05 * distance) + (0.1 * average_distance)

            # Calculate and store the toll rate for the current range
            toll_rates[(vehicle_type, distance_min, distance_max)] = toll_rate_formula(average_distance)

    # Convert the dictionary to a DataFrame
    toll_rates_df = pd.DataFrame.from_dict(toll_rates, orient="index", columns=["toll_rate"])

    # Rename the index columns for clarity
    toll_rates_df.index.names = ["vehicle_type", "distance_min", "distance_max"]

    return toll_rates_df
    
def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

     # Define time intervals
    time_intervals = [
        ("06:00:00", "09:00:00"),
        ("09:00:00", "15:00:00"),
        ("15:00:00", "21:00:00"),
        ("21:00:00", "06:00:00"),
    ]

    # Initialize an empty dictionary to store toll rates
    time_based_toll_rates = {}

    # Loop through each vehicle type
    for vehicle_type in df["vehicle_type"].unique():
        # Filter data for the current vehicle type
        filtered_df = df[df["vehicle_type"] == vehicle_type]

        # Calculate time-based toll rates for each time interval within the vehicle type
        for start_time, end_time in time_intervals:
            # Filter data for the current time interval
            filtered_by_time = filtered_df[(filtered_df["timestamp"].dt.time >= start_time) &
                                            (filtered_df["timestamp"].dt.time < end_time)]

            # Calculate average distance within the time interval
            average_distance = filtered_by_time["distance"].mean()

            # Define a formula for calculating toll rate based on average distance
            toll_rate_formula = lambda distance: (0.1 * distance) + (0.2 * average_distance)

            # Calculate and store the toll rate for the current time interval
            time_based_toll_rates[(vehicle_type, start_time, end_time)] = toll_rate_formula(
                average_distance
            )

    # Convert the dictionary to a DataFrame
    time_based_toll_rates_df = pd.DataFrame.from_dict(
        time_based_toll_rates, orient="index", columns=["toll_rate"]
    )

    # Rename the index columns for clarity
    time_based_toll_rates_df.index.names = ["vehicle_type", "start_time", "end_time"]

    return time_based_toll_rates_df
