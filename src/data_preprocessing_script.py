from data_collection.data_preprocessing import parse_table_from_html, clean_player_dataframe, clean_team_dataframe
from data_collection.data_collection import stat_tables
import os 
import pandas as pd
from pathlib import Path

script_file_path =Path(__file__).resolve()
script_file_dir = script_file_path.parent
project_root = script_file_dir.parent 

html_pages_dir=project_root/"data"/"raw"
html_pages_filename_list = os.listdir(html_pages_dir) # ->list




for html_page in html_pages_filename_list:
    html_filepath = os.path.join(html_pages_dir,html_page)

    with open(html_filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()


    html_name = html_filepath.replace('.html','')
    html_tags= html_name.split('_')
    print(html_tags)
    for word in html_tags:
        if word in stat_tables:
            stat_type_tag = html_tags[-1]
        elif f"{html_tags[-2]}_{html_tags[-1]}" in stat_tables:
            stat_type_tag = f"{html_tags[-2]}_{html_tags[-1]}"
        else:
            pass


    print(f"-> Processing File: {html_page} | Stat Type: {stat_type_tag} ..")
    #print(f'{html_filepath}')

    if stat_type_tag == 'stats':

        stat_type_tag='standard'

        div_id_team = f'all_stats_squads_{stat_type_tag}'
        print(f"Attempting to parse squad data from div_id= '{div_id_team}' ..")
        data_table_team = parse_table_from_html(html_content=html_content,
                                                div_id=div_id_team
                                                )
        if data_table_team:
            print("Squad data successfully retrieved")
        
        print(f"--- Cleaning Columns for {stat_type_tag} ---")
        team_table = pd.read_html(data_table_team, header=[0, 1])[0]
        team_df = clean_team_dataframe(table=team_table)
        print(f"Check cleaning: {team_df.info()}")
        # print(f'Preview dataframe: {print(team_df.head(2))}')

        div_id_players = f'all_stats_{stat_type_tag}'
        print(f"\nAttempting to parse player data from div_id= '{div_id_players}' ..")
        data_table_players = parse_table_from_html(html_content=html_content,
                                                    div_id= div_id_players
                                                    )

        if data_table_players:
            print("Player data successfully retrieved.")
        print(f"--- Cleaning Columns for {stat_type_tag} ---")
        players_table = pd.read_html(data_table_players, header=[0, 1])[0]
        players_df = clean_player_dataframe(table=players_table, stat_type=stat_type_tag)
        print(f"Check cleaning: {players_df.info()}")
        # print(f'Preview dataframe: {print(players_df.head(2))}')
        
    else:
        if stat_type_tag =="keepersadv":
            stat_type_tag="keeper_adv"
        elif stat_type_tag=="playingtime":
            stat_type_tag="playing_time"
        elif stat_type_tag=="keepers":
            stat_type_tag="keeper"

        div_id_players = f'all_stats_{stat_type_tag}'
        print(f"Attempting to parse player data from div_id='{div_id_players}'..")
        data_table_players = parse_table_from_html(html_content=html_content,
                                                    div_id= div_id_players
                                                    )

        if data_table_players:
            print("Player data successfully retrieved")
        
        print(f"--- Cleaning Columns for {stat_type_tag} ---")
        players_table = pd.read_html(data_table_players, header=[0, 1])[0]
        players_df = clean_player_dataframe(table=players_table, stat_type=stat_type_tag)
        print(f"Check cleaning: {players_df.info()}")
        # print(f'Preview dataframe: {players_df.head(2)}')
        
        

    print(f"-> Finished processing {html_page}\n")