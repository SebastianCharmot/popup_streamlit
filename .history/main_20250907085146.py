import streamlit as st

if "player_name_dict" not in st.session_state:
    st.session_state.player_name_dict = {}

print(st.session_state)

with st.form(key="player_names_input"):
    name_p1 = st.text_input(label="Player1 Name",key="name_p1")
    st.session_state.player_name_dict[1] = name_p1