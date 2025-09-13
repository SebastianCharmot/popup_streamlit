import streamlit as st

if "player_name_dict" not in st.session_state:
    st.session_state.player_name_dict = {}

print(st.session_state)

with st.form(key="player_names_input"):
    for i in range(1,9):
        st.text_input(label=f"Player{i} Name",key=f"name_p{i}")
        st.session_state.player_name_dict[i] = name_p1

    st.form_submit_button(label="Submit")