from bs4 import BeautifulSoup, Comment
import requests
import re
import pandas as pd
from io import StringIO
import os
#from pathlib import Path

#output_dir = "../../data/processed"


def parse_table_from_html(
        html_content:str, 
        div_id:str)-> str:

    if not html_content:
        print("Error: HTML content is empty.")
        return None
    
    soup = BeautifulSoup(html_content, features= 'html.parser')

    div_data = soup.find('div', id=div_id)
    if not div_data:
        print(f"Div with id= '{div_id}' not found.")
        return None
        
    table = div_data.find('table')
    if table:
        print(f"Table found directly in div ='{div_id}'")
        return StringIO(str(table))  
    print(f"No direct table in '{div_id}. Checking for commented-out tables..")

    comments= div_data.find_all(string=lambda text:isinstance(text,Comment))
    for comment in comments:
        if '<table'in comment:
            comment_soup = BeautifulSoup(comment, 'html.parser')
            comment_table = comment_soup.find('table')
            if comment_table:
                print(f"Table found inside a comment in div='{div_id}'")
                return StringIO(str(comment_table))
            else:
                print(f"No table could be found in div='{div_id}', either directly or in comments")
                return None 


def clean_data_tables(table:pd.DataFrame) -> pd.DataFrame:
    #merge multi-index header
    table.columns = [
        f'{col[0].lower()}_{col[1].lower()}' if 'Unnamed:' not in col[0] else col[1].lower() for col in table.columns
        ]
    
    #drop duplicated index column
    table.drop(axis=1, columns=['rk'],inplace = True)
    
    
    print(table.head(2))
    print(table.columns)

