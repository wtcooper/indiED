#############################################
# Define Libraries to Import
#############################################

import streamlit as st
import pandas as pd
import SessionState
import logging
import time
from utilities import render_map


#############################################
# Default and Static Variables
#############################################

# Create a Variable of your home coordinates
default_home_lat = 27.83789
default_home_lon = -82.60948

# Create a Variable of the Indi-ED coordinates
indi_ed_lat = 27.77315
indi_ed_lon = -82.65881

# add functionality: set a dynamic title
enable_dynamic_title = 'OFF'

# add functionality: enable driving instructions
enable_driving_run = 'OFF'


#############################################
# Side-bar Navigation
#############################################

# Add a dynamic Title
if enable_dynamic_title == 'ON':
    st.sidebar.markdown('## Display Title')
    user_title = st.sidebar.text_input("Enter your title:", 'How I get to Indi-ED each day!')

# Add the home coordinates
st.sidebar.markdown('## Home Location')
home_lat = st.sidebar.number_input("Starting latitude (North-South):", value=default_home_lat, step=0.015)
home_lon = st.sidebar.number_input("Starting longitude (East-West):", value=default_home_lon, step=0.015)
click_reset = st.sidebar.button('--reset--')

st.sidebar.markdown('## Driving Speed and Direction')
# Action Button step size
step_size = st.sidebar.number_input("Driving Speed:", value=35, step=5)

# Add some Action Buttons to the side navigation bar
st.sidebar.markdown('<span style="font-size:.8em;">Driving Direction:</span>',unsafe_allow_html=True)
click_up = st.sidebar.button('up')
click_down = st.sidebar.button('down')
click_left = st.sidebar.button('left')
click_right = st.sidebar.button('right')

if enable_driving_run == 'ON':
    st.sidebar.markdown('## Driving Instructions')
    drive_instructions = st.sidebar.text_input("Enter directions (U,D,L,R) separated by a comma", 'D,L,L,L,D,D,D,D,D,D,L,L,L')
    click_run = st.sidebar.button('run')


#############################################
# Data Management
#############################################

# Create an Object to remember where you are after each click
session_state = SessionState.get(
    blue_car = pd.DataFrame(
        {'lat': [home_lat],
         'lon': [home_lon]}
    )
)


#############################################
# Main Display
#############################################

# Add a Title
if enable_dynamic_title == 'ON':
    st.title(user_title)
else:
    st.title('How I get to Indi-ED each day!')

image = st.empty()
render_map(session_state, indi_ed_lat, indi_ed_lon, image)


#############################################
# Actions and Logic
#############################################

# Add some Actions when the buttons are clicked
if click_up:
    logging.info("Moving up")
    session_state.blue_car['lat'] = session_state.blue_car['lat']+step_size/3500.0
    render_map(session_state, indi_ed_lat, indi_ed_lon, image)

if click_down:
    logging.info("Moving down")
    session_state.blue_car['lat'] = session_state.blue_car['lat']-step_size/3500.0
    render_map(session_state, indi_ed_lat, indi_ed_lon, image)

if click_left:
    logging.info("Moving left")
    session_state.blue_car['lon'] = session_state.blue_car['lon']-step_size/3500.0
    render_map(session_state, indi_ed_lat, indi_ed_lon, image)

if click_right:
    logging.info("Moving right")
    session_state.blue_car['lon'] = session_state.blue_car['lon']+step_size/3500.0
    render_map(session_state, indi_ed_lat, indi_ed_lon, image)

if click_reset:
    logging.warning("Resetting the home position")
    session_state.blue_car['lon'] = default_home_lon
    session_state.blue_car['lat'] = default_home_lat
    render_map(session_state, indi_ed_lat, indi_ed_lon, image)

# if click_down_left:
#     st.write('Moving down and to the left!')
#     session_state.blue_car['lat'] = session_state.blue_car['lat']-0.01
#     session_state.blue_car['lon'] = session_state.blue_car['lon']-0.01

if enable_driving_run == 'ON':
    if click_run:
        directions = drive_instructions.split(",")
        logging.info(f"directions: {directions}")

        # Loop through all directions entered
        for direction in directions:

            # determine the direction to move
            if direction == "U":
                logging.info("Moving up")
                session_state.blue_car['lat'] = session_state.blue_car['lat']+step_size/3500.0

            if direction == "D":
                logging.info("Moving down")
                session_state.blue_car['lat'] = session_state.blue_car['lat']-step_size/3500.0

            if direction == "L":
                logging.info("Moving left")
                session_state.blue_car['lon'] = session_state.blue_car['lon']-step_size/3500.0

            if direction == "R":
                logging.info("Moving right")
                session_state.blue_car['lon'] = session_state.blue_car['lon']+step_size/3500.0

            render_map(session_state, indi_ed_lat, indi_ed_lon, image)
            # wait 0.5 seconds before taking the next movement
            time.sleep(0.5)


