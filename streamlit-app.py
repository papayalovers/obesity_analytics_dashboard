import streamlit as st
from streamlit_option_menu import option_menu
from pages import clf, Dashboard, hist

# Membaca halaman-halaman yang ada
def load_page(page_name):
    if page_name == "Dashboard":
        # Halaman dashboard
        Dashboard.main()
    elif page_name == "Klasifikasi":
        # Halaman klasifikasi
        clf.main()  # Menjalankan fungsi utama di clf.py

def main():
    st.set_page_config(page_title='Obesity Classification Dashboard', page_icon=':bar_chart:', layout='wide')

    # Menambahkan CSS untuk memberikan padding-top pada sidebar
    st.markdown("""
    <style>
    .css-1d391kg {
        padding-top: 100px !important;
    }

    .css-1r9o0kd {
        padding-top: 100px !important;
    }

    .sidebar .sidebar-content {
        padding-top: 100px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar menu
    with st.sidebar:
        page = option_menu("Main Menu", ["Dashboard", "Klasifikasi"], icons=["house", "search"], menu_icon="cast", default_index=0)

    load_page(page)

if __name__ == "__main__":
    main()
