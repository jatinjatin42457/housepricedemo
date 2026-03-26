import streamlit as st
import pickle
import numpy as np
import pandas as pd
import ssl
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
import pickle
ssl._create_default_https_context = ssl._create_unverified_context
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
# Load the brain (the model we saved)
model = pickle.load(open('model.pkl', 'rb'))

st.title("🏠 House Price Predictor")
st.write("Enter the details below to estimate the house value.")

# Create input fields
income = st.number_input("Median Neighborhood Income (in $10k)", value=3.0)
age = st.slider("House Age (years)", 1, 50, 20)
rooms = st.number_input("Average Number of Rooms", value=5)

# Predict button
if st.button("Predict Price"):
    # Arrange inputs for the model
    features = np.array([[income, age, rooms]])
    prediction = model.predict(features)[0]
    
    # Show the result (converted from $100k units)
    st.success(f"Estimated Price: ${prediction * 100000:,.2f}")