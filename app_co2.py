import ee
import json
import streamlit as st
import geopandas as gpd
import geemap.foliumap as geemap
import geopandas as gpd
import geemap as geemap_r

# setting webpage title and icon
st.set_page_config(page_title="Africa's CO2 emission Monitoring", page_icon='🛰️', layout='wide')

# temporal header
st.subheader('Live Monitoring of Air Quality in Africa')
st.write("""
This dataset provides near real-time high-resolution imagery of UV Aerosol Index, Concentrations of Carbon monoxide (CO) 
         and water vapor, Formaldehyde. Other important greenhouse gases such as the total, tropospheric, and stratospheric 
         nitrogen dioxide concentration, Total atmospheric column ozone concentration, Atmospheric sulphur dioxide (SO₂) 
         concentration, and Atmospheric methane (CH₄) concentration are included in this application for visualization.

The source of this dataset is obtained from the [Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets/catalog/sentinel-5p), 
         and the details of this individual gases can be found in the catalog.
""")

# initializing earth engine credentials
json_data = st.secrets["json_data"]
service_account = st.secrets["service_account"]

json_object = json.loads(json_data, strict=False)
json_object = json.dumps(json_object)
credentials = ee.ServiceAccountCredentials(service_account, key_data=json_object)
ee.Initialize(credentials)


# designing the app to focus on Africa
m = geemap.Map(center=[-2.635789, 24.433594], zoom=3.2)
#m.add_basemap("OpenTopoMap")
m.add_basemap("SATELLITE")

# getting Africa shapefile
shp_path = 'africa_outline.geojson'

with open(shp_path) as f:
  json_data = json.load(f)

# convert to ee data as study_feature
study_feature = geemap.geojson_to_ee(json_data)

collection = ee.ImageCollection('COPERNICUS/S5P/NRTI/L3_CO')\
  .select('CO_column_number_density')\
  .filterDate('2023-06-01', '2023-06-11')\
  .filterBounds(study_feature)

# clip the collection to the Africa plate
africa_col = collection.mean().clip(
  study_feature
)

band_viz = {
  'min': 0,
  'max': 0.8,
  'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']
}

m.addLayer(study_feature, {}, 'Africa')
m.addLayer(africa_col, band_viz, 'S5P CO')
#m.add_geojson(africa_json,'Africa')
m.add_colorbar(band_viz, label='CO concentrations', layer_name='Colorbar',position='bottomright',
               background_color='white', extend='both')

#m.add_colormap(vis_params=band_viz, label='CO concentrations',
#               width=3, height=0.2)
m.to_streamlit(height=600, width=700)