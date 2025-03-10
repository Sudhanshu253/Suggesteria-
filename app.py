import streamlit as st
import pandas as pd
import pickle

# Load data and models
anime = pd.read_csv("anime.csv")
vectorizer = pickle.load(open("PickleFiles/vectorizer.pkl", "rb"))
anime_similarity = pickle.load(open("PickleFiles/anime_similarity.pkl", "rb"))

# Streamlit UI Customization
st.set_page_config(page_title="AniMatch - Anime Recommender", layout="wide")

# Add Custom CSS for a Professional Look
st.markdown("""
    <style>
        .big-title {
            font-size: 36px;
            font-weight: bold;
            color: #1E90FF;
            text-align: center;
            margin-bottom: 10px;
        }
        .sub-header {
            font-size: 20px;
            font-weight: bold;
            color: #4682B4;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #2C3E50;
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 14px;
        }
        .stButton>button {
            background-color: #1E90FF;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 8px 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown('<p class="big-title">🎥 AniMatch - Anime Recommender</p>', unsafe_allow_html=True)
st.write("Find your next favorite anime based on what you already love!")

# Dropdown for anime selection
st.markdown('<p class="sub-header">🔎 Choose an Anime:</p>', unsafe_allow_html=True)
anime_names = anime['name'].tolist()
selected_anime = st.selectbox("", anime_names)

# Recommendation function
def recommend_anime(anime_name, k=5):
    anime_name = anime_name.lower()
    matched_indices = anime[anime['name'].str.lower() == anime_name].index

    if len(matched_indices) == 0:
        return []

    anime_index = matched_indices[0]
    sim_scores = list(enumerate(anime_similarity[anime_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:k+1]
    return [anime['name'][i[0]] for i in sim_scores]

# Display recommendations
if st.button("🎯 Get Recommendations"):
    with st.spinner("🔄 Finding the best anime for you..."):
        recommendations = recommend_anime(selected_anime)

    if recommendations:
        st.markdown('<p class="sub-header">🌟 Recommended Anime:</p>', unsafe_allow_html=True)
        for rec in recommendations:
            st.write(f"📺 {rec}")
    else:
        st.error("No recommendations found.")

# Sidebar - About & Contact Info
st.sidebar.markdown('<p class="sub-header">ℹ️ About AniMatch</p>', unsafe_allow_html=True)
st.sidebar.write("""
AniMatch is a smart anime recommendation system that helps you find similar anime based on what you like.  
Our goal is to make anime discovery easier and more fun!
""")

st.sidebar.markdown('<p class="sub-header">📧 Contact Us</p>', unsafe_allow_html=True)
st.sidebar.write("""
- 📧 Email: support@animatch.com  
- 🔗 Connect: [AniMatch Socials](https://twitter.com)  
- 🌐 Website: [AniMatch](https://animatch.streamlit.app)
""")

# Footer - Copyright Info
st.markdown("""
    <div class="footer">
        © 2025 AniMatch. All Rights Reserved.
    </div>
""", unsafe_allow_html=True)
