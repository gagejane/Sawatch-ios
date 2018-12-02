import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.collections import PatchCollection
#pip install descartes
#pip install shapely

df = pd.read_csv('data/ios_telemetry.csv', index_col='id')
points = df[['latitude', 'longitude']]

#https://geopandas.readthedocs.io/en/latest/gallery/create_geopandas_from_pandas.html
#create coordinates for geopandas and a dataframe
points['Coordinates'] = list(zip(points.longitude, points.latitude))
points['Coordinates'] = points['Coordinates'].apply(Point)
gdf = gpd.GeoDataFrame(points, geometry='Coordinates')

#world template
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

#plotting
ax = world.plot(color='#E9F7EF', edgecolor='black', figsize=(20,20))
gdf.plot(ax=ax, color='red')
plt.title('Data Collection Locations', weight='bold', fontsize=25)
# plt.show()
plt.savefig('images/geomap')
