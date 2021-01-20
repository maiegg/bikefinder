# bikefinder
Find the nearest bikeshare stations to your current location and report on their capacity.

Heavy lifting here is done by the [gbfs-client library](https://pypi.org/project/gbfs-client/). I love transportation, maps, and quick tricks to make life easier - this is all three. 

For any bikeshare system tracked by the `gbfs-client` library - currently over 400 worldwide, find the nearest bike share stations to a precise location or to an approximate measurement of the user's location. Report the names, coordinates, approximate walking time in minutes, and real-time remaining capacity (bikes in docks) at the station. 

Right now, Boston (where I lived for a few years) is hard-coded in: the city's bikeshare system is called `bluebikes`. However, the GBFS client tool allows you to easily discover bikeshare systems by real locations (example taken straight from docs): 
```
>>> from gbfs.services import SystemDiscoveryService
>>> ds = SystemDiscoveryService()
>>> len(ds.system_ids)
221
>>> [x.get('System ID') for x in ds.systems if 'WI' in x.get('Location')]
```
Quickly print some useful outputs including:
+ Nearest station names; the maximum number of nearest stations is configurable
+ Nearest station coordinates
+ **non-trivial** the real-world, on-street walking distance and estimated walking time
  + This is enabled by the awesome library OSMnx, which I used extensively in grad school
  + It's NOT a straight-line or haversine distance estimate - it's a real estimate based on the street network and sidewalks available in the location 
  + Since fetching graph data is expensive and it's a reasonable assumption that the user won't want to walk more than a few tens of meters, we collect a small zone around their location and warn them if there are no requested stations in the collected zone. 
    + This trick, using `if distances[closest_station_index] / 1.2 >= 500:` relies on something called a *circuity factor*<sup>1</sup> to provide an estimate of the longest walking distance reachable within the graph zone. The graph boundary is calculated by taking points within a 500-meter straight-line distance of the user's location. Using a standard academic estimate of the circuity (non-straightness) of urban street networks ( = 1.2), we can guess tha the edge of the graph roughly corrsponds to a walking distance of 600 = 500 * 1.2 meters. Thus, if there's any reported walking distances longer than this, we should be suspicious of them as it's likely we aren't capturing the full walking distance - instead, the `nearest_node` function is returning something at the edge of the graph and we're blind to any additional walking distance beyond that.
    
Here's a demonstration of the script's capability, finding the nearest Blue Bikes stations to a point in the middle of Boston Common and highlighting the shortest paths a pedestrian would take to reach them: <br>

<p align="center">
  <img src="https://github.com/maiegg/bikefinder/blob/main/bike_example.png" />
</p>

<sup>1</sup> https://tram.mcgill.ca/Research/Publications/Circuity.pdf
    
    
