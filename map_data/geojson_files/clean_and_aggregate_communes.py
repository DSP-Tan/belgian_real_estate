import json
from pathlib import Path
import geopandas as gpd

input_file = Path("sh_statbel_statistical_sectors_3812_20240101.geojson")
output_file = Path("communes.geojson")

gdf = gpd.read_file(input_file)

# Remove german and dutch duplicates of certain properties, keep only french
gdf = gdf.drop(columns=[col for col in gdf.columns if col.endswith("_nl") or col.endswith("_de")])

# aggregate to commune level 
gdf_districts = gdf.dissolve(by="cd_munty_refnis", as_index=False)

gdf_districts.to_file(output_file, driver="GeoJSON")
print(f"Aggregated GeoJSON saved to {output_file}")
