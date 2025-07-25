from bs4 import BeautifulSoup #Comment
import requests
import re
import pandas as pd
from io import StringIO


URL = 'https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats#coverage'

page= requests.get(URL)

#create soup object
soup = BeautifulSoup(page.content, 'html.parser')

#parse table data from soup
table = soup.find(
    name='table',
    attrs={
        'id':'stats_standard'
        }
        )

table_str= StringIO(str(table))

#create and inspect dataframe
df_stats = pd.read_html(table_str, index_col=1,header=1)[0]
print(df_stats.head())
print(f'\n{df_stats.info()}')
print(f'\ncolumn names:\n{df_stats.columns.tolist()}')
print(f'\n Players per League:\n{df_stats['Comp'].value_counts()}')
print(f'\n Players per position:\n{df_stats['Pos'].value_counts()}')













