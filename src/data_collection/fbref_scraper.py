from bs4 import BeautifulSoup, Comment
import requests

URL = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'

page= requests.get(URL)
#print(page.text)

soup = BeautifulSoup(page.content, 'html.parser')



table=soup.find(
        name='div',
        attrs={
                #'class':'table_container',
                'id':'div_stats_standard'
                }
                )

for content in table(x=lambda x: isinstance(x,Comment)):
    content.extract()

#print(soup.prettify())
print(table)
#<div class="table_container" id="div_stats_standard">

