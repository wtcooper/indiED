import pydeck as pdk
import streamlit as st
import pandas as pd


def hextofloats(h):
    '''Takes a hex rgb string (e.g. #ffffff) and returns an RGB tuple (float, float, float).'''
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))  # skip '#'


def render_map(session_state, indi_ed_lat, indi_ed_lon, image):
    image.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=indi_ed_lat,
            longitude=indi_ed_lon,
            zoom=11,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=session_state.home,
                get_position='[lon, lat]',
                get_color='[0, 30, 300, 160]',
                get_radius=500,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=pd.DataFrame(
                    {'lat': [indi_ed_lat],
                     'lon': [indi_ed_lon]}
                ),
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=300,
            ),
        ],
    ))
