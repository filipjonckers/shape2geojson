# Convert shape files in shape directory to geoJSON
import geopandas as gpd
from pathlib import Path
import os


def convert_shps_to_geojson(input_dir="./shp", output_dir="./output"):
    # Create the output directory if it doesn't exist
    path_out = Path(output_dir)
    path_out.mkdir(parents=True, exist_ok=True)

    path_in = Path(input_dir)

    # Find all .shp files
    shp_files = list(path_in.glob("*.shp"))

    if not shp_files:
        print(f"No shapefiles found in {input_dir}")
        return

    print(f"Found {len(shp_files)} shapefiles. Starting conversion...")

    for shp_path in shp_files:
        try:
            # Read the shapefile
            # Note: geopandas handles the .dbf and .shx automatically
            gdf = gpd.read_file(shp_path)

            # CRITICAL: Leaflet requires WGS84 (EPSG:4326)
            # Most shapefiles are in local projections (like UTM)
            if gdf.crs is not None and gdf.crs != "EPSG:4326":
                gdf = gdf.to_crs(epsg=4326)

            # Define output filename
            output_filename = path_out / f"{shp_path.stem}.json"

            # Save as GeoJSON
            gdf.to_file(output_filename, driver='GeoJSON')
            print(f"Successfully converted: {shp_path.name} -> {output_filename.name}")

        except Exception as e:
            print(f"Error processing {shp_path.name}: {e}")


if __name__ == "__main__":
    convert_shps_to_geojson()
