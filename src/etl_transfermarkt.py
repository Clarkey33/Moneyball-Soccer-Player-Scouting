from data_collection.scraping_utils import fetch_page,save_html
import requests
from bs4 import BeautifulSoup as bs
from pathlib import Path
import time
import os
import random


project_root = Path(__file__).resolve().parent.parent
output_dir = project_root/"data"/"raw"/"transfermarkt" 

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

def get_last_page(html_content:str)->int:
    if not html_content:
        return 1
    
    soup = bs(html_content,'html.parser')
    last_page_location = soup.find("li",class_="tm-pagination__list-item tm-pagination__list-item--icon-last-page")

    if not last_page_location:
        return 1
    
    last_page_link=last_page_location.find("a")
    
    if not last_page_link or 'href' not in last_page_link.attrs:
        return 1
    
    last_page_url = last_page_link['href']

    try:
        last_page_number = int(last_page_url.split('/')[-1])
        return last_page_number
    except (ValueError,IndexError):
        return 1


def construct_transfermarkt_url(league_name: str,
                                league_id: str,
                                page: int) -> str:
    print("Constructing url for scraping..")
    return f"{BASE_URL}{league_name}/marktwertaenderungen/wettbewerb/{league_id}/page/{page}"


def construct_filepath(output_dir:str, 
                       league_name:str,
                       page_num:int):
    
    print("Constructing filepath..")
    
    safe_league_name = league_name.replace(" ","_")
    
    return os.path.join(
        output_dir, 
        f"{safe_league_name}_page_{page_num}.html")
        #f"{season}_{safe_league_name}_{stat_type}.html")


def scrape_all_data():
    
    output_dir.mkdir(parents=True, exist_ok=True)
    for league, config in league_config_marktvalue.items():
        print(f"\n->Processing Legaue: {league}..")
        last_page=1

        filepath_page1 = construct_filepath(output_dir=output_dir,
                                             league_name=league,
                                             page_num=1
                                             )

        if os.path.isfile(filepath_page1):
            print(f"Page 1 already exists. Reading from file to get page count")
            with open(filepath_page1, 'r',encoding='utf-8') as f:
                html_content_page1 = f.read()
            last_page = get_last_page(html_content=html_content_page1)
        else:
            print("Page 1 not found. fetching from web..")     
            first_page_url= construct_transfermarkt_url(league_name=config.get('name'),
                                                league_id=config.get("id"),
                                                page=1
                                                )
            
            print(f"Attempting to fetch html at :{first_page_url}")
            html_content_page1 = fetch_page(url=first_page_url)

            if html_content_page1:
                save_html(content=html_content_page1,
                          filepath=filepath_page1
                          )
                last_page = get_last_page(html_content=html_content_page1)
            else:
                print(f"Could not fetch page 1 for {league}. Skipping this league..")
                continue

            print(f"Found {last_page} total pages for {league}.")
           

        for page_num in range(1, last_page+1):
            filepath = construct_filepath(output_dir=output_dir,
                                           league_name=league,
                                           page_num=page_num)

            if os.path.isfile(filepath):
                print(f"Fetching page {page_num}..")
            
                url = construct_transfermarkt_url(league_name=config.get('name'),
                                                league_id=config.get("id"),
                                                page=page_num
                                                )
                
                html_content = fetch_page(url=url)


                if html_content:
                    save_html(html_content,filepath)
                else:
                    print(f"Failed to fetch page {page_num}. It will be skipped")


                #print(f"Saved: {filepath}")
        print(f"Scrape complete for: {league}")

            

if __name__ == "__main__":
    scrape_all_data()