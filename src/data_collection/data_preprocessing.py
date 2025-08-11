from bs4 import BeautifulSoup #Comment
import requests
import re
import pandas as pd
from io import StringIO
import os
from pathlib import Path

#Portugal
#URL = 'https://fbref.com/en/comps/32/2024-2025/stats/2024-2025-Primeira-Liga-Stats'
#Brasil
#URL = 'https://fbref.com/en/comps/24/2024/stats/2024-Serie-A-Stats' 
#Belgium
#URL = 'https://fbref.com/en/comps/37/2024-2025/stats/2024-2025-Belgian-Pro-League-Stats'

#Netherlands
# URL = 'https://fbref.com/en/comps/23/2024-2025/stats/2024-2025-Eredivisie-Stats'

# page= requests.get(URL)
# print(type(page.content))

#saved_html_pages_path = "../../data/raw"
#saved_html_pages_path = "/home/on3b3ar/projects/moneyball-wolves-cunha-replacement/data/raw"

script_file_path =Path(__file__).resolve()
script_file_dir = script_file_path.parent
project_root = script_file_dir.parent.parent

saved_html_pages_path=project_root/"data"/"raw"
saved_html_pages = os.listdir(saved_html_pages_path)
output_dir = "../../data/processed"



page = os.path.join(saved_html_pages_path,saved_html_pages[0])
pages= open(page)

#create soup object
# with open(str(saved_html_pages[0])) as f:
#     soup = BeautifulSoup(f)
#print(soup)


soup = BeautifulSoup(pages.read(), features= 'html.parser')
#print(soup)

#parse data from comment tag
comment = soup.find(string=re.compile('<table class='))

#create new soup object of comment class
new_soup= BeautifulSoup(comment, 'html.parser')
print(new_soup)

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













