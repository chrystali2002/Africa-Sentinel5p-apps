import ee
import json
import streamlit as st
import geemap.foliumap as geemap

# setting webpage title and icon
st.set_page_config(page_title="Africa's CO2 emission Monitoring", page_icon='🛰️', layout='wide')

# temporal header
st.subheader('Live Monitoring of CO2 in Africa')

json_data = st.secrets["json_data"]
service_account = st.secrets["service_account"]


json_object = json.loads(json_data, strict=False)
json_object = json.dumps(json_object)
credentials = ee.ServiceAccountCredentials(service_account, key_data=json_object)
ee.Initialize(credentials)


m = geemap.Map(center=[-2.635789, 24.433594], zoom=3)
m.add_basemap("OpenTopoMap")
m.add_basemap("SATELLITE")


collection = ee.ImageCollection('COPERNICUS/S5P/NRTI/L3_CO')\
  .select('CO_column_number_density')\
  .filterDate('2019-06-01', '2019-06-11')

band_viz = {
  min: 0,
  max: 0.05,
  'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']
}

#palette: ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']
m.addLayer(collection.mean(), band_viz, 'S5P CO')
m.add_colormap(vis_params=band_viz, label='CO concentrations', layer_name='Colorbar',position=(0,0),
               vmin=0, vmax=0.5)
m.to_streamlit(height=500)