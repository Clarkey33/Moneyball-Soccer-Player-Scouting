from data_collection.data_preprocessing import parse_table_from_html, clean_player_dataframe, clean_team_dataframe, merge_player_dataframes
from etl_fbref import stat_tables
import os 
import pandas as pd 
from pathlib import Path

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)

script_file_path =Path(__file__).resolve()
script_file_dir = script_file_path.parent
project_root = script_file_dir.parent 

html_pages_dir=project_root/"data"/"raw"
html_pages_filename_list = os.listdir(html_pages_dir) # ->list

processed_data_dir = project_root/"data"/"processed"
player_output_dir = processed_data_dir/"player_stats"
team_output_dir = processed_data_dir/"team_stats"

player_data_groups = {}
team_data_groups ={}

print("-> Commencing Phase 1: Cleaning and Grouping Files")
for html_page in html_pages_filename_list:
    if not html_page.endswith('.html'):
        continue

    html_parts = html_page.replace(".html","").split("_")
    season_id= html_parts[0]

    stat_type=None
    league_name_parts=[]
    for i in range(len(html_parts)-1,0,-1):
        potential_stat= "_".join(html_parts[i:])
        if potential_stat in stat_tables:
            stat_type=potential_stat
            league_name_parts=html_parts[1:i]
            break
    if not stat_type:
        print(f"Error: Could not determine stat type for {html_page}")
        continue

    #stat_type= html_parts[-1]
    league_name =  "_".join(league_name_parts)

    group_key= f"{league_name}_{season_id}"

    print(f"-> Processing: {html_page} | Season: {season_id} | Group: {group_key} | Stat: {stat_type}")
    html_filepath = os.path.join(html_pages_dir,html_page)
    with open(html_filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()

    if stat_type == 'stats':
        stat_type = 'standard'

        div_id_team = f'all_stats_squads_{stat_type}'
        print(f"Attempting to parse squad data from div_id= '{div_id_team}' ..")
        data_table_team = parse_table_from_html(html_content=html_content,
                                                div_id=div_id_team
                                                )
        if data_table_team:
            print("Squad data successfully retrieved")
        
        print(f"--- Cleaning Columns for {stat_type} ---")
        team_table = pd.read_html(data_table_team, header=[0, 1])[0]
        team_df = clean_team_dataframe(table=team_table)
        # print(f"Check cleaning:\n{team_df.info()}")
        # print(f'Preview dataframe:\n{team_df.head(2)}')
        team_data_groups.setdefault(group_key, []).append(team_df)

        div_id_players = f'all_stats_{stat_type}'
        print(f"\nAttempting to parse player data from div_id= '{div_id_players}' ..")
        data_table_players = parse_table_from_html(html_content=html_content,
                                                    div_id= div_id_players
                                                    )

        if data_table_players:
            print("Player data successfully retrieved.")
        print(f"--- Cleaning Columns for {stat_type} ---")
        players_table = pd.read_html(data_table_players, header=[0, 1])[0]
        players_df = clean_player_dataframe(table=players_table, stat_type=stat_type)
        # print(f"Check cleaning:\n{players_df.info()}")
        # print(f'Preview dataframe:\n{players_df.head(2)}')
        player_data_groups.setdefault(group_key, []).append(players_df)
        
    else:
        if stat_type == "keepersadv":
            stat_type = "keeper_adv"
        elif stat_type == "playingtime":
            stat_type = "playing_time"
        elif stat_type == "keepers":
            stat_type = "keeper"

        div_id_players = f'all_stats_{stat_type}'
        print(f"Attempting to parse player data from div_id='{div_id_players}'..")
        data_table_players = parse_table_from_html(html_content=html_content,
                                                    div_id= div_id_players
                                                    )

        if data_table_players:
            print("Player data successfully retrieved")
        
        print(f"--- Cleaning Columns for {stat_type} ---")
        players_table = pd.read_html(data_table_players, header=[0, 1])[0]
        players_df = clean_player_dataframe(table=players_table, stat_type=stat_type)
        # print(f"Check cleaning:\n{players_df.info()}")
        # print(f'Preview dataframe:\n{players_df.head(2)}')
        player_data_groups.setdefault(group_key, []).append(players_df)
        
    print(f"-> Finished processing {html_page}\n")
print("\n -> Phase 1 Complete. All files cleaned and grouped.")
print(f"Found {len(player_data_groups)} groups: {list(player_data_groups.keys())}")
print(f"Found {len(team_data_groups)} groups: {list(team_data_groups.keys())}")

print("-> Commencing Phase 2: Merging DataFrames for Each Group")

final_player_dfs = []
for group_key, list_of_dfs in team_data_groups.items():

    team_df = list_of_dfs[0]
    league_name, season_id = group_key.rsplit('_',1)
    team_df['season_id'] = season_id
    team_df['competition_name'] = league_name.replace('_',' ')
    print(f"\nSaving Team data for group: {group_key} | Shape: {team_df.shape}")

for group_key, list_of_dfs in player_data_groups.items():
    print(f"\nMerging {len(list_of_dfs)} tables for group: {group_key}")
    master_df = merge_player_dataframes(list_of_dfs=list_of_dfs)

    master_df = master_df.copy()

    league_name, season_id = group_key.rsplit('_',1)
    master_df['season_id'] = season_id
    master_df['competition_name'] = league_name.replace('_',' ')
    final_player_dfs.append(master_df)

    print(f"Finished merging for {group_key}. Final shape: {master_df.shape}")
    print("Preview of merged data:")
    print(master_df.head(3))
    print(master_df.info())

print("\n-> Phase 2 Complete. ETL process finished.")

print("->Commencing Phase 3: Staging Files to Processed Directory")

print(f"\nOutput directory set to: {processed_data_dir}")
print(f"\nSaving {len(final_player_dfs)} merged player dataframes..")

for player_master_df in final_player_dfs:
    if player_master_df.empty:
        print("Skipping none or empty player Dataframe")
        continue
    try:
        competition = player_master_df['competition_name'].iloc[0]
        season = player_master_df['season_id'].iloc[0]
    except(KeyError,IndexError):
        print("Warning: Could not determine Competion and Season for player Dataframe")
        continue

    competition_folder_name = competition.lower().replace(' ','_')
    partition_path = player_output_dir/f"competition_name={competition_folder_name}"/f"season_id={season}"
    partition_path.mkdir(parents=True,exist_ok=True)
    file_path = partition_path/"data.parquet"

    try:
        player_master_df.to_parquet(file_path,
                                    index=False,
                                    engine='pyarrow')
        print(f"Succesfully saved player data to: {file_path}")
    except Exception as e:
        print(f"Error: Could not save player file to {file_path} | reason: {e}")

print(f"\nSaving{len(team_data_groups)} team dataframes..")
for group_key, list_of_team_dfs in team_data_groups.items():
    if not list_of_team_dfs:
        print("skipping empty team data list for group: {group_key}")
        continue

    team_df= list_of_team_dfs[0]

    try:
        competition = team_df['competition_name'].iloc[0]
        season= team_df['season_id'].iloc[0]
    except(KeyError,IndexError):
        print(f"Warning: could not determine competition or season for team dataframe: {group_key}.Skipping.")
        continue

    competition_folder_name = competition.lower().replace(' ','_')
    partition_path = team_output_dir/f"competition_name={competition_folder_name}"/f"season_id={season}"
    partition_path.mkdir(parents=True, exist_ok=True)

    file_path = partition_path/"data.parquet"

    try:
        team_df.to_parquet(file_path, index=False, engine='pyarrow')
        print(f"Succesfully saved team data to: {file_path}")
    except Exception as e:
        print(f"Error: could not save file  to: {file_path} | reason: {e}")

print(f"\n-> Phase 3 complete. All data has been staged to the processed directory")