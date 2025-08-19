from data_collection.data_preprocessing import parse_table_from_html
import os 
from pathlib import Path

script_file_path =Path(__file__).resolve()
script_file_dir = script_file_path.parent
project_root = script_file_dir.parent 

html_pages_dir=project_root/"data"/"raw"
html_pages_filename_list = os.listdir(html_pages_dir) # ->list




for html_page in html_pages_filename_list:
    html_filepath = os.path.join(html_pages_dir,html_page)
    html_name = html_filepath.replace('.html','')
    html_tags= html_name.split('_')
    stat_type_tag = html_tags[-1]


    if stat_type_tag == 'stats':
        stat_type_tag='standard'
        div_id_team = f'all_stats_squads_{stat_type_tag}'
        div_id_players = f'all_stats_{stat_type_tag}'

        data_table_team = parse_table_from_html(html_path=html_filepath,
                                            div_id=div_id_team
                                            )
        data_table_players = parse_table_from_html(html_path=html_filepath,
                                                    div_id= div_id_players
                                                    )
        
    elif stat_type_tag == 'keepersadv':
        stat_type_tag = 'keepers_adv'
        div_id_players = f'all_stats_{stat_type_tag}'
        data_table_players = parse_table_from_html(html_path=html_filepath,
                                                    div_id= div_id_players
                                                    )
        
    elif stat_type_tag == 'playingtime':
        stat_type_tag = 'playing_time'
        div_id_players = f'all_stats_{stat_type_tag}'
        data_table_players = parse_table_from_html(html_path=html_filepath,
                                                    div_id= div_id_players
                                                    )
    else:
        div_id_players = f'all_stats_{stat_type_tag}'
        data_table_players = parse_table_from_html(html_path=html_filepath,
                                                    div_id= div_id_players
                                                    )


    print(f"Data retrieved for {html_page}.\n")
