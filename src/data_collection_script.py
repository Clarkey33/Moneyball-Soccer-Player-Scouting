from src.data_collection.data_collection import construct_filepath, construct_url, fetch_page,save_html
from src.data_collection.data_collection import league_config, stat_tables, years_to_scrape
import requests
#from bs4 import BeautifulSoup as bs
#from pathlib import Path
import time
import os
import random


def scrape_all_data():

    output_dir = "data/raw"

    for year in years_to_scrape:
        for league_name, league_values in league_config.items():
            season_string = ''
            if league_values['season'] == 'cross_year':
                #"2024-2025"
                season_string = f"{year-1}-{year}"
            elif league_values['season'] == 'single_year':
                season_string = str(year)

            else:
                print(f"-> Error: Unknown season format for{league_name}")
                continue

            for stat_type in stat_tables:
                file_path =construct_filepath(
                    season=season_string,
                    league_name=league_name,
                    stat_type=stat_type,
                    output_dir=output_dir
                )

                if not os.path.isfile(file_path):

                    url = construct_url(
                        season=season_string,
                        stat_type=stat_type,
                        league_id=league_values['id'],
                        league_name=league_values['name']
                    )
                    print(f"Fecthing: {os.path.basename(file_path)}..")
                    try:
                        html_page= fetch_page(url=url)
                    except requests.exceptions.RequestException as e:
                        print(f"-> Error: Could not fetch{url}.\nReason:{e}")
                        continue

                    save_html(filepath=file_path,
                            content=html_page)
                    print("Successfully saved")

                    delay = random.uniform(9, 12)
                    print(f"-> Waiting for {delay:.2f} seconds...")
                    time.sleep(delay)
                                        
                    print(f"{season_string},{league_name},{stat_type} html content saved.")
                else:
                    print(f"Skipping, file already exists: {os.path.basename(file_path)}")
                    continue
        print(f"\n---- Completed scraping  all leaguesfor {year} ---\n")
                


    
if __name__=="__main__":
    scrape_all_data()
