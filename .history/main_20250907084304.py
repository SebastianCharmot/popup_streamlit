import streamlit as st

if "player_name_dict" not in st.session_state:
    st.session_state.player

with st.form(key="player_names_input"):
