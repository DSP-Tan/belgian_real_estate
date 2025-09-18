import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

geojson_file = Path("sh_statbel_statistical_sectors_3812_20240101.geojson")
output_file = Path("statistical_sectors.png")

gdf = gpd.read_file(geojson_file)

fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, facecolor="lightgrey", edgecolor="black", linewidth=0.2)
ax.set_axis_off()

plt.savefig(output_file, dpi=300, bbox_inches="tight")
plt.close()
