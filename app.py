import streamlit as st
import requests
import pandas as pd

data = pd.read_csv("data/train.csv")  # ton dataset
quartiers = sorted(data["Neighborhood"].unique())
# -----------------------------
# Style CSS pour couleurs
# -----------------------------
st.markdown("""
    <style>
    body {
        background-color: #eaf2f8; /* baby blue */
        color: #0d1b2a;
    }
    .header {
        background-color: #5dade2;  /* Baby blue */
        padding: 20px;
        color: #ffffff;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .footer {
        background-color: #1b263b;  /* Bleu pétrole */
        padding: 10px;
        color: white;
        text-align: center;
        font-size: 14px;
        border-radius: 5px;
        width: 100%;
        bottom: 0;
        left: 0;
        position: fixed;
    }
     .result-box {
        background-color: #f8d7da;  /* fond rose clair pour contraste */
        color: #c82333;              /* texte rouge foncé */
        padding: 20px;
        border-radius: 5px;
        font-size: 24px;
        text-align: center;
        margin-top: 10px;
        font-weight: bold;
    }
    .container-box {
        background-color: #ffffff; /* blanc pour conteneur */
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="header">Estimation des prix immobiliers 🏡</div>', unsafe_allow_html=True)

# -----------------------------
# Sidebar pour navigation
# -----------------------------
page = st.sidebar.radio("Navigation", ["Accueil", "Estimation"])

# -----------------------------
# Page Accueil
# -----------------------------
if page == "Accueil":
    st.subheader("Bienvenue sur l'application immobilière !")
    st.write("Utilisez le menu à gauche pour accéder à l'estimation ou à l'interface administrateur.")

# -----------------------------
# Page Estimation
# -----------------------------
elif page == "Estimation":
    st.markdown('<div class="container-box">', unsafe_allow_html=True)
    st.subheader("Estimation du prix d'une maison")

    with st.form("house_form"):
        surface = st.number_input("Superficie (m²)", min_value=10, value=1500)
        chambres = st.number_input("Nombre de pièces", min_value=1, value=3)
        quartier = st.selectbox("Localisation", quartiers)
        submitted = st.form_submit_button("Prédire le prix")

    if submitted:
        url = "http://127.0.0.1:8000/predict"  # API FastAPI
        data = {
            "BedroomAbvGr": chambres,
            "GrLivArea": surface,
            "YearBuilt": 2005,
            "Neighborhood": quartier
        }

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            st.markdown(f'<div class="result-box">Prix estimé : {result["PredictedPrice"]:,.2f} €</div>', unsafe_allow_html=True)
        except requests.exceptions.HTTPError:
            st.error(f"Erreur API : {response.json()['detail']}")
        except Exception as e:
            st.error(f"Erreur : {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Page Admin
# -----------------------------
# -----------------------------
# Page Admin
# -----------------------------

# -----------------------------
# Footer
# -----------------------------
st.markdown('<div class="footer">© 2026 Mon Projet Immo</div>', unsafe_allow_html=True)
