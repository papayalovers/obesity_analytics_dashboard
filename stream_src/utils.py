import plotly.graph_objects as go
import streamlit as st
import plotly.figure_factory as ff
import random 
import plotly.express as px

###################
# GAUGEPLOT       #
###################
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
                "font": {
                    "size": 20,  # Ukuran font
                    "color": indicator_color,  # Warna font sesuai dengan warna indikator
                    "weight" : "bold"
                }
            },
            gauge={
                "axis": {
                    "range": [0, max_bound],  # Rentang gauge
                    "tickwidth": 1,  # Ukuran tick pada sumbu
                },
                "bar": {"color": indicator_color},  # Warna bar sesuai indikator
            },
            title={
                "text": indicator_title,  # Judul indikator
                "font": {"size": 18},
            },
        )
    )

    fig.update_layout(
        height=150,  # Tinggi gauge
        margin=dict(l=10, r=10, t=50, b=10, pad=8),  # Margin untuk ukuran maksimal
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)' 
    )

    st.plotly_chart(fig, use_container_width=True)
###################
# DISPLOT         #
###################
def distplot(hist_data, group_labels, title):
    fig = ff.create_distplot(hist_data, group_labels,show_rug=False)

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
        width=600, height=500,
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title=title.capitalize(),
    )
    st.plotly_chart(fig, use_container_width=True)
###################
# BARPLOT         #
###################
def barplot(data, x, title, hue=None):
    # jika hue = True, lakukan pemisahan data berdasarkan hue
    if hue:
        hue_values = data[hue].unique()  # ambil semua nilai unik dari kolom hue
        fig = go.Figure()

        colors = px.colors.qualitative.Pastel  # pilihan warna soft

        for hue_value in hue_values:
            # filter data berdasarkan hue_value
            filtered_data = data[data[hue] == hue_value]
            count_data = filtered_data[x].value_counts().reset_index()
            count_data.columns = [x, 'count']
            
            color = random.choice(colors)  # pilih warna secara acak dari Set2

            fig.add_trace(go.Bar(
                name=str(hue_value),
                x=count_data[x],
                y=count_data['count'],
                text=count_data['count'], 
                textposition='outside', 
                textfont=dict(size=12),
                marker_color=color 
            ))

        # layout untuk barmode dan tampilan
        fig.update_layout(
            barmode='group',  
            xaxis_title=title.capitalize(),
            title={
                'text': f'{title.capitalize()} Distribution by {hue.capitalize()}' if hue else f'{x.capitalize()} Distribution',
                'x': 0.5, 'xanchor': 'center', 'font': {'size': 18}},
            width=700, 
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',  
            paper_bgcolor='rgba(0,0,0,0)' 
        )

    else:
        count_data = data[x].value_counts().reset_index()
        count_data.columns = [x, 'count']
        fig = go.Figure([go.Bar(
            x=count_data[x],
            y=count_data['count'],
            text=count_data['count'], 
            textposition='outside',  
            textfont=dict(size=12) 
        )])

        # layout untuk barplot tanpa hue
        fig.update_layout(
            xaxis_title=title.capitalize(),
            title={
                'text': f'{title.capitalize()} Distribution', 
                'x': 0.5, 
                'xanchor': 'center', 
                'font': {'size': 18}
            },
            width=700, 
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',  
            paper_bgcolor='rgba(0,0,0,0)' 
        )

    st.plotly_chart(fig, use_container_width=True)
###################
# GAUGEPLOT2      #
###################
def plot_gauge2(data, column, title):
    # menghitung persentase individu yang memiliki risiko obesitas berdasarkan kategori
    obesity_data = data[data['class'] == 'Obesity']
    value_counts = obesity_data[column].value_counts(dropna=False)
    
    # menghitung persentase
    total = len(obesity_data)
    percentages = (value_counts / total) * 100

    # ambil kategori dengan persentase tertinggi untuk ditampilkan pada gauge
    max_category = percentages.idxmax()
    max_percentage = percentages.max()

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=max_percentage,
        delta={'reference': 50},  
        title={'text': f"{title} - {max_category}", 'font': {'size': 14}},
        gauge={
            'axis': {'range': [None, 100]}, 
            'bar': {'color': "lightblue"},  
            'steps': [
                {'range': [0, 33], 'color': "lightgreen"},
                {'range': [33, 66], 'color': "yellow"},
                {'range': [66, 100], 'color': "red"}
            ]
        },
        number={'font': {'size': 24}, 'suffix': "%"},  # menampilkan persentase
    ))

    fig.update_layout(
        width=400,  
        height=200,  
        margin=dict(t=40, b=40, l=40, r=40),
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)' 
    )
    st.plotly_chart(fig, use_container_width=True)