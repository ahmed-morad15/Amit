import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ------------------- Set Configuration -------------------
st.set_page_config(
    page_title="Boston Housing Prediction",
    page_icon="🏠",
    layout="wide"  
)

# ------------------- Load Model & Scaler -------------------

model = pickle.load(open("C:/DEPI/Amit/Src/ML/Boston-Housing-App/models/Boston_Housing_Best_model.pkl", "rb"))
scaler = pickle.load(open("C:/DEPI/Amit/Src/ML/Boston-Housing-App/models/scaler.pkl", "rb"))

# ------------------- Prediction Page -------------------
def prediction_page():
    st.markdown("<h1 style='text-align:center; color:#2E8B57;'>🏠 Boston Housing Price Prediction</h1>", unsafe_allow_html=True)
    
    # Center the form using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("prediction_form"):
            st.markdown("<h3 style='text-align:center; color:#1F3B4D;'>📋 Enter Housing Features</h3>", unsafe_allow_html=True)

            # ---------------- Section 1 ----------------
            st.markdown("<div style='background-color:#f0f2f6; padding:10px; border-radius:8px;'>"
                        "<h4 style='text-align:center;'>Neighborhood & Crime</h4></div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                crim = st.number_input("Crime Rate (crim)", 0.0, 100.0, 0.1)
                zn = st.number_input("Residential Land Zone (zn)", 0.0, 100.0, 0.0)
                indus = st.number_input("Non-retail Business Acres (indus)", 0.0, 30.0, 5.0)
            with col2:
                chas = st.selectbox("Charles River (chas)", [0,1])
                nox = st.number_input("Nitric Oxide (nox)", 0.0, 1.0, 0.5)
                rm = st.number_input("Average Rooms (rm)", 1.0, 10.0, 6.0)

            # ---------------- Section 2 ----------------
            st.markdown("<div style='background-color:#f0f2f6; padding:10px; border-radius:8px;'>"
                        "<h4 style='text-align:center;'>Property & Environment</h4></div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Old Houses % (age)", 0.0, 100.0, 50.0)
                dis = st.number_input("Distance to Employment (dis)", 0.0, 15.0, 4.0)
                rad = st.number_input("Accessibility Index (rad)", 1.0, 24.0, 5.0)
            with col2:
                tax = st.number_input("Property Tax (tax)", 100.0, 800.0, 300.0)
                ptratio = st.number_input("Pupil-Teacher Ratio", 10.0, 30.0, 18.0)
                b = st.number_input("B Feature", 0.0, 400.0, 300.0)

            # ---------------- Section 3 ----------------
            st.markdown("<div style='background-color:#f0f2f6; padding:10px; border-radius:8px;'>"
                        "<h4 style='text-align:center;'>Socio-Economic Status</h4></div>", unsafe_allow_html=True)
            lstat = st.number_input("Lower Status % (lstat)", 0.0, 40.0, 12.0)
            col1, col2, col3 = st.columns([2.2, 1, 2])
            with col2:
                submitted = st.form_submit_button("🎯 Predict Price")

    if submitted:
        input_df = pd.DataFrame([{
            "crim": crim, "zn": zn, "indus": indus, "chas": chas, "nox": nox,
            "rm": rm, "age": age, "dis": dis, "rad": rad, "tax": tax,
            "ptratio": ptratio, "b": b, "lstat": lstat
        }])
        scaled_data = scaler.transform(input_df)
        prediction = model.predict(scaled_data)
        st.markdown(f"<h3 style='text-align:center; color: #2E8B57;'>Predicted House Price: ${prediction[0]*1000:,.2f}</h3>", unsafe_allow_html=True)

# ------------------- Run the page -------------------
prediction_page()