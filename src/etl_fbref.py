from src.data_collection.scraping_utils import fetch_page,save_html
import requests
from bs4 import BeautifulSoup as bs
from pathlib import Path
import time
import os
import random


base_url = 'https://fbref.com/en/'
years_to_scrape = [2025,2024,2023,2022] 

league_config = {
    "Italian Serie A":{"id":"11", "name":"Serie-A", "season":"cross_year"},
    "English Premier league":{"id":"9", "name":"Premier-League", "season":"cross_year"},
    "Spanish La liga":{"id":"12", "name":"La-Liga", "season":"cross_year"},
    "France Ligue 1":{"id":"13", "name":"Ligue-1", "season":"cross_year"},
    "German Bundesliga":{"id":"20", "name":"Bundesliga", "season":"cross_year"},
    "Argentina Liga Profesional":{"id":"21", "name":"Liga-Profesional-Argentina", "season":"single_year"},
    "Austrian Bundesliga":{"id":"56", "name":"Austrian-Bundesliga", "season":"cross_year"},
    "Belgian Pro League":{"id":"37", "name":"Belgian-Pro-League", "season":"cross_year"},
    "Brazil Serie A":{"id":"24", "name":"Serie-A", "season":"single_year"},
    "Bulgarian First League":{"id":"67", "name":"Bulgarian-First-League", "season":"cross_year"},
    "Croatia Hrvatska NL":{"id":"63", "name":"Hrvatska-NL", "season":"cross_year"},
    "Czech First League":{"id":"66", "name":"Czech-First-League", "season":"cross_year"},
    "Danish Superliga":{"id":"50", "name":"Danish-Superliga", "season":"cross_year"},
    "Super League Greece":{"id":"27", "name":"Super-League-Greece", "season":"cross_year"},
    "Mexico Liga MX":{"id":"31", "name":"Liga-MX", "season":"cross_year"},
    "Netherlands Eredivisie":{"id":"23", "name":"Eredivisie", "season":"cross_year"},
    "Norway Eliteserien":{"id":"28", "name":"Eliteserien", "season":"cross_year"},
    "Poland Ekstraklasa":{"id":"36", "name":"Ekstraklasa", "season":"cross_year"},
    "Portugal Primeira Liga":{"id":"32", "name":"Primeira-Liga", "season":"cross_year"},
    "Russian Premier League":{"id":"30", "name":"Russian-Premier-League", "season":"cross_year"},
    "Scottish Premiership":{"id":"40", "name":"Scottish-Premiership", "season":"cross_year"},
    "Serbian SuperLiga":{"id":"54", "name":"Serbian-SuperLiga", "season":"cross_year"},
    "Swiss Super League":{"id":"57", "name":"Swiss-Super-League", "season":"cross_year"},
    "Allsvenskan":{"id":"29", "name":"Allsvenskan", "season":"cross_year"},
    "Super Lig":{"id":"26", "name":"Super-Lig", "season":"cross_year"},
    "USA Major League Soccer":{"id":"22", "name":"Major-League-Soccer", "season":"single_year"},
}

stat_tables =[
    'keepers','keepersadv','shooting','passing',
    'passing_types','gca','defense','possession',
    'playingtime','misc','stats'
]


def construct_url(league_id:str ,
                  league_name:str,
                  stat_type:str=stat_tables,
                  season:str =years_to_scrape,
                  base_url:str=base_url) -> str:
    
    print("Constructing url for scraping..")
    #https://fbref.com/en/comps/9/2024-2025/keepers/2024-2025-Premier-League-Stats
    return f"{base_url}/comps/{league_id}/{season}/{stat_type}/{season}-{league_name}-Stats"

def construct_filepath(output_dir,
                       season, 
                       league_name,
                       stat_type):
    
    print("Constructing filepath..")
    
    safe_league_name = league_name.replace(" ","_")
    
    return os.path.join(
        output_dir, 
        f"{season}_{safe_league_name}_{stat_type}.html")



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
