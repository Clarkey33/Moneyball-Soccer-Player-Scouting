
import requests
#from bs4 import BeautifulSoup as bs
import os
#import time



base_url = 'https://fbref.com/en/'
years_to_scrape = [2025,2024,2023,2022] #, "2024-2025","2023-2024","2022-2023","2021-2022"]

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


def construct_url(
        league_id:str ,
        league_name:str,
        stat_type:str=stat_tables,
        season:str =years_to_scrape,
        base_url:str=base_url) -> str:
    
    print("Constructing url for scraping..")
    #https://fbref.com/en/comps/9/2024-2025/keepers/2024-2025-Premier-League-Stats
    return f"{base_url}/comps/{league_id}/{season}/{stat_type}/{season}-{league_name}-Stats"

def fetch_page(url:str)->str:
    print("URL constructed successfully")
    print(f'Retrieving content from; {url}')

    response = requests.get(url, timeout=18)
    print(f"\nresponse:{response.status_code}, {response.reason}")

    #delay = random.uniform(12, 18)
    #print(f"Sleeping for {delay:.2f} seconds...")
    #time.sleep(delay)
    
    response.raise_for_status()
    print(f"Conent successfully retrieved")

    return response.text

def construct_filepath(output_dir,
                       season, 
                       league_name,
                       stat_type):
    
    print("Constructing filepath..")
    
    safe_league_name = league_name.replace(" ","_")
    
    return os.path.join(
        output_dir, 
        f"{season}_{safe_league_name}_{stat_type}.html")


def save_html(content, filepath):
    print(f"Filepath successfully constructed.")
    print(F"saving html content at: {filepath}")

    with open(filepath, 'w', encoding='utf-8') as html_file:
        html_file.write(content)


