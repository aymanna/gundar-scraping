import os
import csv
from re import findall
from requests import get
from bs4 import BeautifulSoup
from string import ascii_uppercase


path = 'gundar-scraping.csv'
base_url = 'https://baak.gunadarma.ac.id/'

if os.path.isfile(path):
    mode = 'a'
else:
    mode = 'x'

with open(path, mode, newline='') as f:
    writer = csv.writer(f)

    for letter in ascii_uppercase:
        page = 0
        users = 0

        while True:
            page += 1
            url = f'{base_url}cariMhsBaru/{letter}?page={page}'

            res = get(url)
            raw_html = BeautifulSoup(res.text, 'html.parser')
            raw_table = raw_html.find('table')

            if raw_table is None:
                print(f'Finished inserting {users} users from the letter {letter}')
                break

            rows = raw_table.find_all('tr')

            for row in rows[1:]:
                items = findall('<td.*>(.+)</td>', str(row))
                writer.writerow(items[1:])
                users += 1

print('Web scraping completed.')
