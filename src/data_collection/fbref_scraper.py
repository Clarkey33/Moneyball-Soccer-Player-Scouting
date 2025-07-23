from bs4 import BeautifulSoup, Comment
import requests
import re

URL = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'

page= requests.get(URL)
#print(page.text)

soup = BeautifulSoup(page.content, 'html.parser')


# re.sub(pattern,"",soup)
#soup = soup.replace('<!--',"")

div_tables=soup.find(
        name='div',
        attrs={
                #'class':'table_container is_setup',
                'id':'all_stats_standard'
                }
                )
table_stats=None
for element in div_tables.children:
    if isinstance(element, Comment):
        table_stats=element


print(type(table_stats))
print(table_stats)


#print(type(div_tables.table.string))

# table = str(div_tables)
# pattern =r"<[!]--|-[-]>"
# table = re.sub(pattern,"",table)


#print(table)





#print(div_tables.prettify())
#print(div_tables)
#<div class="table_container" id="div_stats_standard">