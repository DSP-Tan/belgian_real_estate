import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

geojson_file = Path("communes.geojson")
output_file = Path("commune_map.png")

gdf = gpd.read_file(geojson_file)

fig, ax = plt.subplots(figsize=(8, 8))
gdf.plot(ax=ax, facecolor="lightgrey", edgecolor="black", linewidth=0.5)

ax.set_axis_off()
plt.savefig(output_file, dpi=150, bbox_inches="tight")
plt.close()
