import os
import csv
import re
import requests
from bs4 import BeautifulSoup
from string import ascii_uppercase


path = 'gundar-scraping.csv'       # change path if necessary
url_1 = 'https://baak.gunadarma.ac.id/cariMhsBaru/'
url_2 = '?teks=&tipeMhsBaru=&page='
table_index = 'table table-custom table-primary table-fixed bordered-table stacktable large-only'

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
            url = f"{url_1}{letter}{url_2}{page}"

            # fetching the table from the url
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            raw_html = soup.find('table', class_=table_index)

            try:
                table = raw_html.find_all('tr')[1:]
            except Exception:
                print(f"Finished inserting {users} users from the letter {letter}")
                break

            # cleaning each row from the table
            for row in table:
                clean_row = []
                row = str(row).split('\n')[2:-2]

                for item in row:
                    data = re.findall('.+>(.+)<', item)
                    clean_row.append(data[0])

                writer.writerow(clean_row)
                users += 1

print("Web scraping completed.")
