import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# --- 1. SETTINGS & STYLE ---
st.set_page_config(page_title="Pro Portfolio Tracker", layout="wide", page_icon="📈")
st.title("🚀 Python Developer Portfolio Tracker")

# Initialize our "database" in memory if it doesn't exist
if 'my_assets' not in st.session_state:
    st.session_state.my_assets = []

# --- 2. USER INPUT AREA (Sidebar) ---
with st.sidebar:
    st.header("➕ Add New Asset")
    symbol = st.text_input("Ticker Symbol", value="AAPL", help="e.g. TSLA, BTC-USD, RELIANCE.NS")
    quantity = st.number_input("Quantity Owned", min_value=0.01, value=1.0, step=0.1)
    
    if st.button("Add to Portfolio", use_container_width=True):
        # Check if the ticker is valid before adding to the list
        try:
            check_stock = yf.Ticker(symbol)
            check_hist = check_stock.history(period="1d")
            if not check_hist.empty:
                st.session_state.my_assets.append({"ticker": symbol.upper(), "qty": quantity})
                st.success(f"Added {symbol.upper()}")
            else:
                st.error("Ticker found, but no price data available.")
        except:
            st.error("Invalid Ticker or Network Error!")

    st.divider()
    if st.button("🗑️ Clear All Portfolio", use_container_width=True):
        st.session_state.my_assets = []
        st.rerun()

# --- 3. DATA CALCULATION & DISPLAY ---
if st.session_state.my_assets:
    display_data = []
    total_portfolio_value = 0

    # Spinner shows a loading icon while the API fetches data
    with st.spinner('Updating live market prices...'):
        for item in st.session_state.my_assets:
            ticker = item['ticker']
            qty = item['qty']
            
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1d")
                
                # If market is closed or after-hours, hist might be empty
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                else:
                    # Fallback for 24/7 assets or different exchange timings
                    current_price = stock.fast_info['lastPrice'] 
                
                market_value = current_price * qty
                total_portfolio_value += market_value
                
                display_data.append({
                    "Asset": ticker,
                    "Quantity": qty,
                    "Live Price ($)": round(current_price, 2),
                    "Total Value ($)": round(market_value, 2)
                })
            except Exception as e:
                st.error(f"Could not fetch data for {ticker}: {e}")
                continue # Skip this asset and move to the next

    # Convert our list to a DataFrame for easy visualization
    df = pd.DataFrame(display_data)

    # --- 4. THE DASHBOARD ---
    # Top Level Metric
    st.metric(label="Total Portfolio Net Worth", value=f"${total_portfolio_value:,.2f}")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("📊 Your Current Holdings")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("🥧 Asset Allocation")
        fig = px.pie(df, values='Total Value ($)', names='Asset', hole=0.5,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Your portfolio is currently empty. Use the sidebar to add stocks or crypto.")
    st.image("https://images.unsplash.com/photo-1611974717482-9828d0005d6e?auto=format&fit=crop&q=80&w=800", caption="Start tracking your wealth today!")
