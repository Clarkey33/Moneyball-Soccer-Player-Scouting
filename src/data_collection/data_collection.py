
import requests
from bs4 import BeautifulSoup as bs
import os


base_url = 'https://fbref.com/en/'
seasons_to_scrape = ["2024-2025","2023-2024","2022-2023","2021-2022"]

league_config = {
    "Italian Serie A":{"id":"11", "name":"Serie-A"},
    "English Premier league":{"id":"9", "name":"Premier-League"},
    "Spanish La liga":{"id":"12", "name":"La-Liga"},
    "France Ligue 1":{"id":"13", "name":"Ligue-1"},
    "German Bundesliga":{"id":"20", "name":"Bundesliga"},
    "Argentina Liga Profesional":{"id":"21", "name":"Liga-Profesional-Argentina"},
    "Austrian Bundesliga":{"id":"56", "name":"Austrian-Bundesliga"},
    "Belgian Pro League":{"id":"37", "name":"Belgian-Pro-League"},
    "Brazil Serie A":{"id":"24", "name":"Serie-A"},
    "Bulgarian First League":{"id":"67", "name":"Bulgarian-First-League"},
    "Hrvatska NL":{"id":"63", "name":"Hrvatska-NL"},
    "Czech First League":{"id":"66", "name":"Czech-First-League"},
    "Danish Superliga":{"id":"50", "name":"Danish-Superliga"},
    "Super League Greece":{"id":"27", "name":"Super-League-Greece"},
    "Mexico Liga MX":{"id":"31", "name":"Liga-MX"},
    "Netherlands Eredivisie":{"id":"23", "name":"Eredivisie"},
    "Eliteserien":{"id":"28", "name":"Eliteserien"},
    "Ekstraklasa":{"id":"36", "name":"Ekstraklasa"},
    "Primeira Liga":{"id":"32", "name":"Primeira-Liga"},
    "Russian Premier League":{"id":"30", "name":"Russian-Premier-League"},
    "Scottish Premiership":{"id":"40", "name":"Scottish-Premiership"},
    "Serbian SuperLiga":{"id":"54", "name":"Serbian-SuperLiga"},
    "Swiss Super League":{"id":"57", "name":"Swiss-Super-League"},
    "Allsvenskan":{"id":"29", "name":"Allsvenskan"},
    "Super Lig":{"id":"26", "name":"Super-Lig"},
    "USA Major League Soccer":{"id":"22", "name":"Major-League-Soccer"},
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
        season:str =seasons_to_scrape,
        base_url:str=base_url) -> str:
    
    #https://fbref.com/en/comps/9/2024-2025/keepers/2024-2025-Premier-League-Stats
    return f"{base_url}/comps/{league_id}/{season}/{stat_type}/{season}-{league_name}-Stats"

def fetch_page(url:str)->str:

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.text

def construct_filepath(output_dir,
                       season, 
                       league_name,
                       stat_type):
    
    safe_league_name = league_name.replace(" "."_")
    
    return os.path.join(
        output_dir, 
        f"{season}_{safe_league_name}_{stat_type}.html")


def save_html(content, filepath):

    with open(filepath, 'w', encoding='utf-8') as html_file:
        html_file.write(content)


