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
st.subheader('Live Monitoring of CO2 in Africa')
st.write("""
This dataset provides near real-time high-resolution imagery of CO concentrations.

Carbon monoxide (CO) is an important atmospheric trace gas for understanding tropospheric chemistry. 
         In certain urban areas, it is a major atmospheric pollutant. Main sources of CO are combustion 
         of fossil fuels, biomass burning, and atmospheric oxidation of methane and other hydrocarbons. 
         Whereas fossil fuel combustion is the main source of CO at northern mid-latitudes, the oxidation of 
         isoprene and biomass burning play an important role in the tropics. TROPOMI on the Sentinel 5 Precursor 
         (S5P) satellite observes the CO global abundance exploiting clear-sky and cloudy-sky Earth radiance 
         measurements in the 2.3 μm spectral range of the shortwave infrared (SWIR) part of the solar spectrum. 
         TROPOMI clear sky observations provide CO total columns with sensitivity to the tropospheric boundary layer. 
         For cloudy atmospheres, the column sensitivity changes according to the light path.
""")

# initializing earth engine credentials
json_data = st.secrets["json_data"]
service_account = st.secrets["service_account"]

json_object = json.loads(json_data, strict=False)
json_object = json.dumps(json_object)
credentials = ee.ServiceAccountCredentials(service_account, key_data=json_object)
ee.Initialize(credentials)


# designing the app to focus on Africa
m = geemap.Map(center=[-2.635789, 24.433594], zoom=3)
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
  min: 0,
  max: 0.05,
  'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']
}

m.addLayer(africa_col, band_viz, 'S5P CO')
#m.add_geojson(africa_json,'Africa')
# m.add_colorbar(band_viz, label='CO concentrations', layer_name='Colorbar',position='bottomright',
#                background_color='white',vmin=0, vmax=0.5)
m.add_colormap(vis_params=band_viz, label='CO concentrations',
               width=2.5, height=0.2)
m.to_streamlit(height=600, width=700)