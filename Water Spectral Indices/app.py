import ee
import geemap.foliumap as geemap
import spyndex

import datetime
import pandas as pd
from dotenv import load_dotenv
from fast_dash import FastDash, Fastify, html, dmc, dash

load_dotenv()

credentials = ee.ServiceAccountCredentials(os.environ["SERVICE_ACCOUNT_EMAIL"], os.environ["CREDENTIALS_PATH"])
ee.Initialize(credentials)


data = pd.read_csv("gaul_data.csv")
data.head()


columns = ["application_domain", "contributor", "date_of_addition", "long_name", "platforms", "reference", "short_name"]
track_index = []

for index in spyndex.indices.keys():
    i = spyndex.indices[index]
    track_index.append([i.application_domain,
                        i.contributor,
                        i.date_of_addition,
                        i.long_name,
                        i.platforms,
                        i.reference,
                        i.short_name])
                        
index_df = pd.DataFrame(track_index, columns=columns)

water_indices = index_df[(index_df.application_domain == "water") & 
                    (index_df.platforms.apply(lambda x: "Landsat-OLI" in x))]

# Add label column
water_indices["label"] = water_indices.apply(lambda row: f"{row.short_name} ({row.long_name})", axis=1)

# Utility functions
def get_index_function(index_name, image_collection):
    # Get the index function from Spyndex.
    return spyndex.computeIndex(index=index_name,
                     params={"B": image_collection.select("B2"),
                            "G": image_collection.select("B3"),
                            "R": image_collection.select("B4"),
                            "N": image_collection.select("B5"),
                            "S1": image_collection.select("B6"),
                            "S2": image_collection.select("B7"),
                            "T1": image_collection.select("B10"),
                            "T2": image_collection.select("B11"),
                            "gamma": 1,
                            "alpha": 1})

def calculate_mean_index(image, region):
    mean_value = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=30,  # Adjust the scale according to your dataset and accuracy requirements
        maxPixels=1e9
    )
    return mean_value.getInfo()

# Define a color palette manually.
palette = [
    '000033',  # Very dark blue
    '000066',  # Dark blue
    '000099',  # Medium dark blue
    '0000CC',  # Moderate blue
    '0000FF',  # Blue
    '3399FF',  # Lighter blue
    '66CCFF',  # Light blue
    '99CCFF',  # Very light blue
    'CCE6FF'   # Extremely light blue
]


# Define components
country_component = dmc.Select(data=data.ADM0_NAME.unique().tolist(), 
                               value="United States of America",
                               label="Country of interest",
                               searchable=True)

state_component = dmc.Select(label="State, provience or an equivalent administrative unit",
                             value="New York",
                             searchable=True)

county_component = dmc.Select(label="County, district or an equivalent administrative unit",
                              value="Albany",
                             searchable=True)

index_component = dmc.Select(data=water_indices.label.unique().tolist(),
                             value="NDVIMNDWI (NDVI-MNDWI Model)",
                             searchable=True,
                             clearable=True)

map_component = Fastify(html.Iframe(height="100%"), "srcdoc", label_="aijgdi")

# Define a function that takes start_date, end_date, country, city, and index as arguments.
def water_spectral_indices(country: country_component,
                        state_or_province: state_component = None,
                        county_or_district: county_component = None,
                        water_index: index_component = None,
                        minimum_index_value: int = -1,
                        maximum_index_value: int = 1) -> map_component:
    
    """
    Visualize the selected water spectral index. Select your geography from the inputs to get started. Map on the left displays the median index value \
    for the years 2013 - 2015 and the map on the right displays median values for the years 2021-2023. Compare the two maps to understand how these values \
    changed over the years.
    
    Learn more about the Spyndex Python library that enables this dynamic index computation [here](https://github.com/awesome-spectral-indices/spyndex).
    
    :param country: The country of interest.
    :type country: str
    
    :param state_or_province: State, provience or an equivalent administrative unit.
    :type state_or_province: str
    
    :param county_or_district: County, district or an equivalent administrative unit.
    :type county_or_district: str
    
    :param water_index: Name of the water index.
    :type water_index: str
    
    :return: HTML of the leafmap object.
    :rtype: str
    """
    
    if not state_or_province:
        raise Exception("Please select a state")
        
    if not county_or_district:
        raise Exception("Please select a county")
    
    # Load the Global Administrative Unit Layers (GAUL) dataset, which includes administrative boundaries.
    admin_boundaries = ee.FeatureCollection('FAO/GAUL/2015/level2')

    # Filter the GAUL dataset for the specified city and country.
    geometry = admin_boundaries \
        .filter(ee.Filter.eq('ADM0_NAME', country)) \
        .filter(ee.Filter.eq('ADM1_NAME', state_or_province)) \
        .filter(ee.Filter.eq('ADM2_NAME', county_or_district)) \
        .geometry()
        
    # Load a satellite image collection (e.g., Landsat 8 Surface Reflectance).
    left_image = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR') \
        .filterBounds(geometry) \
        .filterDate("2013-01-01", "2015-12-31") \
        .median() \
        .clip(geometry)
    
    right_image = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR') \
        .filterBounds(geometry) \
        .filterDate("2021-01-01", "2023-12-31") \
        .median() \
        .clip(geometry)
    
    # Get index name
    index_name = water_indices[water_indices.label == water_index].short_name.iloc[0]
    
    index_function_left = get_index_function(index_name, left_image)
    index_function_right = get_index_function(index_name, right_image)
    
    # Generate legend and visualization parameters
    # Define visualization parameters using the custom palette.
    vis_params = {
        'min': minimum_index_value,
        'max': maximum_index_value,
        'palette': palette
    }

    # Calculate the range interval for each color.
    num_colors = len(palette)
    interval = 2.0 / num_colors

    # Create the legend dictionary with range values as keys.
    legend_dict = {}
    for i, color in enumerate(palette):
        # Define the range for each color.
        range_min = round(-1 + i * interval, 2)
        range_max = round(-1 + (i + 1) * interval, 2)
        # Use the range as the key and the color as the value.
        legend_dict[f'{range_min}-{range_max}'] = color
    
    # Visualize the spectral index using Geemap.
    Map = geemap.Map(basemap="CartoDB.Positron")
    Map.centerObject(geometry, zoom=11)
    
    left_layer = geemap.ee_tile_layer(index_function_left, vis_params, f"{index_name} 2013-2015")
    right_layer = geemap.ee_tile_layer(index_function_right, vis_params, f"{index_name} 2021-2023")
    Map.split_map(left_layer, right_layer)

    # Add a legend to the map.
    Map.add_legend(title="Legend", legend_dict=legend_dict, position='bottomright')
    
    comparison_map = Map.to_html()

    return comparison_map

# Initialize Fast Dash app
app = FastDash(water_spectral_indices, port=8001, theme="cosmo", mode="external")

# Additional functionality
# Keep only the states present in the selected country
@app.app.callback(dash.Output("state_or_province", "data"),
                 dash.Input("country", "value"))
def filter_states(country):
    return sorted(data[data.ADM0_NAME == country].ADM1_NAME.unique().tolist())

# Keep only the counties present in the selected country and state
@app.app.callback(dash.Output("county_or_district", "data"),
                 dash.Input("country", "value"),
                 dash.Input("state_or_province", "value"))
def filter_counties(country, state):
    filtered_data = data.copy()
    if country:
        filtered_data = filtered_data[filtered_data.ADM0_NAME == country]
        
    if state:
        filtered_data = filtered_data[filtered_data.ADM1_NAME == state]
        
    return sorted(filtered_data.ADM2_NAME.unique().tolist())

# Deploy the underlying Flask app
server = app.server

if __name__ == "__main__":
    app.run()