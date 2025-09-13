import streamlit as st

if "player_name_dict" not in st.session_state:
    st.session_state.player_name_dict = {}

print(st.session_state)

def re_run_callback():
    st.rerun()

with st.form(key="player_names_input"):
    for i in range(1,9):
        st.text_input(label=f"Player{i} Name",key=f"name_p{i}")

    st.form_submit_button(label="Submit",key='player_name_form_button',on_click=re_run_callback)
