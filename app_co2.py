from pdb import line_prefix
import streamlit as st
import geemap
#from streamlit_metrics import metric, metric_row
from streamlit_ace import st_ace
import pandas as pd
import ee
import extra_streamlit_components as stx
import re

# setting webpage title and icon
st.set_page_config(page_title="Africa's CO2 emission Monitoring", page_icon='🛰️', layout='wide')

# temporal header
st.subheader('Live Monitoring of CO2 in Africa')


display, editor = st.columns((1, 1))

INITIAL_CODE = CODE_DICT[str(chosen_id)]


with editor:
    #st.write('### Code editor')
    st.write('')
               
    st.warning(f'''{st.session_state['instruction_idx'] + 1}) {instructions[chosen_id][st.session_state['instruction_idx']]}''')
    
    st.button("◀️ go back", on_click=instruction_step, args=(-1,), disabled=bool(st.session_state['instruction_idx'] == 0))
    st.button("▶️ continue", on_click=instruction_step, args=(1,), disabled=bool(st.session_state['instruction_idx']+1 >= len(instructions[chosen_id])))
    
    st.caption('The code in the box below is run in the browser. You can edit it and see the results on the left.')
    code = st_ace(
            value= '',
            language="python",
            theme="github",
            font_size=18,
            tab_size=4,
            show_gutter=True,
            key=str(chosen_id)
        )
        
    st.write('Hit `CTRL+ENTER` to refresh')
    st.write('*Remember to save your code separately!*')
                  
    with st.expander('Code solution'):
	    st.caption('The code in the box below is given for you. It gives the images that you will be using as code variables.')
	    st.code(CODE_DICT[str(chosen_id)])

with display:
    Map = geemap.Map(draw_export=False, plugin_Draw=True, add_google_map = False, tiles=None)
    Map.addLayer(ee.Image())
    #Map.add_basemap("HYBRID")

    code = code.replace('print(','st.write(')

    executable_code = []
    proj_change = ".changeProj('EPSG:3031', 'EPSG:3857')"
    for line in code.split('\n'):
        if 'Map.addLayer(' in line:
            if proj_change not in line:
                line_suffix = ''.join(line.split('Map.addLayer(')[1:])
                COMMA_MATCHER = re.compile(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)")
                args = COMMA_MATCHER.split(line_suffix)
                #st.write(args)
                if args[0][-1] == ')':
                    first_arg = args[0][:-1]
                    args = []
                    args.append(first_arg)
                    args.append(')')

                first_arg = args[0] + proj_change + ','
                new_line = 'Map.addLayer(' + first_arg + ','.join(args[1:])
                #st.write('line', line)
                #st.write(new_line)
                executable_code.append(new_line)
        else:
            executable_code.append(line)
    executable_code = '\n'.join(executable_code)
    #st.code(executable_code)
    try:
        exec(executable_code)
    except Exception as e:
        st.error(f'There was an error in your code!\n{e}')

    Map.to_streamlit(height=600)
    
    if chosen_id == '1':
        corr = 3
        ans = st.text_input('How far (in km) has the ice moved in the radar images from 2016 to 2022?', help='Distance (in km) that the ice has moved from 2016 to 2022', max_chars=4)
        if ans.replace('.','',1).isdigit():
            ans = float(ans)
            if ans < corr+corr*0.1 and ans > corr-corr*0.1:
                st.success('Well done!')
                if st.session_state.well_done is False:
                    st.snow()
                st.session_state.well_done = True
            else:
                st.error('Incorrect. Try again.')
                st.session_state.well_done = False