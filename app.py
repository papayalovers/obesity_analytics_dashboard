import streamlit as st
from session import Clf, Dashboard, Hist
import base64


# Fungsi untuk memuat halaman
def load_page(page_name):
    if page_name == "Dashboard":
        Dashboard.main()
    elif page_name == "Klasifikasi":
        Clf.main()
    elif page_name == "History":
        st.write("Coming Soon")

# konfigurasi halaman
st.set_page_config(
    page_title="Obesity Classification Dashboard", 
    page_icon=":bar_chart:", 
    layout="wide"
)
st.markdown('<center><h2>Obesity Analytics and Classification</h2></center>', unsafe_allow_html=True)

# Fungsi untuk mengonversi gambar lokal ke base64
def img_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

image_path = 'img/bg.jpg'  

# konversi gambar ke base64
image_base64 = img_to_base64(image_path)

def main():
    # background image
    background_image = f"""
    <style>
    /* Set Background Image untuk seluruh aplikasi */
    .stApp {{
        position: relative;
        background-image: url('data:image/jpeg;base64,{image_base64}');
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        height: 100vh;
    }}

    /* Tambahkan overlay gelap dengan transparansi */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.7);  /* Ubah angka 0.7 untuk mengatur kegelapan overlay */
        z-index: -1;
    }}
    </style>
    """

    st.markdown(background_image, unsafe_allow_html=True)

    # tabs untuk navigasi
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Klasifikasi", "Model History"])

    with tab1:
        load_page("Dashboard")
    
    with tab2:
        load_page("Klasifikasi")
    
    with tab3:
        load_page("History")

if __name__ == "__main__":
    main()
