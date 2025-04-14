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

    ########################### DISTRIBUSI MASING MASING KELAS ##############################
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
    
    ########################################################################################################
    top_left_col, top_right_col = st.columns((2, 1))
    ########################## DISTRIBUSI ATRIBUT KATEGORIK HUE / NO HUE ####################################
    # checkbox untuk grouping by class
    group_by_class = st.checkbox('Group By Class', value=True)    
    # view di kolom kiri
    with top_left_col:
        cat_slected = st.selectbox(
            'Select Attribute Categorical to Preview',
            ('Sex', 
             'Overweight Obese Family', 
             'Consumption of Fast Food', 
             'Frequency of Consuming Vegetables',
             'Number of Main Meals Daily', 
             'Food Intake Between Meals', 
             'Smoking', 
             'Liquid Intake Daily',
             'Calculation of Calorie Intake', 
             'Physical Exercise', 
             'Schedule Dedicated to Technology', 
             'Type of Transportation Used'),
            index=0,
        )
        x = cat_slected.lower().replace(' ', '_')

        hue = 'class' if group_by_class else None

        # menampilkan barplot
        barplot(data=df, x=x, hue=hue, title=cat_slected)

    ########################## DISTRIBUSI ATRIBUT NUMERIK HUE / NO HUE ####################################
    with top_right_col:
        attribute_selected = st.selectbox(
            'Attribute to preview',
            ('Age', 'Height'),
            index=0,
        )

        if group_by_class:
            # grouping data berdasarkan class
            grouped_data = []
            group_labels = []
            for group in df['class'].unique():
                filtered_data = df[df['class'] == group][attribute_selected.lower()].to_list()
                grouped_data.append(filtered_data)
                group_labels.append(group)
            distplot(grouped_data, group_labels, title=attribute_selected)
        else:
            # tampilkan tanpa grouping
            distplot([df[attribute_selected.lower()].to_list()], ['All Data'], title=attribute_selected)

    ###################### TRENDLINE KASUS OBESITAS BERDASARKAN USIA ################################
    st.divider()
    plot_obesity_trend_by_age(df)
    st.info('*Note: This chart shows the number of obesity cases by age—the higher the line, the more cases of obesity.*')

    #############################################################################################
    st.divider()
    bottom_left_col, bottom_right_col = st.columns((2, 2))
    ###################### PROPORSI ORANG  YANG TERKENA OBESITAS ################################
    with bottom_left_col:
        probability_barplot(df, 'Obesity')  
    ###################### RISIKO SESEORANG TERKENA OBESITAS ####################################
    with bottom_right_col:
        probability_barplot(df, None)  

    ##################### HIGHLIGHT (NOT DONE YET) #####################################
    ####################################################################################
    st.divider()

    st.markdown('<center><h4>Lowest Obesity Risk Conditions</h3></center>', unsafe_allow_html=True)
    cols = st.columns(3)
    indicators = low_prob_indicator(df)

    for idx, (_,_,_, fig) in enumerate(indicators):
        with cols[idx]:
            st.plotly_chart(fig, use_container_width=True)
            st.divider()
    ####################################################################################
    ####################################################################################
if __name__ == "__main__":
    main()
