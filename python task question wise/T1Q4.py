import pandas as pd

def filter_routes():
    # Load the dataset from CSV file into a DataFrame
    df = pd.read_csv('dataset-1.csv')

    # Group by 'route' and calculate the average of 'truck' for each route
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' is greater than 7
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of selected routes
    selected_routes.sort()

    return selected_routes


result_routes = filter_routes()
print(result_routes)
