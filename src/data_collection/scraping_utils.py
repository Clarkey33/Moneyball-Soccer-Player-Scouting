import requests
from pathlib import Path
import time
import random

USER_AGENTS=[
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]

def fetch_page(url:str)->str:
    #print("URL constructed successfully")
    print(f'Retrieving content from; {url}')

    headers ={'User-Agent': random.choice(USER_AGENTS)}
    try:
        response = requests.get(url, timeout=18, headers=headers)
        print(f"\nresponse:{response.status_code}, {response.reason}")
    
        response.raise_for_status()
        print(f"Conent successfully retrieved")
        return response.text
    except Exception as e:
        print(f"Failed to fetch html content: {e}")
        return None

def save_html(content, filepath):
    print(f"Filepath successfully constructed.")
    print(F"saving html content at: {filepath}")

    with open(filepath, 'w', encoding='utf-8') as html_file:
        html_file.write(content)


