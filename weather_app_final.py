#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import requests
import pandas as pd
import plotly.express as px


# In[2]:


# ---------------------
# Streamlit Page Config
# ---------------------
st.set_page_config(
    page_title="AI Weather Agent",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------
# Helper Functions
# ---------------------
def get_coordinates(city_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    response = requests.get(url)
    data = response.json()
    if "results" in data and len(data["results"]) > 0:
        return data["results"][0]["latitude"], data["results"][0]["longitude"]
    return None, None

def get_hourly_temperature(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()
    hourly_data = []
    for time, temp in zip(data['hourly']['time'], data['hourly']['temperature_2m']):
        hourly_data.append([time, temp])
    return hourly_data

def get_city_image(city_name):
    return f"https://source.unsplash.com/900x500/?{city_name},city"

def weather_emoji(temp):
    if temp >= 30:
        return "☀️"
    elif temp >= 20:
        return "🌤️"
    elif temp >= 10:
        return "☁️"
    elif temp >= 0:
        return "🌧️"
    else:
        return "❄️"

# ---------------------
# UI Layout
# ---------------------
st.title("🌦️ AI Weather Agent")
st.subheader("Hourly temperatures for any city")

city = st.text_input("Enter city name:")

if city:
    lat, lon = get_coordinates(city)
    if lat is None:
        st.error("City not found. Please try another.")
    else:
        # City image
        st.image(get_city_image(city), use_column_width=True)

        # Fetch hourly weather
        hourly_weather = get_hourly_temperature(lat, lon)
        st.success(f"Next 24 hours for {city}")

        # Create DataFrame for Plotly
        df = pd.DataFrame(hourly_weather[:24], columns=['Time', 'Temperature'])
        df['Time'] = pd.to_datetime(df['Time'])

        # Plotly line chart (no PyArrow needed)
        fig = px.line(df, x='Time', y='Temperature', markers=True, title=f"Hourly Temperature for {city}")
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Temperature (°C)",
            template="plotly_white",
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Horizontal scrollable hourly cards
        st.markdown("### Hourly Forecast")
        cols = st.columns(len(hourly_weather[:24]))
        for i, entry in enumerate(hourly_weather[:24]):
            time, temp = entry
            with cols[i]:
                st.markdown(f"**{time.split('T')[1]}**")
                st.markdown(f"{weather_emoji(temp)}")
                st.markdown(f"**{temp}°C**")

# ---------------------
# Footer
# ---------------------
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit | AI Weather Agent")


# In[ ]:





# In[ ]:





# In[ ]:




