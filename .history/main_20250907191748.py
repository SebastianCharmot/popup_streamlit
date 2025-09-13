import streamlit as st

if "player_name_dict" not in st.session_state:
    st.session_state.player_name_dict = {}
if "scores" not in st.session_state:
    st.session_state.scores = {}
if "progress" not in st.session_state:
    st.session_state.progress = []

print("session state start: ", st.session_state)

def update_session(names, score1, score2):
    id = 1
    for p_name in names:
        st.session_state.player_name_dict[id] = p_name
        id += 1
    st.session_state.scores = {"team1_vs_team2": score1, "team3_vs_team4": score2}
    st.session_state.progress.append("Scores updated")

with st.form(key="player_names_input"):
    p_names = []
    for i in range(1, 9):
        p_names.append(st.text_input(label=f"Player{i} Name", key=f"name_p{i}"))

    score1 = st.number_input(label="Score for Team 1 vs Team 2", key="score1", min_value=0)
    score2 = st.number_input(label="Score for Team 3 vs Team 4", key="score2", min_value=0)

    st.form_submit_button(
        label="Submit",
        key="player_name_form_button",
        on_click=lambda: update_session(p_names, score1, score2),
    )

print("session state end: ", st.session_state)

if "player_name_form_button" in st.session_state and st.session_state.player_name_form_button:
    st.write("Player Names:", st.session_state.player_name_dict)
    st.write("Scores:", st.session_state.scores)
    st.write("Progress:", st.session_state.progress)

