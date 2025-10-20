#!/usr/bin/env python
# coding: utf-8

# In[6]:


import streamlit as st
import requests
import pandas as pd


# In[7]:


# Streamlit Page Config
# ---------------------
st.set_page_config(
    page_title="AI Weather Agent",
    page_icon="🌦️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------
# Helper Functions
# ---------------------

def get_coordinates(city_name):
    """Get latitude and longitude for a city"""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    response = requests.get(url)
    data = response.json()
    if "results" in data and len(data["results"]) > 0:
        return data["results"][0]["latitude"], data["results"][0]["longitude"]
    return None, None

def get_hourly_temperature(lat, lon):
    """Fetch hourly temperature data from Open-Meteo API"""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()
    hourly_data = []
    for time, temp in zip(data['hourly']['time'], data['hourly']['temperature_2m']):
        hourly_data.append([time, temp])
    return hourly_data

def get_city_image(city_name):
    """Get a dynamic image for the city from Unsplash"""
    url = f"https://source.unsplash.com/600x400/?{city_name},city"
    return url

# ---------------------
# UI Layout
# ---------------------
st.title("🌦️ AI Weather Agent")
st.subheader("Check hourly temperatures for any city")

city = st.text_input("Enter city name:")

if city:
    lat, lon = get_coordinates(city)
    if lat is None:
        st.error("City not found. Please try another.")
    else:
        st.image(get_city_image(city), use_column_width=True)
        hourly_weather = get_hourly_temperature(lat, lon)
        st.success(f"Showing next 24 hours for {city}")

        # ---------------------
        # Temperature Line Chart (Streamlit native)
        # ---------------------
        df = pd.DataFrame(hourly_weather[:24], columns=['Time', 'Temperature'])
        df['Time'] = pd.to_datetime(df['Time'])
        df.set_index('Time', inplace=True)
        st.line_chart(df)

        # ---------------------
        # Hourly Cards with Emoji
        # ---------------------
        st.markdown("### Hourly Temperatures")
        for entry in hourly_weather[:12]:  # show first 12 hours
            time, temp = entry
            if temp >= 25:
                emoji = "☀️"
            elif temp >= 15:
                emoji = "🌤️"
            else:
                emoji = "❄️"
            col1, col2 = st.columns([2,3])
            col1.write(f"{time}")
            col2.write(f"{temp}°C {emoji}")

# ---------------------
# Footer
# ---------------------
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit | AI Weather Agent")


# In[ ]:




