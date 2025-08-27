from src.data_collection.scraping_utils import fetch_page,save_html
import requests
from bs4 import BeautifulSoup as bs
from pathlib import Path
import time
import os
import random



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



def construct_transfermarkt_url(league_name: str,
                                league_id: str,
                                page: int) -> str:
    print("Constructing url for scraping..")
    return f"{BASE_URL}{league_name}/marktwertaenderungen/wettbewerb/{league_id}/page/{page}"