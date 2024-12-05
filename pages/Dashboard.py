import streamlit as st
import pandas as pd
from stream_src.utils import *  # Pastikan 'plot_gauge' dan 'distplot' terdefinisi di sini
from streamlit_elements import elements, mui, html
import numpy as np

########################
#   PAGE SETUP        #
########################

def main():
    st.markdown("_Prototype v0.4.1_")
    df = pd.read_csv('dataset/obesity.csv')

    # Data preview (dapat diaktifkan dengan menghilangkan komentar)
    with st.expander('Data Preview'):
        df = pd.read_csv('dataset/obesity.csv')
        st.dataframe(df, use_container_width=True)

    ##################################################################################   
    st.markdown('<center><h3>Class Proportions Overview</h3></center>', unsafe_allow_html=True)
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
    st.divider()

    ##################################################################################    
    top_left_col, top_right_col = st.columns((2, 1))
    with top_left_col:
        cat_slected = st.selectbox(
            'Select Attribute Categorical to Preview',
            ('Sex', 'Overweight Obese Family', 'Consumption of Fast Food','Frequency of Consuming Vegetables',
             'Number of Main Meals Daily','Food Intake Between Meals', 'Smoking','Liquid Intake Daily','Calculation of Calorie Intake',
             'Physical Exercise','Schedule Dedicated to Technology','Type of Transportation Used'),
            index=0,
        )
        x = cat_slected.lower().replace(' ','_')

        hue_option = st.checkbox('Use Hue (Class)', value=True)  # Mengaktifkan hue secara default

        # Jika hue_option dipilih, menggunakan kolom 'class' untuk warna
        if hue_option:
            hue = 'class'  # Kolom 'class' untuk hue
        else:
            hue = None  # Tidak ada hue jika tidak dicentang

        # Menampilkan barplot
        barplot(data=df, x=x, hue=hue, title=cat_slected)

    with top_right_col:
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

    ##################################################################################    
    # Judul dan deskripsi
    st.divider()
    st.markdown('<center><h3>Risk of Obesity</h3></center>', unsafe_allow_html=True)
    # Menampilkan Gauge Chart untuk masing-masing kategori
    col_1, col_2, col_3, col_4 = st.columns(4)

    with col_1:
        plot_gauge2(df, 'frequency_of_consuming_vegetables', 'Frekuensi Konsumsi Sayuran')

    with col_2:
        plot_gauge2(df, 'number_of_main_meals_daily', 'Jumlah Makan Utama Sehari')

    with col_3:
        plot_gauge2(df, 'physical_exercise', 'Aktivitas Latihan Fisik')

    with col_4:
        plot_gauge2(df, 'type_of_transportation_used', 'Jenis Transportasi')


if __name__ == "__main__":
    main()
