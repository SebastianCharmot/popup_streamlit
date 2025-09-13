import streamlit as st
import pandas as pd

if "player_name_dict" not in st.session_state:
    st.session_state.player_name_dict = {}
if "player_name_form_button" not in st.session_state:
    st.session_state.player_name_form_button = False
if "scores" not in st.session_state:
    st.session_state.scores = {}
if "progress" not in st.session_state:
    st.session_state.progress = []

print("session state start: ", st.session_state)

def update_session(names):
    id = 1
    for p_name in names:
        st.session_state.player_name_dict[id] = p_name
        st.session_state.scores[f"p{id}_wins"] = [0,] * 7
        st.session_state.scores[f"p{id}_p_for"] = [0,] * 7
        st.session_state.scores[f"p{id}_diff"] = [0,] * 7
        id += 1

    # st.session_state.player_name_form_button = True

with st.form(key="player_names_input"):
    p_names = []
    for i in range(1, 9):
        p_names.append(st.text_input(label=f"Player{i} Name", key=f"name_p{i}"))

    if st.form_submit_button(label="Submit"):
        update_session(p_names)

def get_player_name(player_id):
    return st.session_state.player_name_dict.get(player_id, f"Player {player_id}")

def match_form(round_number, team1, team2, team3, team4):
    with st.form(key=f"round_form_{round_number}"):
        st.header(f"Round {round_number}")
        col1, col2 = st.columns(2)

        with col1:
            team1_names = " + ".join(get_player_name(pid) for pid in team1)
            team2_names = " + ".join(get_player_name(pid) for pid in team2)
            st.write(f"{team1_names} vs. {team2_names}")
            score1 = st.number_input(label=f"Score for {team1_names}", key=f"score_{round_number}_1", min_value=0)
            score2 = st.number_input(label=f"Score for {team2_names}", key=f"score_{round_number}_2", min_value=0)

        with col2:
            team3_names = " + ".join(get_player_name(pid) for pid in team3)
            team4_names = " + ".join(get_player_name(pid) for pid in team4)
            st.write(f"{team3_names} vs. {team4_names}")
            score3 = st.number_input(label=f"Score for {team3_names}", key=f"score_{round_number}_3", min_value=0)
            score4 = st.number_input(label=f"Score for {team4_names}", key=f"score_{round_number}_4", min_value=0)

        submitted = st.form_submit_button(label="Submit")
        if submitted:
            # update team1 and team2 
            if score1 > score2:
                for pid in team1:
                    st.session_state.scores[f"p{pid}_wins"][round_number - 1] = 1
            elif score2 > score1:
                for pid in team2:
                    st.session_state.scores[f"p{pid}_wins"][round_number - 1] = 1
            for pid in team1:
                st.session_state.scores[f"p{pid}_p_for"][round_number - 1] = score1
                st.session_state.scores[f"p{pid}_diff"][round_number - 1] = score1 - score2
            for pid in team2:
                st.session_state.scores[f"p{pid}_p_for"][round_number - 1] = score2
                st.session_state.scores[f"p{pid}_diff"][round_number - 1] = score2 - score1
            
            # update team3 and team4
            if score3 > score4:
                for pid in team3:
                    st.session_state.scores[f"p{pid}_wins"][round_number - 1] = 1
            elif score4 > score3:
                for pid in team4:
                    st.session_state.scores[f"p{pid}_wins"][round_number - 1] = 1
            for pid in team3:
                st.session_state.scores[f"p{pid}_p_for"][round_number - 1] = score3
                st.session_state.scores[f"p{pid}_diff"][round_number - 1] = score3 - score4
            for pid in team4:
                st.session_state.scores[f"p{pid}_p_for"][round_number - 1] = score4
                st.session_state.scores[f"p{pid}_diff"][round_number - 1] = score4 - score3

def get_standings_df():

    data = []
    for pid in range(1, 9):
        name = st.session_state.player_name_dict.get(pid, f"Player {pid}")
        wins = sum(st.session_state.scores[f"p{pid}_wins"])
        p_for = sum(st.session_state.scores[f"p{pid}_p_for"])
        diff = sum(st.session_state.scores[f"p{pid}_diff"])
        data.append({
            "Player": name,
            "Wins": wins,
            "Point Difference": diff,
            "Points For": p_for
        })
    df = pd.DataFrame(data)
    df = df.sort_values(by=["Wins", "Point Difference", "Points For"], ascending=False).reset_index(drop=True)
    df.index += 1  # Start index at 1 for ranking
    return df

def add_player_to_team(team, player_name):
    selected_pid = next(
        pid for pid, name in st.session_state.player_name_dict.items()
        if name == player_name
    )
    st.session_state.playoff_teams[team].append(selected_pid)
    st.session_state.drafted_players.append(selected_pid)

def reset_draft():
    st.session_state.drafted_players = []
    st.session_state.playoff_teams = {1: [], 2: [], 3: [], 4: []}

def draft_playoff_teams():
    if "drafted_players" not in st.session_state:
        st.session_state.drafted_players = []
    if "playoff_teams" not in st.session_state:
        st.session_state.playoff_teams = {1: [], 2: [], 3: [], 4: []}

    st.subheader("Draft Playoff Teams")

    # Add Redraft button
    st.button("Redraft", on_click=reset_draft)

    available_players = [
        pid for pid in st.session_state.player_name_dict.keys()
        if pid not in st.session_state.drafted_players
    ]

    for team in range(1, 5):
        if len(st.session_state.playoff_teams[team]) < 2:
            if st.session_state.playoff_teams[team]:
                player_names = [get_player_name(pid) for pid in st.session_state.playoff_teams[team]]
                st.write(f"Team {team}: {', '.join(player_names)}")
            else:
                st.write(f"Team {team}")
            player = st.selectbox(
                f"Select player for Team {team}",
                options=[get_player_name(pid) for pid in available_players],
                key=f"draft_team_{team}_player_{len(st.session_state.playoff_teams[team]) + 1}"
            )
            st.button(
                f"Add to Team {team}",
                key=f"add_team_{team}_player_{len(st.session_state.playoff_teams[team]) + 1}",
                on_click=add_player_to_team,
                args=(team, player)
            )

    st.write("Playoff Teams:")
    for team, players in st.session_state.playoff_teams.items():
        player_names = [get_player_name(pid) for pid in players]
        st.write(f"Team {team}: {', '.join(player_names)}")

def playoff_form(team1, team2, team3, team4):

    if "gold_medal_teams" not in st.session_state:
        st.session_state.gold_medal_teams = []
    if "bronze_medal_teams" not in st.session_state:
        st.session_state.bronze_medal_teams = []
    if "playoff_scores" not in st.session_state:
        st.session_state.playoff_scores = {}

    with st.form(key=f"playoff_form"):
        st.header(f"Semifinals Playoff") 
        col1, col2 = st.columns(2)

        with col1:
            team1_names = " + ".join(get_player_name(pid) for pid in team1)
            team2_names = " + ".join(get_player_name(pid) for pid in team2)
            st.write(f"{team1_names} vs. {team2_names}")
            score1 = st.number_input(label=f"Score for {team1_names}", key=f"score_playoff_1", min_value=0)
            score2 = st.number_input(label=f"Score for {team2_names}", key=f"score_playoff_2", min_value=0)

        with col2:
            team3_names = " + ".join(get_player_name(pid) for pid in team3)
            team4_names = " + ".join(get_player_name(pid) for pid in team4)
            st.write(f"{team3_names} vs. {team4_names}")
            score3 = st.number_input(label=f"Score for {team3_names}", key=f"score_playoff_3", min_value=0)
            score4 = st.number_input(label=f"Score for {team4_names}", key=f"score_playoff_4", min_value=0)

        submitted = st.form_submit_button(label="Submit")
        if submitted:
            # update team1 and team2 
            if score1 > score2:
                st.session_state.gold_medal_teams[0] = team1
                st.session_state.bronze_medal_teams[0] = team2
            else:
                st.session_state.gold_medal_teams[0] = team2
                st.session_state.bronze_medal_teams[0] = team1

            if score3 > score4:
                st.session_state.gold_medal_teams[0] = team3
                st.session_state.bronze_medal_teams[0] = team4
            else:
                st.session_state.gold_medal_teams[0] = team4
                st.session_state.bronze_medal_teams[0] = team3
            st.session_state.playoff_scores = {
                "semifinal_1": (score1, score2),
                "semifinal_2": (score3, score4)
            }

def playoffs():
    if "playoff_teams" in st.session_state and all(len(team) == 2 for team in st.session_state.playoff_teams.values()):
        playoff_form(
            team1=st.session_state.playoff_teams[1],
            team2=st.session_state.playoff_teams[4],
            team3=st.session_state.playoff_teams[2],
            team4=st.session_state.playoff_teams[3]
        )

# Generate match forms
if "player_name_dict" in st.session_state and st.session_state.player_name_dict:
    match_form(round_number=1,team1=[1,5], team2=[7,8], team3=[2,3], team4=[4,6])
    match_form(round_number=2,team1=[4,7], team2=[6,8], team3=[1,2], team4=[3,5])
    # match_form(round_number=3,team1=[3,4], team2=[5,7], team3=[2,6], team4=[1,8])
    # match_form(round_number=4,team1=[1,6], team2=[4,5], team3=[3,7], team4=[2,8])
    # match_form(round_number=5,team1=[5,6], team2=[7,2], team3=[1,4], team4=[3,8])
    # match_form(round_number=6,team1=[4,8], team2=[2,5], team3=[6,7], team4=[1,3])
    # match_form(round_number=7,team1=[1,7], team2=[2,4], team3=[3,6], team4=[5,8])

    st.subheader("Standings")
    standings_df = get_standings_df()
    st.dataframe(standings_df)

    draft_playoff_teams()

    playoffs()

# Playoffs 


print("session state end: ", st.session_state)

# if "player_name_form_button" in st.session_state and st.session_state.player_name_form_button:
#     st.write("Player Names:", st.session_state.player_name_dict)
#     st.write("Scores:", st.session_state.scores)
#     st.write("Progress:", st.session_state.progress)

