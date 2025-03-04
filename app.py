import streamlit as st
import requests
from datetime import datetime
import time

# Constants
PLOT_BGCOLOR = 'rgba(0,0,0,0)'

# Set page config - this must be the first Streamlit command
st.set_page_config(
    page_title="Currency Converter",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    body {
    background-color: black;
            }
    .main-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 10px;
    }
    .app-title1 {
        color: blue;
        text-align: center;
        font-size: 28px;
        margin-bottom: 5px;
        font-weight: bold;
        text-shadow: 4px 4px 16px rgba(0, 0, 0, 0.3);
    }
    .app-title2 {
        color: #e11d48;
        text-align: center;
        font-size: 28px;
        margin-bottom: 5px;
        font-weight: bold;
        text-shadow: 4px 4px 16px rgba(0, 0, 0, 0.3);
    }
    .app-subtitle {
        color: white !important;
        text-align: center;
        font-size: 16px;
        margin-bottom: 20px;
    }
    .result-container {
        font-size: 24px;
        font-weight: bold;
        color: #46f705;
        text-align: center;
        margin: 15px 0;
    }
    .label {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .footer {
        text-align: center;
        color: #BF40BF;
        font-size: 16px;
        font-weight: bold;
        margin-top: 10px;
    }
    .stButton > button {
        background-color: #111827 !important;
        color: #fef08a !important;
        font-weight: bold !important;
        font-size: 18px !important;
        width: 100% !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
    }
    .stSelectbox {
        color: #2563eb !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'converted_amount' not in st.session_state:
    st.session_state.converted_amount = "0.00"
if 'exchange_rates' not in st.session_state:
    st.session_state.exchange_rates = {}
if 'last_updated' not in st.session_state:
    st.session_state.last_updated = None
if 'conversion_history' not in st.session_state:
    st.session_state.conversion_history = []

# Function to fetch exchange rates
@st.cache_data(ttl=3600)
def fetch_exchange_rates():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data["rates"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), None
    except Exception as e:
        return None, None, f"Error fetching exchange rates: {str(e)}"

# Main app container
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="app-title1">🐍 Learn Python 🐍</div>', unsafe_allow_html=True)
st.markdown('<div class="app-title2">💱 Currency Converter</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Convert between different currencies.</div>', unsafe_allow_html=True)

# Fetch exchange rates
with st.spinner("Fetching exchange rates..."):
    rates, last_updated, error = fetch_exchange_rates()
    if rates:
        st.session_state.exchange_rates = rates
        st.session_state.last_updated = last_updated

if error:
    st.error(error)
else:
    currencies = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "PKR", "SAR", "AED", "MYR"]
    
    # Input fields
    col1, col2 = st.columns([3, 1])
    with col1:
        amount = st.number_input("Amount", min_value=0.01, value=1.00, step=0.01, label_visibility="collapsed")
    with col2:
        source_currency = st.selectbox("Source Currency", currencies, index=0, label_visibility="collapsed", key="source_currency")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="result-container">Please select amount & currency name</div>', unsafe_allow_html=True)
    with col2:
        target_currency = st.selectbox("Target Currency", currencies, index=currencies.index("PKR"), label_visibility="collapsed", key="target_currency")
    
    # Convert button
    if st.button("Convert"):
        with st.spinner("Converting..."):
            time.sleep(0)
            if source_currency and target_currency and amount and st.session_state.exchange_rates:
                if source_currency == "USD":
                    rate = st.session_state.exchange_rates[target_currency]
                else:
                    rate = st.session_state.exchange_rates[target_currency] / st.session_state.exchange_rates[source_currency]
                
                result = amount * rate
                st.session_state.converted_amount = f"{result:.2f}"
                st.session_state.conversion_history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "from_currency": source_currency,
                    "to_currency": target_currency,
                    "amount": amount,
                    "result": result
                })
            else:
                st.session_state.converted_amount = "Conversion failed"

# Show last updated time
if st.session_state.last_updated:
    st.markdown(f'<div style="text-align: center; color: white;">Rates last updated: {st.session_state.last_updated}</div>', unsafe_allow_html=True)

# Conversion history section
if st.session_state.conversion_history:
    
    st.markdown('<h3 style="color: green; text-align: center;">Conversion Result &  History</h3>', unsafe_allow_html=True)
    
    for conversion in reversed(st.session_state.conversion_history[-5:]):
        st.markdown(f"""
            <div style="padding: 10px; margin-bottom: 8px; border-bottom: 1px solid #e5e7eb;">
                <div style="font-size: 20px; font-weight: bold; color: blue;">{conversion['timestamp']}</div>
                <div style="font-size: 20px; font-weight: bold; color: red;">
                    {conversion['amount']} {conversion['from_currency']} = {conversion['result']:.2f} {conversion['to_currency']}
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="footer">Author: Azmat Ali</div>', unsafe_allow_html=True)

# {st.session_state.converted_amount}