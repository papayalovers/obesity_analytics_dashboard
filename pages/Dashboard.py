import streamlit as st
import pandas as pd
from stream_src.visualization import *
from streamlit_elements import elements, mui, html
import numpy as np

########################
#   PAGE SETUP        #
########################

# def dashboard():
# st.title('Obesity Analytics Dashboard')
st.markdown("_Prototype v0.4.1_")
df = pd.read_csv('dataset/obesity.csv')

# data preview
# with st.expander('Data Preview'):
#     df = pd.read_csv('dataset/obesity.csv')
#     st.dataframe(df, use_container_width=True)


top_left_col, top_right_col = st.columns((2, 1))


with top_left_col:
    
    st.markdown('<center>Class Proportions Overview</center>', unsafe_allow_html=True) 
    st.divider()
    col_1, col_2, col_3, col_4 = st.columns(4)
    total = len(df)
    with col_1:
        val1 = len(df[df['class'] == 'Underweight'])
        plot_gauge(val1, "#0039e6", "", "Underweight", total)
    with col_2:
        val2 = len(df[df['class'] == 'Normal'])
        plot_gauge(val2, "#00ff00", "", "Normal", total)
    with col_3:
        val3 = len(df[df['class'] == 'Overweight'])
        plot_gauge(val3, "#ff8000", "", "Overweight", total)   
    with col_4:
        val4 = len(df[df['class'] == 'Obesity'])
        plot_gauge(val4, "#ff0000", "", "Obesity", total)   
    st.title('apani')

with top_right_col:
    st.markdown('<center>Numerical Attribute Distribution</center>', unsafe_allow_html=True) 
    st.divider()
    # select the attributes
    attribute_selected = st.selectbox(
        'Attribute to preview',
        ('Age', 'Height'),
        index=0,
    )
    st.divider()
    
    grouped_data = []
    group_labels = []
    for group in df['class'].unique():
        filtered_data = df[df['class'] == group][attribute_selected.lower()].to_list()
        grouped_data.append(filtered_data)
        group_labels.append(group)

    distplot(grouped_data, group_labels, title=f"{attribute_selected} by Class", bin_size=1.25)


st.title('Apalah ya yang mau di coba coba kok pusing banget')