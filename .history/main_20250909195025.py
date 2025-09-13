import streamlit as st

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


            # st.session_state.scores[f"p{id}_wins"] = [0,] * 7
            # st.session_state.scores[f"p{id}_p_for"] = [0,] * 7
            # st.session_state.scores[f"p{id}_diff"] = [0,] * 7

            # st.session_state.scores[f"match_{match_id}"] = {
            #     "round": round_number,
            #     team1: score1,
            #     team2: score2,
            #     team3: score3,
            #     team4: score4,
            # }
            # st.session_state.progress.append(f"Match {match_id} scores updated")
        # if submitted:
        #     st.session_state.scores[f"match_{match_id}"] = {
        #         "round": round_number,
        #         team1: score1,
        #         team2: score2,
        #         team3: score3,
        #         team4: score4,
        #     }
        #     st.session_state.progress.append(f"Match {match_id} scores updated")


# Generate match forms
if "player_name_dict" in st.session_state and st.session_state.player_name_dict:
    match_form(round_number=1,team1=[1,5], team2=[7,8], team3=[2,3], team4=[4,6])
    match_form(round_number=2,team1=[4,7], team2=[6,8], team3=[1,2], team4=[3,5])
    # match_form(round_number=3,team1=[3,4], team2=[5,7], team3=[2,6], team4=[1,8])
    # match_form(round_number=4,team1=[1,6], team2=[4,5], team3=[3,7], team4=[2,8])
    # match_form(round_number=5,team1=[5,6], team2=[7,2], team3=[1,4], team4=[3,8])
    # match_form(round_number=6,team1=[4,8], team2=[2,5], team3=[6,7], team4=[1,3])
    # match_form(round_number=7,team1=[1,7], team2=[2,4], team3=[3,6], team4=[5,8])

print("session state end: ", st.session_state)

def get_standings_df()

# if "player_name_form_button" in st.session_state and st.session_state.player_name_form_button:
#     st.write("Player Names:", st.session_state.player_name_dict)
#     st.write("Scores:", st.session_state.scores)
#     st.write("Progress:", st.session_state.progress)

