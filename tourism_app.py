import streamlit as st
import pandas as pd
import numpy as np

# Load Data
@st.cache_data
def load_data():
    cuisine = pd.read_csv("data/cuisine.csv")
    cuisine.columns = cuisine.columns.str.strip().str.lower()
    
    payment = pd.read_csv("data/payment.csv")
    restaurant = pd.read_csv("data/restaurant.csv")
    reviews = pd.read_csv("data/reviews.csv")
    timing = pd.read_csv("data/timing.csv")
    timing_cuisine = pd.read_csv("data/timing_cuisine.csv")
    
    return cuisine, payment, restaurant, reviews, timing, timing_cuisine


cuisine_df, payment_df, restaurant_df, reviews_df, timing_df, timing_cuisine_df = load_data()

# Page Config
st.set_page_config(page_title="🏝️ Tourism Recommender", layout="wide")
st.markdown("<h1 style='text-align: center;'>🏝️ Tourism Recommendation System</h1>", unsafe_allow_html=True)

# Sidebar - User Inputs
st.sidebar.header("🔍 Filter Preferences")
selected_cuisine = st.sidebar.selectbox("Choose a Cuisine", sorted(cuisine_df["cuisine"].unique()))
algo = st.sidebar.radio("Recommendation Type", ["Nearby", "Rating", "Price", "Personalized", "Timing Based"])

# Filter Functions
def find_nearby():
    return restaurant_df.sample(10)

def find_rating(cuisine):
    rid_cuisine = cuisine_df[cuisine_df["cuisine"] == cuisine]["rid"]
    matched = restaurant_df[restaurant_df["id"].isin(rid_cuisine)].sort_values("rating", ascending=False)
    return matched.head(10)

def find_price(cuisine):
    rid_cuisine = cuisine_df[cuisine_df["cuisine"] == cuisine]["rid"]
    matched = restaurant_df[restaurant_df["id"].isin(rid_cuisine)].sort_values("price", ascending=True)
    return matched.head(10)

def find_personalized(cuisine):
    rid_cuisine = cuisine_df[cuisine_df["cuisine"] == cuisine]["rid"]
    matched = restaurant_df[restaurant_df["id"].isin(rid_cuisine)]
    return matched.sort_values(by=["rating", "price"], ascending=[False, True]).head(10)

def find_timing():
    rid = timing_df["rid"].unique()
    return restaurant_df[restaurant_df["id"].isin(rid)].sample(10)

# Display Results
if st.sidebar.button("Get Recommendations"):
    if algo.lower() == "nearby":
        recs = find_nearby()
    elif algo.lower() == "rating":
        recs = find_rating(selected_cuisine)
    elif algo.lower() == "price":
        recs = find_price(selected_cuisine)
    elif algo.lower() == "personalized":
        recs = find_personalized(selected_cuisine)
    elif algo.lower() == "timing based":
        recs = find_timing()
    else:
        recs = pd.DataFrame()

    if not recs.empty:
        st.success(f"🍽️ Recommended Restaurants based on *{algo}*")
        st.dataframe(recs[["name", "address", "city", "rating", "cost"]])

        
        if st.checkbox("📍 Show Map"):
            map_df = recs[["latitude", "longitude"]].rename(columns={"latitude": "lat", "longitude": "lon"})
            st.map(map_df)
    else:
        st.warning("No matching recommendations found.")

# Footer
st.markdown("---")
st.markdown("<center>Made with ❤️ using Streamlit</center>", unsafe_allow_html=True)
