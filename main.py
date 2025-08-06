from src.data_collection.data_collection import construct_filepath, construct_url, fetch_page
from src.data_collection.data_collection import league_config, stat_tables, seasons_to_scrape
import requests
from bs4 import BeautifulSoup as bs
import time
import os


def scrape_all_data():

    output_dir = "data/raw"

    
