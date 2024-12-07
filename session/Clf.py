import streamlit as st
import pandas as pd

def main():
    # Create two columns for input
    left_col, right_col = st.columns(2)

    with left_col:
        # Input for data in the left column
        sex = st.selectbox(
            'Gender',
            ('Male', 'Female'),
            index=None,  # No default selection
            placeholder='Select your gender'  # Clearer placeholder
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
        # Input for data in the right column
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

    # Organize user input into a dictionary
    user_input = {
        'Gender': sex,
        'Age': age,
        'Height (cm)': height,
        'Overweight/Obese Family History': overweight_obese_family,
        'Consumption of Fast Food': consumption_of_fast_food,
        'Frequency of Consuming Vegetables': frequency_of_consuming_vegetables,
        'Number of Main Meals Daily': number_of_main_meals_daily,
        'Food Intake Between Meals': food_intake_between_meals,
        'Smoking': smoking,
        'Liquid Intake Daily': liquid_intake_daily,
        'Calculation of Calorie Intake': calculation_of_calorie_intake,
        'Physical Exercise': physical_exercise,
        'Schedule Dedicated to Technology': schedule_dedicated_to_technology,
        'Type of Transportation Used': type_of_transportation_used
    }

    # Convert the dictionary into a DataFrame
    user_input_df = pd.DataFrame([user_input])

    # Display the DataFrame containing the user's input
    st.markdown("User Input Data:")
    st.dataframe(user_input_df, use_container_width=True)


    do_pred = st.button('Predict')

    if do_pred:
        st.markdown('Sabar yah masih belum')
if __name__ == "__main__":
    main()
