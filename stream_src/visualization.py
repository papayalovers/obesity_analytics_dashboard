import plotly.express as px
import plotly.graph_objects as go
import random
import streamlit as st
import plotly.figure_factory as ff
import scipy.stats as stats
import numpy as np

###################
# GAUGEPLOT       #
###################
@st.cache_data
def plot_gauge(
    indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 20,
                'font.color': indicator_color,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={
                "text": indicator_title,
                "font": {"size": 14},
            },
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        height=115,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
    )
    st.plotly_chart(fig, use_container_width=True)


###################
# DISPLOT        #
###################
@st.cache_resource
def distplot(hist_data, group_labels, title, bin_size):

    fig = ff.create_distplot(hist_data, group_labels,
                         bin_size=bin_size, show_rug=False)

    # add title
    fig.update_layout(
        legend=dict(
            x=0.65,  # posisi x dalam grafik (0 - 1)
            y=0.95,  # posisi y dalam grafik (0 - 1)
            
        ),
        title={
            'text': title,
            'font' : {'size': 18},
            'x' : 0.5,
            'xanchor' : 'center',
        },
        width=500, height=400
    )
    st.plotly_chart(fig, use_container_width=True)
