import streamlit as st
import pickle
import numpy as np
import os
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
import pickle

# 1. Load data
data = fetch_california_housing()
df = pd.DataFrame(data.data, columns=data.feature_names)
X = df[['MedInc', 'HouseAge', 'AveRooms']] # Simplified features
y = data.target # Price in $100k units

# 2. Train Model
model = LinearRegression()
model.fit(X, y)

# 3. Save Model to a file
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved as model.pkl")
# --- 1. LOAD THE PRE-TRAINED MODEL ---
# This part stays outside the button so it only runs once
if os.path.exists('model.pkl'):
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
else:
    st.error("Model file (model.pkl) not found! Please upload it to GitHub.")
    st.stop()

# --- 2. USER INTERFACE ---
st.title("🏠 House Price Predictor")
st.write("Enter the details below to estimate the house value.")

# Create input fields
income = st.number_input("Median Neighborhood Income (in $10k)", value=3.0, min_value=0.0)
age = st.slider("House Age (years)", 1, 52, 20)
rooms = st.number_input("Average Number of Rooms", value=5, min_value=1)

# --- 3. PREDICTION LOGIC ---
if st.button("Predict Price"):
    try:
        # Arrange inputs for the model exactly how it was trained
        features = np.array([[income, age, rooms]])
        prediction = model.predict(features)[0]
        
        # Format the output nicely
        # Note: California dataset prices are in $100k units
        final_price = prediction * 100000
        
        if final_price < 0:
            st.warning("The predicted price is unusually low. Check your inputs!")
        else:
            st.success(f"Estimated Price: **${final_price:,.2f}**")
            
    except Exception as e:
        st.error(f"Prediction failed: {e}")
