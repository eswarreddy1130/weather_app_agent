#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pyttsx3


# In[2]:


# ------------------- CONFIG -------------------
st.set_page_config(page_title="AI Weather Agent", page_icon="⛅", layout="centered")

# Voice Engine (English)
engine = pyttsx3.init()
engine.setProperty('rate', 165)
engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')

# Background styling (dynamic)
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #74ABE2, #5563DE);
    background-attachment: fixed;
}
.weather-card {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    color: white;
    text-align: center;
}
.weather-card h3 {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;
}
.toggle {
    font-size: 18px;
    color: #fff;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ------------------- FUNCTIONS -------------------

def get_weather_data(city):
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_res = requests.get(geocode_url).json()
    if "results" not in geo_res:
        return None
    lat, lon = geo_res["results"][0]["latitude"], geo_res["results"][0]["longitude"]

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,relative_humidity_2m,weathercode,windspeed_10m"
        f"&daily=temperature_2m_max,temperature_2m_min,weathercode"
        f"&current_weather=true&timezone=auto"
    )
    return requests.get(weather_url).json(), geo_res["results"][0]["name"]

def weather_description(code):
    mapping = {
        0: "Clear sky ☀️", 1: "Mainly clear 🌤️", 2: "Partly cloudy ⛅", 3: "Overcast ☁️",
        45: "Fog 🌫️", 48: "Depositing rime fog 🌫️", 51: "Light drizzle 🌦️",
        61: "Rainy 🌧️", 71: "Snowfall ❄️", 95: "Thunderstorm ⛈️"
    }
    return mapping.get(code, "Unknown")

def speak_weather(city, temp, desc):
    text = f"The current temperature in {city} is {temp:.1f} degrees Celsius with {desc.lower()}."
    engine.say(text)
    engine.runAndWait()

def c_to_f(c):
    return (c * 9/5) + 32

# ------------------- UI -------------------

st.markdown("<h1 style='text-align:center; color:white;'>🌤️ AI Weather Agent</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:white;'>Your friendly AI weather companion</h3>", unsafe_allow_html=True)

city = st.text_input("Enter city name", placeholder="e.g. Hyderabad, New York", key="city")

unit = st.radio("Select Temperature Unit", ["°C", "°F"], horizontal=True, key="unit")

if city:
    with st.spinner("Fetching live weather data..."):
        data, city_name = get_weather_data(city)
        if data:
            current = data["current_weather"]
            temp_c = current["temperature"]
            desc = weather_description(current["weathercode"])

            temp_display = c_to_f(temp_c) if unit == "°F" else temp_c
            st.markdown(
                f"<div class='weather-card'><h3>{city_name}</h3>"
                f"<p style='font-size:48px'>{temp_display:.1f}{unit}</p>"
                f"<p style='font-size:22px'>{desc}</p></div>",
                unsafe_allow_html=True
            )

            # Voice
            speak_weather(city_name, temp_c, desc)

            # Hourly Forecast (next 6 hours)
            st.subheader("🌇 Next 6 Hours")
            hours = data["hourly"]["time"][:6]
            temps = data["hourly"]["temperature_2m"][:6]
            if unit == "°F":
                temps = [c_to_f(t) for t in temps]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hours, y=temps, mode="lines+markers", line=dict(width=3)))
            fig.update_layout(
                xaxis_title="Time",
                yaxis_title=f"Temperature ({unit})",
                template="plotly_dark",
                height=300,
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Weekly Forecast
            st.subheader("🗓️ Weekly Forecast")
            days = data["daily"]["time"]
            max_t = data["daily"]["temperature_2m_max"]
            min_t = data["daily"]["temperature_2m_min"]
            descs = [weather_description(c) for c in data["daily"]["weathercode"]]

            cols = st.columns(7)
            for i, col in enumerate(cols):
                with col:
                    col.markdown(
                        f"<div class='weather-card'><h4>{days[i][5:]}</h4>"
                        f"<p>{descs[i]}</p>"
                        f"<p>🌡️ {max_t[i]:.1f}/{min_t[i]:.1f}°C</p></div>",
                        unsafe_allow_html=True
                    )
        else:
            st.error("City not found! Please check the name and try again.")


# In[ ]:




