from bs4 import BeautifulSoup #Comment
import requests
import re
import pandas as pd
from io import StringIO
import os
from pathlib import Path



#output_dir = "../../data/processed"





def parse_table_from_html(
        html, 
        div_id:str):

    # with open(html_path,'r',encoding='utf-8') as f:
    #     html_content = f.read()
    
    soup = BeautifulSoup(
        html,
        features= 'html.parser'
        )
    print(soup)
    if not soup:
        print(f"Soup object not created properly")
        return None


    if not soup.find('div',div_id):
        print(f"div not found with id: {div_id}, table_found: {table_data}")
        
    if not soup.find('div',class_='placeholder'):
        return None
    
    else:
        print(f'div found')
    
    div_data= soup.find('div',div_id)
    print(div_data)
    try:
        print("Searching for table..")
        table_data = div_data.find('table')
        if table_data:
            table_data_str= StringIO(str(table_data))
            print(f"Table found!\n")
            return table_data_str
        elif not table_data:
            #check if hidden by comment tags
            print(f"Checking if table hidden by comment tags..")
            parse_comments = soup.find(string=re.compile('<table class='))
            parse_comments_soup = BeautifulSoup(parse_comments,'html.parser')
            table_data_comment = parse_comments_soup.find(name='table')
            if table_data_comment:
                table_data_comment_str= StringIO(str(table_data_comment))
                print(f"Table found !")
                return table_data_comment_str
            else:
                print(f"No table found!")
                return None    
        else:
            print(f"no table found in div!: {div_id}")
            return None
    except Exception as e:
        print(f" Failed to parse table from div: {e}\n")

    












