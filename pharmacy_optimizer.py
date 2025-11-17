# pharmacy_optimizer.py
import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt

st.title(" Pharmacy Inventory Optimizer")
st.markdown("**5 Drugs | 50 Weeks | Seasonal + Trend Data**")

# --- Generate 5 Drugs with Unique Patterns ---
np.random.seed(42)
drugs = ['Paracetamol 500mg', 'Dolo 650', 'Crocin', 'Amoxicillin 250mg', 'Metformin 500mg']
data_list = []

for drug in drugs:
    dates = pd.date_range("2025-01-05", periods=50, freq='W')
    base = 32 if drug != 'Amoxicillin 250mg' else 22
    
    # Very slow trend (+5 units per year max)
    trend = np.linspace(0, 5, 50)
    
    # Gentle seasonal swing (±10 units)
    season = 10 * np.sin(2 * np.pi * np.arange(50) / 52)
    
    # Small noise
    noise = np.random.normal(0, 4, 50)
    
    demand = base + trend + season + noise
    demand = np.clip(demand, 18, 58).astype(int)   # Hard cap at 58
    
    df_drug = pd.DataFrame({'ds': dates, 'y': demand, 'drug_name': drug})
    data_list.append(df_drug)

df = pd.concat(data_list, ignore_index=True)

# --- Streamlit App ---
selected_drug = st.selectbox("Select Drug", sorted(df['drug_name'].unique()))

if st.button("Generate Forecast"):
    data = df[df['drug_name'] == selected_drug][['ds', 'y']].copy()
    
    m = Prophet(yearly_seasonality=True, weekly_seasonality=True)
    m.fit(data)
    future = m.make_future_dataframe(periods=4, freq='W')
    forecast = m.predict(future)
    
    fig = m.plot(forecast)
    plt.title(f"{selected_drug} - Demand Forecast")
    plt.ylabel("Units Sold")
    st.pyplot(fig)
    
    pred = int(forecast['yhat'].iloc[-1])
    st.metric("Next Week Predicted Demand", f"{pred} units")
    
    if pred > 50:
        st.error("CRITICAL: Reorder 60+ units NOW!")
    elif pred > 40:
        st.warning("High demand — Reorder soon")
    else:
        st.success("Normal demand")
    
    with st.expander("View Last 5 Weeks"):
        st.write(data.tail(5).rename(columns={'ds': 'Week', 'y': 'Sold'}))
