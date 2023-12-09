import os
import ee
from dotenv import load_dotenv
import geemap.foliumap as geemap

from fast_dash import FastDash, html, Fastify

load_dotenv()

credentials = ee.ServiceAccountCredentials(os.environ["SERVICE_ACCOUNT_EMAIL"], os.environ["CREDENTIALS_PATH"])
ee.Initialize(credentials)

# Define years over which we'll compare land cover
years = ['2001', '2004', '2006', '2008', '2011', '2013', '2016', '2019']

# Using Fastify, Fast Dash allows making any Dash component suitable with Fast Dash
iframe_component = html.Iframe(height="100%")

# Build and deploy!
# If running locally, feel free to drop the mode and port arguments.
def compare_land_cover(year_of_left_layer: str = years, 
                       year_of_right_layer: str = years) -> iframe_component:
    "Compare how land cover in the US changed over the years"

    # Geemap code. Ref: https://huggingface.co/spaces/giswqs/geemap/blob/main/app.py
    Map = geemap.Map(center=(40, -100), zoom=4, height=600)

    nlcd_left = ee.Image(
        f"USGS/NLCD_RELEASES/2019_REL/NLCD/{year_of_left_layer}"
    ).select("landcover")
    nlcd_right = ee.Image(
        f"USGS/NLCD_RELEASES/2019_REL/NLCD/{year_of_right_layer}"
    ).select("landcover")

    left_layer = geemap.ee_tile_layer(nlcd_left, {}, f"NLCD {year_of_left_layer}")
    right_layer = geemap.ee_tile_layer(nlcd_right, {}, f"NLCD {year_of_right_layer}")

    Map.split_map(left_layer, right_layer)

    # Convert to HTML
    land_cover_map = Map.to_html()

    return land_cover_map

app = FastDash(compare_land_cover, theme="Zephyr")
server = app.server

if __name__ == "__main__":
    app.run()