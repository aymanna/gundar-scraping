import os
from os.path import isfile
from csv import writer
from re import findall
from requests import get
from bs4 import BeautifulSoup
from string import ascii_uppercase


def scraper(arg, filescript):
    file = filescript.split('.py')[0] + '.csv'
    url = 'https://baak.gunadarma.ac.id/'

    if isfile(file):
        mode = 'a'
    else:
        mode = 'x'

    with open(file, mode, newline='') as f:
        w = writer(f)

        for letter in ascii_uppercase:
            page = 0
            users = 0

            while True:
                page += 1
                target_url = f'{url}{arg}/{letter}?page={page}'

                res = get(target_url)
                html = BeautifulSoup(res.text, 'html.parser')
                table = html.find('table')

                if table is None:
                    print(f'Finished inserting {users} users from the letter {letter}')
                    break

                rows = table.find_all('tr')

                for row in rows[1:]:
                    items = findall('<td.*>(.+)</td>', str(row))
                    w.writerow(items[1:])
                    users += 1

    print('Web scraping completed.')
