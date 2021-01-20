# Illustrate:
import matplotlib.pyplot as plt 

# distance in meters 
G = ox.graph_from_point((user_loc['lat'], user_loc['lon']), dist=1000, network_type='walk')

user_nearest_node = ox.get_nearest_node(G, (user_loc['lat'], user_loc['lon']))

node_sizes = [500 if node == user_nearest_node else 0 for node in G.nodes]

# routes of interest 
route1 = nx.shortest_path(G, user_nearest_node, ox.get_nearest_node(G, (42.35498, -71.06335)), weight='length')
route2 = nx.shortest_path(G, user_nearest_node, ox.get_nearest_node(G, (42.35258, -71.06764)), weight='length')
route3 = nx.shortest_path(G, user_nearest_node, ox.get_nearest_node(G, (42.35605, -71.06985)), weight='length')

rc = ['r', 'y', 'c']

# plot the routes
fig, ax = ox.plot_graph_routes(
    G
    , routes=[route1, route2, route3]
    , route_colors=rc
    , route_linewidth=6
    , node_size=0
    , show=False
    , close=False)

ax.scatter(
    G.nodes[user_nearest_node]['x']
    , G.nodes[user_nearest_node]['y']
    , facecolors='white'
    , edgecolors='white'
    , s=650
    , alpha=0.75
)

ax.legend(['Closest station','2nd Closest Station','3rd Closest Station'])

plt.show()