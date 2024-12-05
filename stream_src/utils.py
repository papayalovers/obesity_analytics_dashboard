import plotly.graph_objects as go
import streamlit as st
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt 
import random 
import plotly.express as px

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
                "font": {
                    "size": 20,  # Ukuran font
                    "color": indicator_color  # Warna font sesuai dengan warna indikator
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
        width=800, height=500
    )
    st.plotly_chart(fig, use_container_width=True)


def barplot(data, x, title, hue=None):
    # Jika hue disertakan, lakukan pemisahan data berdasarkan hue
    if hue:
        hue_values = data[hue].unique()  # Ambil semua nilai unik dari kolom hue
        fig = go.Figure()

        # Menggunakan palet warna dari Plotly
        colors = px.colors.qualitative.Pastel  # Pilihan warna soft

        for hue_value in hue_values:
            # Filter data berdasarkan hue_value
            filtered_data = data[data[hue] == hue_value]
            # Hitung frekuensi untuk setiap kategori pada x
            count_data = filtered_data[x].value_counts().reset_index()
            count_data.columns = [x, 'count']
            
            # Pilih warna secara acak dari palet Plotly setiap kali
            color = random.choice(colors)  # Pilih warna secara acak dari Set2

            # Tambahkan bar plot untuk setiap nilai hue_value
            fig.add_trace(go.Bar(
                name=str(hue_value),
                x=count_data[x],
                y=count_data['count'],
                text=count_data['count'],  # Menampilkan label di atas bar
                textposition='outside',  # Posisi text di luar bar
                textfont=dict(size=12),  # Ukuran font
                marker_color=color  # Warna yang dipilih secara acak
            ))

        # Mengatur layout untuk barmode dan tampilan
        fig.update_layout(
            barmode='group',  # Menyusun batang secara berdampingan
            xaxis_title=title.capitalize(),
            title={'text': f'{title.capitalize()} Distribution by {hue.capitalize()}' if hue else f'{x.capitalize()} Distribution',
                   'x': 0.5, 'xanchor': 'center', 'font': {'size': 18}},
            width=800, height=500
        )

    else:
        # Jika tidak ada hue, hanya tampilkan satu barplot berdasarkan x
        count_data = data[x].value_counts().reset_index()
        count_data.columns = [x, 'count']
        fig = go.Figure([go.Bar(
            x=count_data[x],
            y=count_data['count'],
            text=count_data['count'],  # Menampilkan label di atas bar
            textposition='outside',  # Posisi text di luar bar
            textfont=dict(size=12)  # Ukuran font
        )])

        # Mengatur layout untuk barplot tanpa hue
        fig.update_layout(
            xaxis_title=title.capitalize(),
            title={'text': f'{title.capitalize()} Distribution', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 18}},
            width=800, height=500
        )

    # Menampilkan grafik menggunakan Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Fungsi untuk menampilkan Gauge Chart dengan kategori dan persentase tertinggi
def plot_gauge2(data, column, title):
    # Menghitung persentase individu yang memiliki risiko obesitas berdasarkan kategori
    obesity_data = data[data['class'] == 'Obesity']
    value_counts = obesity_data[column].value_counts(dropna=False)
    
    # Menghitung persentase
    total = len(obesity_data)
    percentages = (value_counts / total) * 100

    # Ambil kategori dengan persentase tertinggi untuk ditampilkan pada gauge
    max_category = percentages.idxmax()
    max_percentage = percentages.max()

    # Menyiapkan Gauge Chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=max_percentage,
        delta={'reference': 50},  # Nilai referensi untuk perbandingan
        title={'text': f"{title} - {max_category}", 'font': {'size': 18}},
        gauge={
            'axis': {'range': [None, 100]},  # Rentang antara 0 hingga 100
            'bar': {'color': "lightblue"},  # Warna bar
            'steps': [
                {'range': [0, 33], 'color': "lightgreen"},
                {'range': [33, 66], 'color': "yellow"},
                {'range': [66, 100], 'color': "red"}
            ]
        },
        number={'font': {'size': 24}, 'suffix': "%"},  # Menampilkan persentase
    ))
    # Menyesuaikan ukuran plot untuk tampilan yang lebih proporsional
    fig.update_layout(
        width=400,  # Menyesuaikan lebar
        height=400,  # Menyesuaikan tinggi
        margin=dict(t=40, b=40, l=40, r=40)  # Margin untuk memastikan judul tidak terpotong
    )
    # Menampilkan chart di Streamlit
    st.plotly_chart(fig, use_container_width=True)