from data_collection.data_preprocessing import parse_table_from_html

import os 
from pathlib import Path

script_file_path =Path(__file__).resolve()
script_file_dir = script_file_path.parent
project_root = script_file_dir.parent 

html_pages_dir=project_root/"data"/"raw"
html_pages_filename_list = os.listdir(html_pages_dir) # ->list

for html_page in html_pages_filename_list[:2]:
    print(f"start: {html_page}")
    html_filepath = os.path.join(html_pages_dir,html_page)
    html_name = html_filepath.replace('.html','')
    html_tags= html_name.split('_')
    stat_type_tag = html_tags[-1]

    print(html_filepath)

    
    with open(html_filepath,'r',encoding='utf-8') as f:
        html_content = f.read()

    if stat_type_tag == 'stats':
        stat_type_tag='standard'
        div_id_team = f"switcher_stats_squads_{stat_type_tag}"
        div_id_players = f"all_stats_{stat_type_tag}"
        print(div_id_team)
        print(div_id_players)
        #print(html_content)

        data_table_team = parse_table_from_html(html=html_content,
                                            div_id=div_id_team
                                            )
        print(f'{data_table_team}\n')
        data_table_players = parse_table_from_html(html=html_content,
                                                    div_id= div_id_players
                                                    )
        print(f'{data_table_players}\n')

    elif stat_type_tag == 'keepersadv':
        stat_type_tag = 'keepers_adv'
        div_id_players = f'all_stats_{stat_type_tag}'
        print(div_id_players)
        data_table_players = parse_table_from_html(html=html_content,
                                                    div_id= div_id_players
                                                    )
        
    elif stat_type_tag == 'playingtime':
        stat_type_tag = 'playing_time'
        div_id_players = f'all_stats_{stat_type_tag}'
        print(div_id_players)
        data_table_players = parse_table_from_html(html=html_content,
                                                    div_id= div_id_players
                                                    )
    else:
        div_id_players = f'all_stats_{stat_type_tag}'
        print(div_id_players)
        data_table_players = parse_table_from_html(html=html_content,
                                                    div_id= div_id_players
                                                    )


    #print(f"Data retrieved for {html_page}.\n")
