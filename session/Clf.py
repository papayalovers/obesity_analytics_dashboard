import streamlit as st
import pandas as pd
import json
import joblib
import plotly.graph_objects as go

model = joblib.load('model/optuna_study.pkl')
mean_encoding_path = 'dataset/mean_encoding_90.txt'

def preprocess_user_input(user_input_df, mean_dict_path, feature_order):

    with open(mean_dict_path, "r") as f:
        mean_dict = json.load(f)

    df = user_input_df.copy()

    yn_columns = ['overweight_obese_family', 'consumption_of_fast_food', 'smoking', 'calculation_of_calorie_intake']
    for col in yn_columns:
        if col in df.columns:
            df[col] = df[col].map({'Yes': 1, 'No': 0})

    if 'food_intake_between_meals' in df.columns:
        df['food_intake_between_meals'] = df['food_intake_between_meals'].map({
            'Rarely': 0, 'Sometimes': 1, 'Usually': 2, 'Always': 3
        })

    for col, encoding in mean_dict.items():
        if col in df.columns:
            df[col] = df[col].map(encoding).fillna(0)

    df["sex_Male"] = 1 if df["sex"].iloc[0] == "Male" else 0

    liquid_value = df["liquid_intake_daily"].iloc[0]
    df["liquid_intake_daily_<1 liter"] = 1 if liquid_value == "<1 liter" else 0
    df["liquid_intake_daily_>2 liter"] = 1 if liquid_value == ">2 liters" else 0

    tech_value = df["schedule_dedicated_to_technology"].iloc[0]
    df["schedule_dedicated_to_technology_3-5 hours"] = 1 if tech_value == "3-5 hours" else 0
    df["schedule_dedicated_to_technology_>5 hours"] = 1 if tech_value == ">5 hours" else 0

    age = df["age"].iloc[0]
    df["age_grouped_26-45"] = 1 if 26 <= age <= 45 else 0
    df["age_grouped_46-65"] = 1 if 46 <= age <= 65 else 0

    drop_cols = [
        "sex", "liquid_intake_daily", "schedule_dedicated_to_technology", "age"
    ]
    df.drop(columns=drop_cols, inplace=True)

    df = df.reindex(columns=feature_order, fill_value=0)
    return df

def main():
    st.markdown('<center><h4>Obesity Risk Classification App</h4></center>', unsafe_allow_html=True)

    left_col, right_col = st.columns(2)

    with left_col:
        
        sex = st.selectbox(
            'Gender',
            ('Male', 'Female'),
            index=None,  
            placeholder='Select your gender'  
        )
        
        age = st.number_input(
            'Age', 
            min_value=1, 
            max_value=120, 
            value=1, 
            help="Enter your age"
        )

        height = st.number_input(
            'Height (cm)', 
            min_value=1, 
            max_value=250, 
            value=1, 
            help="Enter your height in cm"
        )
        
        overweight_obese_family = st.selectbox(
            'Overweight/Obese Family History',
            ['Yes', 'No'],
            index=None,
            placeholder='Is there a history of overweight/obesity in your family?'
        )
        
        consumption_of_fast_food = st.selectbox(
            'Consumption of Fast Food',
            ['Yes', 'No'],
            index=None,
            placeholder='Do you consume fast food regularly?'
        )

        frequency_of_consuming_vegetables = st.selectbox(
            'Frequency of Consuming Vegetables',
            ['Sometimes', 'Always', 'Rarely'],
            index=None,
            placeholder='How often do you consume vegetables?'
        )
        
        number_of_main_meals_daily = st.selectbox(
            'Number of Main Meals Daily',
            ['1-2', '3', '>3'],
            index=None,
            placeholder='How many main meals do you have per day?'
        )

    with right_col:
        food_intake_between_meals = st.selectbox(
            'Food Intake Between Meals',
            ['Sometimes', 'Usually', 'Rarely', 'Always'],
            index=None,
            placeholder='How often do you eat between meals?'
        )
        
        smoking = st.selectbox(
            'Smoking',
            ['Yes', 'No'],
            index=None,
            placeholder='Do you smoke?'
        )
        
        liquid_intake_daily = st.selectbox(
            'Liquid Intake Daily',
            ['<1 liter', '1-2 liters', '>2 liters'],
            index=None,
            placeholder='How much liquid do you consume daily?'
        )
        
        calculation_of_calorie_intake = st.selectbox(
            'Calculation of Calorie Intake',
            ['Yes', 'No'],
            index=None,
            placeholder='Do you track your calorie intake?'
        )
        
        physical_exercise = st.selectbox(
            'Physical Exercise',
            ['No Activity', '1-2 days a week', '3-4 days a week', '5-6 days a week', '6 or more days a week'],
            index=None,
            placeholder='How often do you exercise per week?'
        )
        
        schedule_dedicated_to_technology = st.selectbox(
            'Schedule Dedicated to Technology',
            ['0-2 hours', '3-5 hours', '>5 hours'],
            index=None,
            placeholder='How much time do you dedicate to technology daily?'
        )
        
        type_of_transportation_used = st.selectbox(
            'Type of Transportation Used',
            ['Walking', 'Bicycle', 'Motorbike', 'Public Transportation', 'Automobile'],
            index=None,
            placeholder='What type of transportation do you use?'
        )

    st.info('''
    *Note: The data you enter in this classification tool is not stored or recorded. 
    It is solely used for informational purposes to help assess the likelihood of obesity based on the input provided. 
    This result should not be considered a medical diagnosis. For a comprehensive health evaluation, please consult a qualified healthcare professional.*
    ''')

    user_input = {
        'sex': sex,
        'age': age,
        'height': height,
        'overweight_obese_family': overweight_obese_family,
        'consumption_of_fast_food': consumption_of_fast_food,
        'frequency_of_consuming_vegetables': frequency_of_consuming_vegetables,
        'number_of_main_meals_daily': number_of_main_meals_daily,
        'food_intake_between_meals': food_intake_between_meals,
        'smoking': smoking,
        'liquid_intake_daily': liquid_intake_daily,
        'calculation_of_calorie_intake': calculation_of_calorie_intake,
        'physical_excercise': physical_exercise,
        'schedule_dedicated_to_technology': schedule_dedicated_to_technology,
        'type_of_transportation_used': type_of_transportation_used
    }

    user_input_df = pd.DataFrame([user_input])
    st.markdown("### User Input Preview:")
    st.dataframe(user_input_df)

    if st.button('Classify'):
        if user_input_df.isnull().values.any():
            st.error('Please input your data information first!')
        else:
            feature_order = [
                'age', 'height', 'overweight_obese_family', 'consumption_of_fast_food',
                'frequency_of_consuming_vegetables', 'number_of_main_meals_daily',
                'food_intake_between_meals', 'smoking', 'calculation_of_calorie_intake',
                'physical_excercise', 'type_of_transportation_used', 'sex_Male',
                'liquid_intake_daily_<1 liter', 'liquid_intake_daily_>2 liter',
                'schedule_dedicated_to_technology_3-5 hours',
                'schedule_dedicated_to_technology_>5 hours', 'age_grouped_26-45',
                'age_grouped_46-65'
            ]

            class_value = {
                0:'Underweight', 
                1:'Normal',  
                2:'Overweight', 
                3:'Obesity' ,
            }

            user_input_df.columns = user_input_df.columns.str.lower().str.replace(' ', '_')
            processed_input = preprocess_user_input(user_input_df, mean_encoding_path, feature_order)
            proba = model.predict_proba(processed_input)[0]
            prediction = proba.argmax()
            # hasil klasifikasi
            st.markdown(f"""
            <div style='
                background-color:#f0f2f6;
                padding: 1.5rem;
                border-radius: 12px;
                text-align: center;
                font-size: 1.2rem;
                color: #333;
                font-weight: bold;'>
                Your Classification: <span style='color: #0072B5;'>{class_value[prediction]}</span><br>
            </div>
            """, unsafe_allow_html=True)

            # distribusi probabilitas prediksi
            labels = list(class_value.values())
            colors = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072'] 

            fig = go.Figure(
                data=[go.Pie(
                    labels=labels,
                    values=proba,
                    marker=dict(colors=colors),
                    hole=0.3,
                    textinfo='label+percent',
                    hoverinfo='label+value',
                    sort=False
                )]
            )

            fig.update_layout(
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=50, b=0, l=0, r=0)
            )

            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
