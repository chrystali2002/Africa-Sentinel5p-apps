import ee
import json
import datetime
import streamlit as st
import geopandas as gpd
import geemap.foliumap as geemap
import geopandas as gpd
import geemap as geemap_r

# setting webpage title and icon
st.set_page_config(page_title="Africa's CO2 emission Monitoring", page_icon='🛰️', layout='wide')

# temporal header
st.header('Live Monitoring of Air Quality in Africa', divider='rainbow')
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


#---------------------------------------------------------------------------------------------#
# Designing the columns and shape of the web application
st.write("""##### Select the gases to visualize""")
gas = st.selectbox('', ['Concentrations of Carbon monoxide (CO)',
                        'Concentrations of water vapor', 
                        'UV Aerosol Index ', 
                        'Concentrations of Formaldehyde', 
                        'Concentrations of total, tropospheric, and stratospheric nitrogen dioxide', 
                        'Concentrations of total atmospheric column ozone', 
                        'Concentrations of  atmospheric sulphur dioxide (SO₂)',
                        'Concentrations of atmospheric methane (CH₄)'])

my_col1, my_col2 = st.columns(2)  # month, year column
with my_col1:
  year = st.slider('Select Year:', 2018, 2024, 2024, key='sl_1')

with my_col2:
  month = st.selectbox('Select Month:', ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                                         'August', 'September', 'October', 'November', 'December'])

# creating dictionaries to store the information of the month in acceptable format
month_dict = {'January': '1', 'February': '2', 'March': '3', 'April': '4', 'May': '5', 'June': '6',
              'July': '7', 'August': '8', 'September': '9', 'October': '10', 'November': '11', 'December': '12'}
# Visualization
st.subheader(f"Interactive Map of showing the {gas} in Africa")
st.write(f'The Map shows the {gas} in {month} {year} for the Africa region. Zoom into the map and use the colorbar to get the \
         concentration value of the gases. Also, feel free to select any other year and month of your choice to visualize.')

# creating a nexted dictionary that contains all the information for each of the gases
gas_dict = {
  'Concentrations of Carbon monoxide (CO)': {'col': 'COPERNICUS/S5P/NRTI/L3_CO', 'band': 'CO_column_number_density', 'min': 0,
                                             'max': 0.05, 'layer_name': 'S5P CO', 'label': 'CO concentrations (mol/m^2)'},
  'Concentrations of water vapor': {'col': 'COPERNICUS/S5P/NRTI/L3_CO', 'band': 'H2O_column_number_density', 'min': 0.01,
                                    'max': 0.06., 'layer_name': 'S5P H20', 'label': 'H20 concentrations (mol/m^2)'},
  'UV Aerosol Index': {'col': 'COPERNICUS/S5P/NRTI/L3_AER_AI', 'band': 'absorbing_aerosol_index', 'min': -1,
                       'max': 2.0, 'layer_name': 'S5P Aerosol', 'label': 'UV Aerosol Index'},
  'Concentrations of Formaldehyde': {'col': 'COPERNICUS/S5P/NRTI/L3_HCHO', 'band': 'tropospheric_HCHO_column_number_density', 'min': 0,
                                     'max': 0.0003, 'layer_name': 'S5P HCHO', 'label': 'Formaldehyde concentrations (mol/m^2)'},
  'Concentrations of total, tropospheric, and stratospheric nitrogen dioxide': {'col': 'COPERNICUS/S5P/NRTI/L3_NO2', 
                                                                                'band': 'NO2_column_number_density', 'min': 0,
                                                                                'max': 0.0002, 'layer_name': 'S5P N02', 
                                                                                'label': 'Total vertical column of NO2 (mol/m^2)'},
  'Concentrations of total atmospheric column ozone': {'col': 'COPERNICUS/S5P/NRTI/L3_O3', 'band': 'O3_column_number_density', 'min': 0.12,
                                                       'max': 0.15, 'layer_name': 'S5P O3', 'label': 'Total atmospheric column of O3 (mol/m^2)'}, 
  'Concentrations of  atmospheric sulphur dioxide (SO₂)': {'col': 'COPERNICUS/S5P/NRTI/L3_SO2', 'band': 'SO2_column_number_density', 'min': 0,
                                                  'max': 0.0005, 'layer_name': 'S5P SO2', 
                                                  'label': 'SO2 vertical column density at ground level (mol/m^2)'},
  'Concentrations of atmospheric methane (CH₄)': {'col': 'COPERNICUS/S5P/OFFL/L3_CH4', 'band': 'CH4_column_volume_mixing_ratio_dry_air', 
                                                  'min': 1750, 'max': 1900, 'layer_name': 'S5P CH4', 
                                                  'label': 'Dry air mixing ratio of methane, as parts-per-billion (Mol fraction)'}
}



# catch an error, just incase the user enters the date in the future.
today = datetime.date.today()  # gets today's date
user_seletion = datetime.date(year, int(month_dict[month]), 1)

if user_seletion > today :
  st.write('''### Ooops! I know you long for the future, but select current or past date 😉''')

else:
  pass


collection = ee.ImageCollection(gas_dict[gas]['col'])\
  .select(gas_dict[gas]['band'])\
  .filterDate('2023-06-01', '2023-06-11')\
  .filterBounds(study_feature)

# clip the collection to the Africa plate
africa_col = collection.mean().clip(
  study_feature
)

band_viz = {
  'min': gas_dict[gas]['min'],
  'max': gas_dict[gas]['max'],
  'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']
}

m.addLayer(study_feature, {}, 'Africa')
m.addLayer(africa_col, band_viz, gas_dict[gas]['layer_name'])

m.add_colorbar(band_viz, label=gas_dict[gas]['label'], layer_name='Colorbar',position='bottomright',
               background_color='white', extend='both')

#m.add_colormap(vis_params=band_viz, label=gas_dict[gas]['col'],
#               width=3, height=0.2)
m.to_streamlit(height=600, width=700)