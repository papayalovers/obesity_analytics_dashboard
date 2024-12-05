import streamlit as st
import pandas as pd

# Fungsi encoding yang sesuai dengan data training
def encoder_to_digit(dataset, columns_to_encode, ohe_columns):
    """
    Fungsi ini memastikan bahwa kolom yang dihasilkan sesuai dengan kolom data training.
    
    dataset: DataFrame input pengguna.
    columns_to_encode: Daftar kolom yang akan di-encode (categorical columns).
    ohe_columns: Kolom-kolom yang sudah di-encode dengan One-Hot Encoding dari training data.
    """
    # Membuat salinan dataset
    dataset_copy = dataset.copy()

    # Encoding untuk kolom kategori
    for col in columns_to_encode:
        if col in ['sex', 'age_grouped', 'schedule_dedicated_to_technology', 'liquid_intake_daily']:
            # Gunakan pd.get_dummies untuk menangani kolom kategorikal dengan lebih dari dua kategori
            dataset_copy = pd.get_dummies(dataset_copy, columns=[col], drop_first=True, dtype=int)
        elif col in ['overweight_obese_family', 'consumption_of_fast_food', 'smoking', 'calculation_of_calorie_intake']:
            # Map kategori Yes/No ke 1/0
            dataset_copy[col] = dataset_copy[col].map({
                'Yes': 1,
                'No': 0
            })
        elif col == 'food_intake_between_meals':
            # Mapping kategori 'Rarely', 'Sometimes', 'Usually', 'Always' ke angka
            dataset_copy[col] = dataset_copy[col].map({
                'Rarely': 0,
                'Sometimes': 1,
                'Usually': 2,
                'Always': 3
            })
        elif col == 'class':
            # Mapping label kelas ke angka
            dataset_copy[col] = dataset_copy[col].map({
                'Underweight': 0,
                'Normal': 1,
                'Overweight': 2,
                'Obesity': 3
            })

    # Memastikan kolom dummy dari OHE yang hilang ditambahkan
    for col in ohe_columns:
        if col not in dataset_copy.columns:
            dataset_copy[col] = 0  # Tambahkan kolom yang hilang dengan nilai 0

    return dataset_copy

# Fungsi untuk input dari pengguna
def user_input():
    # Input untuk sex
    sex = st.radio("Select Sex", ('Male', 'Female'))

    # Input untuk age_grouped
    age_group = st.selectbox("Select Age Group", ('<30', '31-40', '41-50', '51-60', '60+'))

    # Input untuk schedule dedicated to technology
    tech_schedule = st.selectbox("Schedule Dedicated to Technology", ('0-3 hours', '3-5 hours', '>5 hours'))

    # Input untuk liquid intake daily
    liquid_intake = st.radio("Liquid Intake (Daily)", ('<1 liter', '1-2 liters', '>2 liters'))

    # Input untuk food intake between meals
    food_intake = st.selectbox("Food Intake Between Meals", ('Rarely', 'Sometimes', 'Usually', 'Always'))

    # Mengumpulkan input dalam dictionary
    user_data = {
        'sex': sex,
        'age_grouped': age_group,
        'schedule_dedicated_to_technology': tech_schedule,
        'liquid_intake_daily': liquid_intake,
        'food_intake_between_meals': food_intake
    }

    return pd.DataFrame(user_data, index=[0])

# Membaca data dan menampilkan input pengguna setelah encoding
def main():
    # Mengambil input dari pengguna
    user_df = user_input()

    # Kolom-kolom yang perlu di-encode
    columns_to_encode = [
        'sex', 'age_grouped', 'schedule_dedicated_to_technology', 'liquid_intake_daily', 
        'food_intake_between_meals', 'overweight_obese_family', 'consumption_of_fast_food', 
        'smoking', 'calculation_of_calorie_intake', 'class'
    ]

    # Kolom-kolom yang sudah ada setelah OHE dari data training
    ohe_columns = [
        'sex_Male', 'age_grouped_26-45', 'age_grouped_46-65', 
        'schedule_dedicated_to_technology_3-5 hours', 'schedule_dedicated_to_technology_>5 hours', 
        'liquid_intake_daily_<1 liter', 'liquid_intake_daily_>2 liters'
    ]

    # Melakukan encoding pada input pengguna
    user_encoded = encoder_to_digit(user_df, columns_to_encode, ohe_columns)

    # Menampilkan data setelah encoding
    st.write("Encoded User Data:")
    st.write(user_encoded)

if __name__ == "__main__":
    main()
