import streamlit as st

if "player_name_dict" not in st.session_state:
    st.session_state.player_name_dict = {}

print(st.session_state)

def pop_p_names_dict(names):
    id = 1
    for p_name in names:
        st.session_state.player_name_dict[id] = p_name
        id +=1

with st.form(key="player_names_input"):
    p_names = []
    for i in range(1,9):
        p_names.append(st.text_input(label=f"Player{i} Name",key=f"name_p{i}"))

    st.form_submit_button(label="Submit",key='player_name_form_button',on_click=pop_p_names_dict)
