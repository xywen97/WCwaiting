import streamlit as st
import time
import numpy as np
from toilet_sim import ToiletSimStep

st.title("Restroom Queue Simulation and Visualization")

# Add time variation controls
st.sidebar.header("Time Variation Settings")
enable_time_variation = st.sidebar.checkbox("Enable Time Variation", value=False)
time_variation_std = st.sidebar.slider("Time Variation Standard Deviation (seconds)", 1, 30, 5, disabled=not enable_time_variation)

params = {
    'n_male': st.slider('Number of male stalls', 1, 10, 3),
    'n_female': st.slider('Number of female stalls', 1, 10, 3),
    'arrival_interval': st.slider('Average arrival interval (seconds)', 5, 60, 20),
    'female_ratio': st.slider('Female ratio', 0.1, 0.9, 0.5),
    'male_pee_time': st.slider('Male urination average time (seconds)', 10, 120, 20),
    'male_poop_time': st.slider('Male defecation average time (seconds)', 30, 1800, 60),
    'male_poop_prob': st.slider('Male defecation probability', 0.05, 0.3, 0.1),
    'female_pee_time': st.slider('Female urination average time (seconds)', 20, 300, 40),
    'female_poop_time': st.slider('Female defecation average time (seconds)', 60, 1800, 90),
    'female_poop_prob': st.slider('Female defecation probability', 0.05, 0.3, 0.1),
    'sim_time': st.slider('Total simulation time (seconds)', 600, 18000, 3600),
    'enable_time_variation': enable_time_variation,
    'time_variation_std': time_variation_std
}

if st.button('Start Simulation'):
    sim = ToiletSimStep(params['n_male'], params['n_female'], params)
    status_placeholder = st.empty()
    queue_placeholder = st.empty()
    while not sim.finished:
        sim.step()
        status = sim.get_status()
        # Display stall status
        with status_placeholder.container():
            st.write(f"Current time: {status['now']:.1f} seconds")
            st.write("Male restroom stall status:")
            cols = st.columns(params['n_male'])
            for i, s in enumerate(status['male_status']):
                cols[i].write("Occupied" if s else "Available")
            st.write("Female restroom stall status:")
            cols = st.columns(params['n_female'])
            for i, s in enumerate(status['female_status']):
                cols[i].write("Occupied" if s else "Available")
        # Display queue length
        with queue_placeholder.container():
            st.metric("Male queue length", status['male_queue_len'])
            st.metric("Female queue length", status['female_queue_len'])
        time.sleep(0.05)
    st.success("Simulation completed!") 