from bs4 import BeautifulSoup
import requests

URL = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'

page= requests.get(URL)
#print(page.text)

soup = BeautifulSoup(page.content, 'html.parser')

print(soup.body)
#print(soup.title)
#tables = soup.find(id='div_stats_standard')
#rint(tables)