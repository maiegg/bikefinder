import haversine
from haversine import haversine, Unit
from gbfs.services import SystemDiscoveryService
import numpy as np 
import osmnx as ox 
import networkx as nx 


# hard-code a user location like home or work (this is optional)
# # fake location :
user_loc = [42.35482454810904, -71.06568705616053]

# get user location if that's missing 
try:
    user_loc
except NameError:
    import geocoder
    g = geocoder.ip('me')
    user_loc = (g.latlng)

user_loc = {'lat':user_loc[0], 'lon':user_loc[1]}

# find closest n stations 
num_stations = 3

ds = SystemDiscoveryService()
client = ds.instantiate_client('bluebikes')
stations = client.request_feed('station_information').get('data').get('stations')

# distance in meters 
G = ox.graph_from_point((user_loc['lat'], user_loc['lon']), dist=500, network_type='walk')

user_nearest_node = ox.get_nearest_node(G, (user_loc['lat'], user_loc['lon']))

def meters_to_station(user_nearest_node, item):
    station_nearest_node = ox.get_nearest_node(G, (item['lat'], item['lon']))
    # meters
    return(
        nx.shortest_path_length(G, user_nearest_node, station_nearest_node, weight='length')
    )
    
distances = [meters_to_station(user_nearest_node, item) for item in stations]


def print_station_info(stations, distances, message):
    print(message)
    closest_station_index = np.argmin(distances)
    closest_station_distance = distances[closest_station_index]
    closest_station = stations[closest_station_index]

    def live_status_for(station):
        all_statuses = client.request_feed('station_status').get('data').get('stations')
        return next(filter(lambda x: x.get('station_id') == station.get('station_id'), all_statuses))

    def print_status_message(station):
        bikes_available = live_status_for(station).get('num_bikes_available')
        
        capacity = station.get('capacity')
        if capacity > 0:
            print('{}\nCurrently at {}% capacity with {} bikes available to rent.'.format(
            station.get('name'), int(100*bikes_available/capacity), bikes_available))
        else: 
            print('{}\nCurrently at 0% capacity with {} bikes available to rent.'.format(
            station.get('name'), bikes_available))

    print_status_message(closest_station)

    walking_speed_meters_per_second = 1.35 # https://www.healthline.com/health/exercise-fitness/average-walking-speed
    
    if distances[closest_station_index] / 1.2 >= 500:
        print('Warning - station may be more than 500 meters away (off street map)')
        
    print(f"{distances[closest_station_index] / (walking_speed_meters_per_second * 60):.1f} minutes away")
    print(f"Station coords: {closest_station['lat']:.5f}, {closest_station['lon']:.5f}")
    
    return(closest_station_index)
    
    
if num_stations == 1:
    reported_on_station = print_station_info(stations, distances, 'Closest station to you is:')
else:
    reported_on_station = print_station_info(stations, distances, 'Closest station to you is:')
    del stations[reported_on_station]
    del distances[reported_on_station]

    for next_index in range(num_stations - 1):
        reported_on_station = print_station_info(stations, distances, '\nNext closest:')
        del stations[reported_on_station]
        del distances[reported_on_station]