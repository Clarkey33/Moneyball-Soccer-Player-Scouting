from bs4 import BeautifulSoup #Comment
import requests
import re
import pandas as pd
from io import StringIO
import os
from pathlib import Path


script_file_path =Path(__file__).resolve()
script_file_dir = script_file_path.parent
project_root = script_file_dir.parent.parent

saved_html_pages_path=project_root/"data"/"raw"
saved_html_pages = os.listdir(saved_html_pages_path)
output_dir = "../../data/processed"



page = os.path.join(saved_html_pages_path,saved_html_pages[0])
pages= open(page)

def parse_table_from_html(
        html_page, 
        div_id:str) -> str:
    
    soup = BeautifulSoup(
        html_page.read(),
        features= 'html.parser'
        )
    
    div_container = None
    try: 
        if soup.find('div',div_id):
            div_container = soup.find('div',div_id)
        else:
            print("Contents not found for tag id :<div id{div_locator}")

    except Exception as e:
        print("f{e}")

    


    #parse data from comment tag
    comment = soup.find(string=re.compile('<table class='))

    #create new soup object of comment class
    new_soup= BeautifulSoup(comment, 'html.parser')
    #print(new_soup)

    #parse required data only
    table = new_soup.find(
        name='table',
        #attrs={'id':'stats_standard'}
        )

    table_str= StringIO(str(table))
#print(type(table_str))

df_stats = pd.read_html(table_str, index_col=1,header=1)[0]
print(df_stats.head())
print(f'\n{df_stats.info()}')
print(f'\ncolumn names:\n{df_stats.columns.tolist()}')



#parse html from table
"""
1. load saved html page from ../../data/raw [input]
2. create soup object with html page
3. search soup oject for <div id= ''; id string [input]
4. search for <table></table>; if found parse
    a. If not found; check and parse table from comment tag
    b. if no table found in either 4/5 return none and move on to next html doc
5. return parsed table as str 
"""









