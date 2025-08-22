from bs4 import BeautifulSoup, Comment
import requests
import re
import pandas as pd
import numpy as np
from io import StringIO
import os
#from pathlib import Path

#output_dir = "../../data/processed"

MAPPING_STANDARD = {
    'playing_time_mp': 'matches_played',
    'playing_time_starts': 'matches_started',
    'playing_time_min': 'minutes_played',
    'performance_gls': 'goals',
    'performance_ast': 'assists',
    'performance_g_pk': 'non_pen_goals',
    'performance_pk': 'pen_made',
    'performance_pkatt': 'pen_att',
    'performance_crdy': 'yellow_cards',
    'performance_crdr': 'red_cards',
    'expected_xg': 'xg',
    'expected_npxg': 'npxg',
    'expected_xag': 'xa',  # Note: Fbref's xAG is the best equivalent for xA
    'progression_prgc': 'prg_carries',
    'progression_prgp': 'prg_passes',
    'progression_prgr': 'prg_passes_received'
    }

MAPPING_SHOOTING = {
    'standard_gls': 'goals',
    'standard_sh': 'shots',
    'standard_sot': 'shots_on_target',
    'standard_dist': 'avg_shot_dist',
    'standard_pk': 'pen_made',
    'standard_pkatt': 'pen_att'
    # shots_freekicks is not directly available in this table
}

MAPPING_PASSING = {
    'total_cmp': 'pass_cmp',
    'total_att': 'pass_att',
    'total_totdist': 'total_pass_dist',
    'total_prgdist': 'prg_pass_dist',
    'short_cmp': 'passes_short_cmp',
    'short_att': 'passes_short_att',
    'medium_cmp': 'passes_med_cmp',
    'medium_att': 'passes_med_att',
    'long_cmp': 'passes_long_cmp',
    'long_att': 'passes_long_att',
    'ast': 'assists',
    'kp': 'key_passes',
    '1/3': 'passes_final_3rd',
    'ppa': 'passes_pen_area',
    'crspa': 'crosses_pen_area'
    # prg_passes is in the 'standard' table
}

MAPPING_PASSING_TYPES = {
    'pass_types_live': 'passes_live_ball',
    'pass_types_dead': 'passes_dead_ball',
    'pass_types_fk': 'passes_freekicks', # Assuming FK is freekick passes
    'pass_types_tb': 'passes_through_ball',
    'pass_types_sw': 'passes_switches',
    'pass_types_crs': 'passes_cross',
    'outcomes_cmp': 'pass_cmp' # Redundant but available
}

MAPPING_GCA = {
    'sca_sca': 'sca',
    'sca_types_passlive': 'sca_passes_live',
    'sca_types_passdead': 'sca_passes_dead',
    'sca_types_to': 'sca_takeons', # TO on Fbref is "Take-on"
    'sca_types_sh': 'sca_shots',
    'sca_types_fld': 'sca_fouls_drawn',
    'sca_types_def': 'sca_def_actions',
    'gca_gca': 'gca',
    'gca_types_passlive': 'gca_passes_live',
    'gca_types_passdead': 'gca_passes_dead',
    'gca_types_to': 'gca_takeons',
    'gca_types_sh': 'gca_shots',
    'gca_types_fld': 'gca_fouls_drawn',
    'gca_types_def': 'gca_def_actions'
}

MAPPING_DEFENSE = {
    'tackles_tkl': 'tackles',
    'tackles_tklw': 'tackles_won',
    'tackles_def_3rd': 'tackles_def_third',
    'tackles_mid_3rd': 'tackles_mid_third',
    'tackles_att_3rd': 'tackles_atk_third',
    'challenges_tkl': 'dribblers_tackled_won',
    'challenges_att': 'tackles_total_dribblers', # Att is total dribblers challenged
    'challenges_lost': 'dribblers_tackled_lost',
    'blocks_blocks': 'blocks',
    'blocks_sh': 'block_shots',
    'blocks_pass': 'block_passes',
    'int': 'interceptions',
    'clr': 'clearances',
    'err': 'errors_to_shots'
}

MAPPING_POSSESSION = {
    'touches_touches': 'touches',
    'touches_def_pen': 'touches_def_pen_area',
    'touches_def_3rd': 'touches_def_3rd',
    'touches_mid_3rd': 'touches_mid_3rd',
    'touches_att_3rd': 'touches_atk_3rd',
    'touches_att_pen': 'touches_atk_pen_area',
    'take-ons_att': 'takeons_att',
    'take-ons_succ': 'takeons_successful',
    'take-ons_tkld': 'tackled_during_takeons',
    'carries_carries': 'carries',
    'carries_totdist': 'total_carry_dist',
    'carries_prgdist': 'prg_carry_dist',
    'carries_prgc': 'prg_carries', # This is also in the standard table
    'carries_1/3': 'carries_final_third',
    'carries_cpa': 'carries_pen_area',
    'carries_mis': 'miscontrols',
    'carries_dis': 'dispossessed',
    'rec': 'passes_received'
}

MAPPING_PLAYING_TIME = {
    'playing_time_mp': 'matches_played',
    'playing_time_min': 'minutes_played',
    'starts_starts': 'matches_started'
    # Other columns are interesting but not in your DBML schema
}

MAPPING_MISC = {
    'performance_crdy': 'yellow_cards',
    'performance_crdr': 'red_cards',
    'performance_fls': 'fouls_committed',
    'performance_fld': 'fouls_drawn',
    'performance_off': 'offside',
    'performance_crs': 'crosses',
    'performance_pkwon': 'pen_won',
    'performance_pkcon': 'pen_conceded',
    'performance_og': 'own_goals',
    'performance_recov': 'ball_recoveries',
    'aerial_duels_won': 'aerial_duels_won',
    'aerial_duels_lost': 'aerial_duels_lost'
}

MAPPING_KEEPER = {
    'playing_time_mp': 'matches_played',
    'playing_time_starts': 'matches_started',
    'playing_time_min': 'minutes_played',
    'performance_ga': 'goals_against_gk',
    'performance_sota': 'shots_on_target_against_gk',
    'performance_saves': 'shots_saved_gk',
    'performance_cs': 'clean_sheets_gk',
    'penalty_kicks_pkatt': 'pen_att_gk',
    'penalty_kicks_pka': 'pen_allowed_gk',
    'penalty_kicks_pksv': 'pen_saved_gk',
    'penalty_kicks_pkm': 'pen_missed_against_gk'
}

MAPPING_KEEPER_ADV = {
    'goals_ga': 'goals_against_gk',
    'goals_pka': 'pen_allowed_gk',
    'goals_fk': 'freekick_goals_against_gk',
    'goals_ck': 'cornerkick_goals_against_gk',
    'goals_og': 'own_goals_scored_against_gk',
    'expected_psxg': 'psxg_gk',
    'launched_cmp': 'launched_passes_cmp_gk',
    'launched_att': 'launched_passes_att_gk',
    'passes_att_(gk)': 'passes_att_gk',
    'passes_thr': 'throws_att_gk',
    'passes_avglen': 'avg_passes_dist_gk',
    'goal_kicks_att': 'goal_kicks_att_gk',
    'goal_kicks_avglen': 'avg_goal_kick_dist_gk',
    'crosses_opp': 'crosses_faced_gk',
    'crosses_stp': 'crosses_stopped_gk',
    'sweeper_#opa': 'def_actions_outside_box_gk',
    'sweeper_avgdist': 'avg_def_actions_dist_gk'
}

# --- Master Dictionary to select the correct mapping ---
PLAYER_STAT_MAPPINGS = {
    'standard': MAPPING_STANDARD,
    'shooting': MAPPING_SHOOTING,
    'passing': MAPPING_PASSING,
    'passing_types': MAPPING_PASSING_TYPES,
    'gca': MAPPING_GCA,
    'defense': MAPPING_DEFENSE,
    'possession': MAPPING_POSSESSION,
    'playing_time': MAPPING_PLAYING_TIME,
    'misc': MAPPING_MISC,
    'keeper': MAPPING_KEEPER,
    'keeper_adv': MAPPING_KEEPER_ADV
}

# --- Mapping for the Team Stats Table ---
TEAM_STAT_MAPPING = {
    'squad': 'club_name',
    '#_pl': 'squad_size',
    'age': 'avg_age',
    'poss': 'avg_possession',
    'performance_gls': 'goals',
    'performance_ast': 'assists',
    'performance_pk': 'pen_made',
    'expected_xg': 'xg',
    'expected_npxg': 'npxg'
}





def parse_table_from_html(
        html_content:str, 
        div_id:str)-> str:

    if not html_content:
        print("Error: HTML content is empty.")
        return None
    
    soup = BeautifulSoup(html_content, features= 'html.parser')

    div_data = soup.find('div', id=div_id)
    if not div_data:
        print(f"Div with id= '{div_id}' not found.")
        return None
        
    table = div_data.find('table')
    if table:
        print(f"Table found directly in div ='{div_id}'")
        return StringIO(str(table))  
    print(f"No direct table in '{div_id}. Checking for commented-out tables..")

    comments= div_data.find_all(string=lambda text:isinstance(text,Comment))
    for comment in comments:
        if '<table'in comment:
            comment_soup = BeautifulSoup(comment, 'html.parser')
            comment_table = comment_soup.find('table')
            if comment_table:
                print(f"Table found inside a comment in div='{div_id}'")
                return StringIO(str(comment_table))
            else:
                print(f"No table could be found in div='{div_id}', either directly or in comments")
                return None 


def clean_player_dataframe(table:pd.DataFrame,
                       stat_type:str) -> pd.DataFrame:
    
    if not isinstance(table, pd.DataFrame) or table.empty:
        print(f"Empty or invalid Dataframe provided for stat_type '{stat_type}'.")
        return pd.DataFrame()
    
    df = table.copy()

    #merge multi-index header
    df.columns = [
        f'{col[0].lower()}_{col[1].lower()}' if 'Unnamed:' not in col[0] else col[1].lower() for col in table.columns
        ]
    
    df.columns = [
        col.replace(' ','_').replace('+','plus').replace('-','_').replace('.','') 
        for col in df.columns
        ]
    
    
    if stat_type not in PLAYER_STAT_MAPPINGS:
        raise ValueError(f"Unknown stat_type: '{stat_type}'. No mapping found.")
    
    mapping = PLAYER_STAT_MAPPINGS[stat_type]

    df.rename(columns=mapping, inplace=True)

    final_db_columns = list(mapping.values())
    base_player_info = ['player', 'nation', 'pos', 'squad', 'age', 'born', '90s']

    cols_to_keep = [col for col in final_db_columns if col in df.columns]
    base_cols_to_keep = [col for col in base_player_info if col in df.columns]
    
    df = df[base_cols_to_keep + cols_to_keep]
    #df = df[df['player'] != 'Player'].copy()
    i = df[df['player'] == 'Player'].index
    df.drop(i, inplace=True)


    if 'player' in df.columns:
        #df = df[df['player'] != 'Player'].copy()
        name_split = df['player'].str.split(' ', n=1, expand=True)
        df['firstname'] = name_split[0]
        df['lastname'] = name_split[1]
        df['lastname'] = df['lastname'].fillna(df['firstname'])#,inplace=True)
        df.drop(columns=['player'], inplace=True)

    if 'nation' in df.columns:
        df['nation'] = df['nation'].str.split().str[-1]

    if 'pos' in df.columns:
        df['pos'] = df['pos'].str.split(',').str[0]

    if 'born' in df.columns:
        df['born'] = pd.to_datetime(df['born'],format='%Y', errors='coerce')
    
    df.drop(columns=['rk','matches'], inplace=True,errors='ignore')

    known_string_cols = ['firstname', 'lastname', 'nation', 'pos', 'squad']

    for col in df.columns:
        if col not in known_string_cols:
            if df[col].dtype == 'object':
                df[col] = pd.to_numeric(df[col], errors= 'coerce')


    # for col in df.select_dtypes(include=['object']).columns:
    #     df[col] = pd.to_numeric(df[col], errors= 'coerce')

    df.reset_index(drop=True, inplace=True)

    return df


def clean_team_dataframe(table: pd.DataFrame) -> pd.DataFrame:

    if not isinstance(table, pd.DataFrame) or table.empty:
        print(f"Empty or invalid Dataframe provided for team cleaning'.")
        return pd.DataFrame()
    
    df = table.copy()

    #merge multi-index header
    df.columns = [
        f'{col[0].lower()}_{col[1].lower()}' if 'Unnamed:' not in col[0] else col[1].lower() for col in table.columns
        ]
    
    df.columns = [
        col.replace(' ','_').replace('+','plus').replace('-','_').replace('.','') 
        for col in df.columns
        ]

    df.rename(columns= TEAM_STAT_MAPPING, inplace=True)

    final_db_columns = list(TEAM_STAT_MAPPING.values())
    cols_to_keep = [col for col in df.columns if col in final_db_columns]
    df = df[cols_to_keep]

    for col in df.columns:
        if col != 'club_name':
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df.fillna(0, inplace=True)

    for col in df.select_dtypes(include=['float']).columns:
        if (df[col]==df[col].astype(int)).all():
            df[col] = df[col].astype(int)

    return df

