import streamlit as st
import numpy as np
import base64
import logging
from streamlit_option_menu import option_menu

########################
#   SIDEBAR SETUP        #
########################
st.set_page_config(page_title='Obesity Dashboard', page_icon=':bar_chart:', layout='wide')

if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

dashboard = st.Page('pages/Dashboard.py', title='Dashboard', icon=':material/dashboard:')
clf = st.Page('pages/clf.py', title='Classification', icon=':material/search:')

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Menu": [dashboard, clf],
        }
    )
    
    

pg.run()