from data_collection.data_preprocessing import parse_table_from_html
import os 
from pathlib import Path

script_file_path =Path(__file__).resolve()
script_file_dir = script_file_path.parent
project_root = script_file_dir.parent #.parent #might need to remove one parent, we step up a folder

html_pages_dir=project_root/"data"/"raw"
html_pages_filename_list = os.listdir(html_pages_dir) # ->list

html_pages_filepath = os.path.join(html_pages_dir,html_pages_filename_list[0])
#pages= open(page)

stats_name_list = [
    'standard', 'shooting', 'keeper',
    'passing','keeper_adv','passing_types',
    'gca','defense','possession',
    'playing_time','misc'
              ]

# stat_name=None
# div_id_squad = f"all_stats_squad_{stat_name}"
# div_id_players = f"all_stats_{stat_name}"

#still need to figure out a smarter way to switch between searching for player and squad data
#right now I only need standard stats for squad data

for stat_name in stats_name_list:
    div_id = f"all_stats_{stat_name}"
    print(div_id)

    table_players_stats = parse_table_from_html(html_page=pages,
                                                div_id=div_id
                                                )
    
    print(f"Table data type:  {type(table_players_stats)}")
