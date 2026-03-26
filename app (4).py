import streamlit as st
import pickle
import numpy as np

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