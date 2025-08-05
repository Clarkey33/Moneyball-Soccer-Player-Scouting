""" 

"""


# import requests
# from bs4 import BeautifulSoup as bs


# url = 'https://fbref.com/en/'
# reqs = requests.get(url)
# soup = bs(reqs.text, 'html.parser')

# leagues=[
#     '11/Serie-A-', '9/Premier-League-','12/La-Liga-',
#     '13/Ligue-1-', '20/Bundesliga-', '21/Liga-Profesional-Argentina-',
#     '56/Austrian-Bundesliga-','37/Belgian-Pro-League-', '24/Serie-A-',
#     '67/Bulgarian-First-League-','63/Hrvatska-NL-', '66/Czech-First-League-',
#     '50/Danish-Superliga-','27/Super-League-Greece-','31/Liga-MX-','23/Eredivisie-',
#     '28/Eliteserien-', '36/Ekstraklasa-', '32/Primeira-Liga-', '30/Russian-Premier-League-',
#     '40/Scottish-Premiership-','54/Serbian-SuperLiga-', '57/Swiss-Super-League-',
#     '29/Allsvenskan-','26/Super-Lig-','22/Major-League-Soccer-',  
#     ]

# urls=[]
# for link in soup.find_all('a', href=True):
#     urls.append(link.get('href'))



#print(urls)

#-----------------------------------Start----------------------------------------------------

#----Testing out urllib.parse----

from urllib.parse import urlparse, urlsplit

print(f"{urlparse('https://fbref.com/en/comps/9/2024-2025/2024-2025-Premier-League-Stats')}")
print(f"{urlsplit('https://fbref.com/en/comps/9/2024-2025/2024-2025-Premier-League-Stats')}")
print(f"\n{urlparse('https://fbref.com/en/')}")
print(f"\n{urlparse('https://fbref.com/en/comps/12/La-Liga-Stats')}")








#------------------------------------End---------------------------------------------------------





# for comp in leagues:
#     for link in urls:
#         if not comp in link:
#             continue
#         else:

  



