from pdb import line_prefix
import streamlit as st
import geemap
#from streamlit_metrics import metric, metric_row
from streamlit_ace import st_ace
import pandas as pd
import leafmap.foliumap as leafmap
import ee
import extra_streamlit_components as stx
import re

# setting webpage title and icon
st.set_page_config(page_title="Africa's CO2 emission Monitoring", page_icon='🛰️', layout='wide')

# temporal header
st.subheader('Live Monitoring of CO2 in Africa')


with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map()
        m.split_map(
            left_layer='ESA WorldCover 2020 S2 FCC', right_layer='ESA WorldCover 2020'
        )
        m.add_legend(title='ESA Land Cover', builtin_legend='ESA_WorldCover')

m.to_streamlit(height=700)