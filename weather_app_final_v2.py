#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import requests
import pandas as pd
import plotly.express as px


# In[2]:


st.set_page_config(page_title="AI Weather Agent", layout="centered")

st.title("🌤️ AI Weather Agent")
st.write("Check live and hourly weather updates for any city!")

city = st.text_input("🏙️ Enter city name", "Chicago")

if city:
    # Step 1: Get city coordinates from Open-Meteo geocoding API
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_res = requests.get(geo_url).json()

    if "results" in geo_res and len(geo_res["results"]) > 0:
        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        city_name = geo_res["results"][0]["name"]
        country = geo_res["results"][0].get("country", "")

        # Step 2: Fetch both current and hourly forecast data
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,weathercode&timezone=auto"
        res = requests.get(weather_url).json()

        # Step 3: Extract current temperature and condition
        current_temp = res.get("current_weather", {}).get("temperature", "N/A")
        weather_code = res.get("current_weather", {}).get("weathercode", 0)

        # Weather condition mapping
        weather_descriptions = {
            0: "☀️ Clear sky",
            1: "🌤️ Mainly clear",
            2: "⛅ Partly cloudy",
            3: "☁️ Overcast",
            45: "🌫️ Foggy",
            48: "🌫️ Depositing rime fog",
            51: "🌦️ Light drizzle",
            53: "🌧️ Drizzle",
            55: "🌧️ Heavy drizzle",
            61: "🌦️ Light rain",
            63: "🌧️ Moderate rain",
            65: "🌧️ Heavy rain",
            71: "🌨️ Snow fall",
            80: "🌦️ Rain showers",
            95: "⛈️ Thunderstorm"
        }
        current_condition = weather_descriptions.get(weather_code, "🌤️ Clear")

        # Show current weather
        st.subheader(f"🌡️ Current Weather in {city_name}, {country}")
        st.metric(label="Temperature", value=f"{current_temp}°C", delta=None)
        st.write(f"**Condition:** {current_condition}")

        # Step 4: Hourly forecast
        hourly = res["hourly"]
        df = pd.DataFrame({
            "Time": hourly["time"],
            "Temperature (°C)": hourly["temperature_2m"]
        })

        # Keep next 24 hours only
        df = df.head(24)

        st.markdown("---")
        st.subheader(f"🕐 Next 24 Hours Forecast for {city_name}")

        # Plot interactive line chart
        fig = px.line(df, x="Time", y="Temperature (°C)", title="Hourly Temperature", markers=True)
        st.plotly_chart(fig, use_container_width=True)  # Fixed deprecated warning

        # Show hourly icons and details
        st.markdown("### 🌦️ Hourly Forecast Details")
        weather_codes = hourly.get("weathercode", [0] * 24)
        for t, temp, code in zip(df["Time"], df["Temperature (°C)"], weather_codes[:24]):
            icon = weather_descriptions.get(code, "🌤️")
            st.write(f"{t} — {icon} {temp}°C")

    else:
        st.error("❌ City not found. Please enter the City name correctly or try again.")


# In[ ]:




