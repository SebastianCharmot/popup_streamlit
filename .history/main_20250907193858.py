import streamlit as st

if "player_name_dict" not in st.session_state:
    st.session_state.player_name_dict = {}
if "scores" not in st.session_state:
    st.session_state.scores = {}
if "progress" not in st.session_state:
    st.session_state.progress = []

print("session state start: ", st.session_state)

def update_session(names):
    id = 1
    for p_name in names:
        st.session_state.player_name_dict[id] = p_name
        id += 1
    st.session_state

def match_form(match_id, team1, team2, team3, team4, round_number):
    with st.form(key=f"match_form_{match_id}"):
        st.header(f"Round {round_number}")
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"{team1} vs {team2}")
            score1 = st.number_input(label=f"Score for {team1}", key=f"score_{match_id}_1", min_value=0)
            score2 = st.number_input(label=f"Score for {team2}", key=f"score_{match_id}_2", min_value=0)

        with col2:
            st.write(f"{team3} vs {team4}")
            score3 = st.number_input(label=f"Score for {team3}", key=f"score_{match_id}_3", min_value=0)
            score4 = st.number_input(label=f"Score for {team4}", key=f"score_{match_id}_4", min_value=0)

        submitted = st.form_submit_button(label="Submit")
        if submitted:
            st.session_state.scores[f"match_{match_id}"] = {
                "round": round_number,
                team1: score1,
                team2: score2,
                team3: score3,
                team4: score4,
            }
            st.session_state.progress.append(f"Match {match_id} scores updated")

with st.form(key="player_names_input"):
    p_names = []
    for i in range(1, 9):
        p_names.append(st.text_input(label=f"Player{i} Name", key=f"name_p{i}"))

    st.form_submit_button(
        label="Submit",
        key="player_name_form_button",
        on_click=lambda: update_session(p_names),
    )

# Generate match forms
if "player_name_dict" in st.session_state and st.session_state.player_name_dict:
    match_form(1, "Team 1", "Team 2", "Team 3", "Team 4", 1)
    match_form(2, "Winner Match 1", "Winner Match 2", "Loser Match 1", "Loser Match 2", 2)
    match_form(3, "Winner Match 3", "Winner Match 4", "Loser Match 3", "Loser Match 4", 3)
    match_form(4, "Final Winner", "Final Loser", "Third Place Winner", "Third Place Loser", 4)

print("session state end: ", st.session_state)

if "player_name_form_button" in st.session_state and st.session_state.player_name_form_button:
    st.write("Player Names:", st.session_state.player_name_dict)
    st.write("Scores:", st.session_state.scores)
    st.write("Progress:", st.session_state.progress)

