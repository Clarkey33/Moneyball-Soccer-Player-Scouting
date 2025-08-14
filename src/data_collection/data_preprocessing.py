from bs4 import BeautifulSoup #Comment
import requests
import re
import pandas as pd
from io import StringIO
import os
from pathlib import Path



#output_dir = "../../data/processed"





def parse_table_from_html(
        html_path:str, 
        div_id:str) -> str:
    
    """
1. load saved html page from ../../data/raw [input]
2. create soup object with html page
3. search soup oject for <div id= ''; id string [input]
4. search for <table></table>; if found parse
    a. If not found; check and parse table from comment tag
    b. if no table found in either 4/5 return none and move on to next html doc
5. return parsed table as str 
"""

    with open(html_path,'r',encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(
        html_content,
        features= 'html.parser'
        )
    
    div_data = None
    parse_comments=None
    table_data = None
    table_data_comment= None

    if not soup.find('div',div_id):
        print(f"div not found!")
        return f"There was no div with id({div_id} found: {table_data}"
    
    else:
        print(f'div found')
        div_data= soup.find('div',div_id)
        print("Searching for table..")
        try: 
            table_data = div_data.find('table')
            table_data_comment = soup.find(string=re.compile('<table class='))

            if table_data and table_data_comment:
                print(f"\nparsing table from {table_data}\n")
                table_data_str= StringIO(str(table_data))

                print(f"\nparsing table from {table_data_comment}\n")
                parse_comments = soup.find(string=re.compile('<table class='))
                new_soup = BeautifulSoup(parse_comments, 'html.parser')
                table_data_comment_= new_soup.find(name='table')
                table_data_comment_str= StringIO(str(table_data_comment_))

                return table_data_str, table_data_comment_str
            
            elif table_data:
                print("Contents found for tag id : <div id={div_locator}")
                table_data_str= StringIO(str(table_data))
                print("Desired table found!")
                return table_data_str
            
            elif table_data_comment:
                print("Contents not found for tag id : <div id={div_locator}")
                print("checking if hidden by comment tag '<!--' ..")
                parse_comments = soup.find(string=re.compile('<table class='))
                new_soup = BeautifulSoup(parse_comments, 'html.parser')
                table_data_comment_= new_soup.find(name='table')
                table_data_comment_str= StringIO(str(table_data_comment_))
                print("Desired table found!")
                return table_data_comment_str
        except Exception as e:
            print(f" Failed to parse table from div: {e}")

    












