#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import requests
import pandas as pd
import plotly.express as px


# In[3]:


# 🌇 App Configuration
st.set_page_config(page_title="AI Weather Agent", layout="wide")

# 🌈 Custom CSS (Better contrast + default background)
st.markdown("""
    <style>
    body {
        background-color: #121212;
        font-family: 'Segoe UI', sans-serif;
    }
    .stApp {
        background-image: linear-gradient(to bottom, #1e1e1e, #2e2e2e);
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 25px;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        color: #fff;
        text-align: center;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🏙️ Header
st.markdown("<h1 style='text-align:center;'>🌤️ AI Weather Agent</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Your intelligent, visually enhanced weather companion</p>", unsafe_allow_html=True)
st.markdown("---")

# 🧭 City input (no default)
city = st.text_input("🏙️ Enter city name to check weather", "")

if city.strip():
    with st.spinner("Fetching weather data..."):
        # 🌍 Get coordinates
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_res = requests.get(geo_url).json()

        if "results" in geo_res and len(geo_res["results"]) > 0:
            lat = geo_res["results"][0]["latitude"]
            lon = geo_res["results"][0]["longitude"]
            city_name = geo_res["results"][0]["name"]
            country = geo_res["results"][0].get("country", "")

            # 🖼️ Background image (Unsplash API)
            bg_url = f"https://source.unsplash.com/1600x900/?{city},cityscape,skyline"
            st.markdown(f"""
                <style>
                .stApp {{
                    background-image: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.7)), url("{bg_url}");
                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                }}
                </style>
            """, unsafe_allow_html=True)

            # 🌦️ Weather data
            weather_url = (
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
                "&current_weather=true&hourly=temperature_2m,weathercode&timezone=auto"
            )
            res = requests.get(weather_url).json()

            current_temp = res.get("current_weather", {}).get("temperature", "N/A")
            weather_code = res.get("current_weather", {}).get("weathercode", 0)

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

            # 🌡️ Show Current Weather
            st.markdown(
                f"""
                <div class="glass-card">
                    <h2>{city_name}, {country}</h2>
                    <h1 style='font-size:70px;'>{current_temp}°C</h1>
                    <h3>{current_condition}</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # 📈 Hourly Forecast
            hourly = res["hourly"]
            df = pd.DataFrame({
                "Time": hourly["time"],
                "Temperature (°C)": hourly["temperature_2m"]
            })
            df = df.head(24)

            st.markdown("<br><h3 style='text-align:center;'>🌤️ Next 24 Hours Forecast</h3>", unsafe_allow_html=True)
            fig = px.line(
                df,
                x="Time",
                y="Temperature (°C)",
                title="",
                markers=True,
                template="plotly_dark",
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig, use_container_width=True)

            # 🕒 Hourly details
            st.markdown("<h4>🕓 Detailed Hourly Forecast</h4>", unsafe_allow_html=True)
            weather_codes = hourly.get("weathercode", [0] * 24)
            for t, temp, code in zip(df["Time"], df["Temperature (°C)"], weather_codes[:24]):
                icon = weather_descriptions.get(code, "🌤️")
                st.markdown(
                    f"""
                    <div style="padding:8px; margin:5px; background:rgba(255,255,255,0.2);
                    border-radius:10px; backdrop-filter:blur(10px); color:white;">
                        <b>{t}</b> — {icon} {temp}°C
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:
            st.error("❌ City not found. Please try again.")
else:
    st.info("👆 Please enter a city name to view the weather forecast.")


# In[ ]:




