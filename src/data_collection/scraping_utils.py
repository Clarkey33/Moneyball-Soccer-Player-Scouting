import requests
from pathlib import Path
import time
import random



def fetch_page(url:str)->str:
    print("URL constructed successfully")
    print(f'Retrieving content from; {url}')

    response = requests.get(url, timeout=18)
    print(f"\nresponse:{response.status_code}, {response.reason}")
    
    response.raise_for_status()
    print(f"Conent successfully retrieved")

    return response.text

def save_html(content, filepath):
    print(f"Filepath successfully constructed.")
    print(F"saving html content at: {filepath}")

    with open(filepath, 'w', encoding='utf-8') as html_file:
        html_file.write(content)



#--------------- Transfer market----------------

#f"{https://www.transfermarkt.com}/{campeonato-brasileiro-serie-a}/startseite/wettbewerb/{BRA1}"
f"{https://www.transfermarkt.com}/{torneo-clausura}/marktwertaenderungen/wettbewerb/{ARGC}/page/1"
#BASE_URL/LEAGUE_NAME/marktwertaenderungen/wettbewerb/LEGAUE_ID/page/1

BASE_URL = "https://www.transfermarkt.com/"
league_config_marktvalue ={
    "Italian Serie A":{"id":"IT1", "name":"serie-a"},
    "English Premier league":{"id":"GB1", "name":"premier-league"},
    "Spanish La liga":{"id":"ES1", "name":"laliga"},
    "France Ligue 1":{"id":"FR1", "name":"ligue-1"},
    "German Bundesliga":{"id":"L1", "name":"bundesliga"},
    "Argentina Liga Profesional":{"id":"ARGC", "name":"torneo-final"},
    "Austrian Bundesliga":{"id":"A1", "name":"bundesliga"},
    "Belgian Pro League":{"id":"BE1", "name":"jupiler-pro-league"},
    "Brazil Serie A":{"id":"BRA1", "name":"campeonato-brasileiro-serie-a"},
    "Bulgarian First League":{"id":"BU1", "name":"efbet-liga"},
    "Croatia Hrvatska NL":{"id":"KR1", "name":"1-hnl"},
    "Czech First League":{"id":"TS1", "name":"fortuna-liga"},
    "Danish Superliga":{"id":"DK1", "name":"superligaen"},
    "Super League Greece":{"id":"GR1", "name":"Super-League-Greece"},
    "Mexico Liga MX":{"id":"MEXA", "name":"liga-mx-apertura"},
    "Netherlands Eredivisie":{"id":"NL1", "name":"eredivisie"},
    "Norway Eliteserien":{"id":"NO1", "name":"eliteserien"},
    "Poland Ekstraklasa":{"id":"PL1", "name":"pko-ekstraklasa"},
    "Portugal Primeira Liga":{"id":"PO1", "name":"liga-nos"},
    "Russian Premier League":{"id":"RU1", "name":"premier-liga"},
    "Scottish Premiership":{"id":"SC1", "name":"scottish-premiership"},
    "Serbian SuperLiga":{"id":"SER1", "name":"super-liga-srbije"},
    "Swiss Super League":{"id":"C1", "name":"super-league"},
    "Allsvenskan":{"id":"SE1", "name":"allsvenskan"},
    "Super Lig":{"id":"TR1", "name":"super-lig"},
    "USA Major League Soccer":{"id":"MLS1", "name":"major-league-soccer"},
}

