import streamlit as st
import geemap.foliumap as geemap

# setting webpage title and icon
st.set_page_config(page_title="Africa's CO2 emission Monitoring", page_icon='🛰️', layout='wide')

# temporal header
st.subheader('Live Monitoring of CO2 in Africa')


m = geemap.Map(center=[-2.635789, 24.433594], zoom=3)
m.add_basemap("SATELLITE")
m.to_streamlit(height=500)