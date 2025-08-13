from bs4 import BeautifulSoup #Comment
import requests
import re
import pandas as pd
from io import StringIO
import os
from pathlib import Path



output_dir = "../../data/processed"





def parse_table_from_html(
        html_path:str, 
        div_id:str) -> str:
    
    with open(html_path,'r',encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(
        html_content,
        features= 'html.parser'
        )
    
    div_with_table_data = None
    parse_comments=None
    table_with_data = None

    if not soup.find('div',div_id):
        print(f"div not found!")
        return table_with_data
    
    else:
        print(f'div found')
        div_with_table_data= soup.find('div',div_id)
        print("Searching for table..")
        try: 
            if div_with_table_data.find('table'):
                table_with_data = div_with_table_data.find('table')
                table_str= StringIO(str(table_with_data))
                print("Desired table found!")
                return table_str
            else:
                print("Contents not found for tag id : <div id={div_locator}")
                print("checking if hidden by comment tag '<!--' ..")
                if soup.find(string=re.compile('<table class=')):
                    parse_comments = soup.find(string=re.compile('<table class='))
                    new_soup = BeautifulSoup(parse_comments, 'html.parser')
                    table_with_data= new_soup.find(name='table')
                    table_str= StringIO(str(table_with_data))
                    print("Desired table found!")

                return table_str
        except Exception as e:
            print(f" Failed to parse table from div: {e}")

    


#     #parse data from comment tag
#     comment = soup.find(string=re.compile('<table class='))

#     #create new soup object of comment class
#     new_soup= BeautifulSoup(comment, 'html.parser')
#     #print(new_soup)

#     #parse required data only
#     table = new_soup.find(
#         name='table',
#         #attrs={'id':'stats_standard'}
#         )

#     table_str= StringIO(str(table))
# #print(type(table_str))

# df_stats = pd.read_html(table_str, index_col=1,header=1)[0]
# print(df_stats.head())
# print(f'\n{df_stats.info()}')
# print(f'\ncolumn names:\n{df_stats.columns.tolist()}')



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









