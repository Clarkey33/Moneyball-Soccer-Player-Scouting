from bs4 import BeautifulSoup #Comment
import requests
import re
import pandas as pd
from io import StringIO

URL = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'

page= requests.get(URL)

#create soup object
soup = BeautifulSoup(page.content, 'html.parser')

#parse data from comment tag
comment = soup.find(string=re.compile('<table class='))

#create new soup object of comment class
new_soup= BeautifulSoup(comment, 'html.parser')

#parse required data only
table = new_soup.find(
    name='table',
    attrs={'id':'stats_standard'}
    )

table_str= StringIO(str(table))
#print(type(table_str))

df_stats = pd.read_html(table_str, index_col=1,header=1)[0]
print(df_stats.head())
print(f'\ncolumn names:\n{df_stats.columns.tolist()}')













