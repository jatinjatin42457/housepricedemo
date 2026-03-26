
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# --- 1. SETTINGS & STYLE ---
st.set_page_config(page_title="Pro Portfolio", layout="wide")
st.title("🚀 Python Developer Portfolio Tracker")

# Initialize our "database" in memory
if 'my_assets' not in st.session_state:
    st.session_state.my_assets = []

# --- 2. USER INPUT AREA (Sidebar) ---
with st.sidebar:
    st.header("➕ Add New Asset")
    symbol = st.text_input("Ticker Symbol", value="AAPL", help="e.g. TSLA, BTC-USD, RELIANCE.NS")
    quantity = st.number_input("Quantity Owned", min_value=0.01, value=1.0)
    
    if st.button("Add to Portfolio"):
        # Check if the ticker is valid before adding
        try:
            test_data = yf.Ticker(symbol).history(period="1d")
            if not test_data.empty:
                st.session_state.my_assets.append({"ticker": symbol.upper(), "qty": quantity})
                st.success(f"Added {symbol.upper()}")
            else:
                st.error("Invalid Ticker Symbol!")
        except:
            st.error("Connection Error!")

    if st.button("🗑️ Clear All"):
        st.session_state.my_assets = []
        st.rerun()

# --- 3. DATA CALCULATION ---
if st.session_state.my_assets:
    display_data = []
    total_portfolio_value = 0

    for item in st.session_state.my_assets:
        ticker = item['ticker']
        qty = item['qty']
        
        # Fetching Live Price
        stock = yf.Ticker(ticker)
        current_price = stock.history(period="1d")['Close'].iloc[-1]
        market_value = current_price * qty
        total_portfolio_value += market_value
        
        display_data.append({
            "Asset": ticker,
            "Quantity": qty,
            "Live Price ($)": round(current_price, 2),
            "Total Value ($)": round(market_value, 2)
        })

    df = pd.DataFrame(display_data)

    # --- 4. THE DASHBOARD ---
    # Top Stats
    st.metric(label="Total Net Worth", value=f"${total_portfolio_value:,.2f}")

    # Layout: Table on left, Chart on right
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Current Holdings")
        st.table(df) # Shows a clean, non-interactive table for summary

    with col2:
        st.subheader("Asset Allocation")
        fig = px.pie(df, values='Total Value ($)', names='Asset', hole=0.5,
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No assets added yet. Use the sidebar to add your first stock or crypto!")
