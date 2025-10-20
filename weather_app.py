#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import requests


# In[2]:


# Function to get latitude and longitude from city name
def get_coordinates(city_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    response = requests.get(url)
    data = response.json()

    if "results" in data:
        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]
        return lat, lon
    else:
        return None, None

# Function to get hourly temperature
def get_hourly_temperature(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    hourly_data = []
    for time, temp in zip(data['hourly']['time'], data['hourly']['temperature_2m']):
        hourly_data.append(f"{time} → {temp}°C")
    return hourly_data

# Streamlit UI
st.title("🌦️ AI Weather Agent")
st.subheader("Check hourly temperatures for any city")

city = st.text_input("Enter city name:")

if city:
    lat, lon = get_coordinates(city)
    if lat is None:
        st.error("City not found.")
    else:
        hourly_weather = get_hourly_temperature(lat, lon)
        st.success(f"Showing next 24 hours for {city}")
        st.write("\n".join(hourly_weather[:24]))  # show first 24 hours


# In[ ]:




