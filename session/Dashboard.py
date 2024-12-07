import streamlit as st
import pandas as pd
from stream_src.utils import *

def main():
    df = pd.read_csv('dataset/obesity.csv')
    # map value agar plot ditampilkan sesuai
    df['number_of_main_meals_daily'] = df['number_of_main_meals_daily'].map(
        {
            '1-2' : 'Between 1 and 2 times',
            '3' : '3 Times',
            '>3' : 'More than 3 times'
        }
    )
    # data preview
    with st.expander('Data Preview'):
        st.dataframe(df, use_container_width=True)

    st.markdown('<center><h3>Class Proportions Overview</h3></center>', unsafe_allow_html=True)
    st.divider()

    ##################################################################################
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
    group_by_class = st.checkbox('Group By Class', value=True)
    # Checkbox for grouping by class
    

    with top_left_col:
        cat_slected = st.selectbox(
            'Select Attribute Categorical to Preview',
            ('Sex', 'Overweight Obese Family', 'Consumption of Fast Food', 'Frequency of Consuming Vegetables',
             'Number of Main Meals Daily', 'Food Intake Between Meals', 'Smoking', 'Liquid Intake Daily',
             'Calculation of Calorie Intake', 'Physical Exercise', 'Schedule Dedicated to Technology', 'Type of Transportation Used'),
            index=0,
        )
        x = cat_slected.lower().replace(' ', '_')

        # Use hue option based on checkbox state
        hue = 'class' if group_by_class else None

        # menampilkan barplot
        barplot(data=df, x=x, hue=hue, title=cat_slected)

    with top_right_col:
        attribute_selected = st.selectbox(
            'Attribute to preview',
            ('Age', 'Height'),
            index=0,
        )

        # Process the distplot based on grouping checkbox
        if group_by_class:
            # Grouping data based on 'class' column
            grouped_data = []
            group_labels = []
            for group in df['class'].unique():
                filtered_data = df[df['class'] == group][attribute_selected.lower()].to_list()
                grouped_data.append(filtered_data)
                group_labels.append(group)
            distplot(grouped_data, group_labels, title=attribute_selected)
        else:
            # Display without grouping
            distplot([df[attribute_selected.lower()].to_list()], ['All Data'], title=attribute_selected)

    ##################################################################################
    st.divider()
    st.markdown('<center><h3>Risk of Obesity</h3></center>', unsafe_allow_html=True)
    
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
