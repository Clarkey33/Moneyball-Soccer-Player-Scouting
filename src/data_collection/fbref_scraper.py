from bs4 import BeautifulSoup
import requests

URL = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'

page= requests.get(URL)
#print(page.text)

soup = BeautifulSoup(page.content, 'html.parser')
soup_tag_div = soup.div

# print(soup_tag_div.find_parents(
#     'table', attrs="table container is_setup"
#     )
#     )

# print(soup.find_parents(name='table',attrs='table container is_setup'))

# print(soup.select('div > table'))


#find all tags = "table"
# print(soup.find_all(
#     name='div', 
#     #attrs= "min_width sortable stats_table shade_zero now_sortable sticky_table eq2 re2 le2",
#     ))

#print(soup.find_all('table',id='stats_standard'))


#print(soup_tag_div['id':"wrap"])
print(soup)
#print(soup.table)
#print(type(soup.table))
