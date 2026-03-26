import streamlit as st
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
import ssl

# Fix for potential SSL/Download errors in Colab environment
ssl._create_default_https_context = ssl._create_unverified_context

# --- 1. THE BRAIN (Training logic inside the file) ---
@st.cache_resource  
def train_model():
    # Loading the dataset from Scikit-Learn
    data = fetch_california_housing()
    
    # Selecting 3 key features for the prediction
    X = pd.DataFrame(data.data, columns=data.feature_names)[['MedInc', 'HouseAge', 'AveRooms']]
    y = data.target # Target is price in $100k units
    
    # Training the Linear Regression model
    model = LinearRegression()
    model.fit(X, y)
    return model

# Initialize the model
model = train_model()

# --- 2. THE FACE (User Interface) ---
st.set_page_config(page_title="House Predictor", page_icon="🏠")

st.title("🏠 California House Price Predictor")
st.markdown("---")
st.write("Enter the neighborhood details below to get an instant price estimation.")

# Creating the Input Fields
col1, col2 = st.columns(2)

with col1:
    income = st.number_input("Median Income (in $10k)", min_value=0.5, max_value=15.0, value=3.5, step=0.1)
    rooms = st.number_input("Average Number of Rooms", min_value=1.0, max_value=10.0, value=5.0, step=0.5)

with col2:
    age = st.slider("House Age (Years)", 1, 52, 25)

st.markdown("---")

# --- 3. THE PREDICTION ---
if st.button("Calculate Estimated Price", use_container_width=True):
    # Prepare the input for the model
    input_data = np.array([[income, age, rooms]])
    
    # Get the prediction
    prediction = model.predict(input_data)[0]
    
    # Convert from $100k units to actual Dollars
    actual_price = prediction * 100000
    
    # Display the result
    st.metric(label="Predicted Market Value", value=f"${actual_price:,.2f}")
    
    if actual_price > 300000:
        st.success("This is considered a high-value neighborhood.")
    else:
        st.info("This is considered an affordable-range neighborhood.")
