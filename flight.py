# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 17:34:18 2025

@author: dhore
"""

import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import numpy as np

st.title("City Route Mapper")
st.write("Enter at least 2 cities to plot their route on a map.")

# Input from user
num_cities = st.number_input("How many cities are you traveling to?", min_value=2, value=2, step=1)

cities = []
for i in range(num_cities):
    city = st.text_input(f"Enter City {i+1}:", key=f"city_{i}")
    cities.append(city)

# When all cities are filled
if all(cities) and st.button("Generate Map"):
    geolocator = Nominatim(user_agent="my_geocoding_app")
    geo_location = np.zeros((num_cities, 2))

    for i, city in enumerate(cities):
        location = geolocator.geocode(city)
        if location:
            geo_location[i][0] = location.latitude
            geo_location[i][1] = location.longitude
        else:
            st.error(f"Could not find location for: {city}")
            st.stop()

    # Create the map
    m = folium.Map(location=[geo_location[0][0], geo_location[0][1]], zoom_start=3)

    # Add city markers
    for i in range(num_cities):
        folium.Marker(
            location=[geo_location[i][0], geo_location[i][1]],
            popup=cities[i]
        ).add_to(m)

    # Draw route
    for i in range(num_cities - 1):
        folium.PolyLine(
            locations=[
                [geo_location[i][0], geo_location[i][1]],
                [geo_location[i+1][0], geo_location[i+1][1]]
            ],
            color="red", weight=2, dash_array="5,5"
        ).add_to(m)

    # Loop back to first city
    folium.PolyLine(
        locations=[
            [geo_location[-1][0], geo_location[-1][1]],
            [geo_location[0][0], geo_location[0][1]]
        ],
        color="red", weight=2, dash_array="5,5"
    ).add_to(m)

    st.subheader("Generated Map:")
    folium_static(m)