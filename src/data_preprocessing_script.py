from data_collection.data_preprocessing import parse_table_from_html
from data_collection.data_collection import years_to_scrape, league_config, stat_tables, construct_filepath
import os 
from pathlib import Path

script_file_path =Path(__file__).resolve()
script_file_dir = script_file_path.parent
project_root = script_file_dir.parent 

html_pages_dir=project_root/"data"/"raw"
html_pages_filename_list = os.listdir(html_pages_dir) # ->list

html_pages_filepath = os.path.join(html_pages_dir,html_pages_filename_list)
#pages= open(page)

stats_name_list = [
    'standard', 'shooting', 'keeper',
    'passing','keeper_adv','passing_types',
    'gca','defense','possession',
    'playing_time','misc'
              ]



# f"{season}_{safe_league_name}_{stat_type}.html"
# -> safe league name is made with the key value 
#idea: create a foor loop years scrape , league name, stat type similar to data collection
# check file path for save html is it is stat type standard.. scrape both team and player stats
#if stat type not standard only scrape player stats
stat_val=None
for year in years_to_scrape:
    for league_name, league_values in league_config.items():
        season_string = ''
        if league_values.get("season") == "single_year":
            season_string = year
        elif league_values.get("seaspm") == "cross_year":
            season_string = f"{year-1}-{year}"
        else:
            print("no season available")
            continue 
        for stat in stats_name_list:
            if stat.find('_'):
                stat_val=stat.replace('_',"")
            else:
                continue

            html_file_path = construct_filepath(
                output_dir=html_pages_dir,
                season=season_string,
                league_name=league_name,
                stat_type=stat_val
            )

            if not os.path.isfile(html_file_path):
                continue

            else:
                if stat == "standard":
                    table_players_stats = parse_table_from_html(
                        html_page=html_pages_filepath,
                        div_id=stat
                        )

#refractor code to simplify logic
#return to original approach; do not reconstruct the file path
#use the list of files already captured in code
#split path to extract stat type , seasons etc
#div id is stat type; two types have '_' separator
#only need squad and player tables for standard
#div id tempplate:  id= all_stats_squads_<stat_type> | id= all_stats_<stat_type>


















for stat_name in stats_name_list:
    div_id = f"all_stats_{stat_name}"
    print(div_id)

    table_players_stats = parse_table_from_html(html_page=html_pages_filepath,
                                                div_id=div_id
                                                )
    
    print(f"Table data type:  {type(table_players_stats)}")
