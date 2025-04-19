import streamlit as st
from session import Clf, Dashboard, Hist

# konfigurasi halaman
st.set_page_config(
    page_title="Obesity Classification Dashboard", 
    page_icon="img/icon.png", 
    layout="wide"
)

# bikin status login pertama kali
if 'agreed' not in st.session_state:
    st.session_state.agreed = False

# fungsi utama halaman dengan tabs
def main():
    st.markdown('<center><h2>Obesity Analytics and Classification</h2></center>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Dashboard", "Obesity Classification", "Model Training History"])

    with tab1:
        load_page("Dashboard")
    
    with tab2:
        load_page("Klasifikasi")
    
    with tab3:
        load_page("History")

# fungsi untuk memuat halaman
def load_page(page_name):
    if page_name == "Dashboard":
        Dashboard.main()
    elif page_name == "Klasifikasi":
        Clf.main()
    elif page_name == "History":
        Hist.main()

# disclaimer
def show_disclaimer():
    st.markdown("""
    <div style="border: 2px solid #d3d3d3; padding: 20px; border-radius: 10px; background-color: #000000; text-align: center;">
        <h4 style="color:white;">📌 Disclaimer & Acknowledgement</h4>
        <p style="font-size:16px; color:white;">
            Please note that the results presented in this dashboard are derived based on the dataset used.<br>
            <a href="https://www.kaggle.com/datasets/suleymansulak/obesity-dataset" target="_blank" style="color:#00ffff;">Click here to view the dataset</a>.<br><br>
            These results are not intended to be generalized beyond the scope of the original data.<br>
            Special thanks to <strong>Niğmet KÖKLÜ</strong><sup>1</sup> and <strong>Süleyman Alpaslan SULAK</strong><sup>2</sup> for providing the dataset used in this research.<br>
            Read the original research by Niğmet KÖKLÜ <a href="https://doi.org/10.33484/sinopfbd.1445215" target="_blank" style="color:#00ffff;">(DOI: 10.33484/sinopfbd.1445215)</a>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)  # spasi
    
    cols = st.columns(9)  
    
    with cols[4]: 
        center_button = st.button("Continue to Dashboard")
        if center_button:
            st.session_state.agreed = True
            st.rerun()

# app logic
if __name__ == "__main__":
    if not st.session_state.agreed:
        show_disclaimer()
    else:
        main()
