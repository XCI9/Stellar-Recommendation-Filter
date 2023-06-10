from bs4 import BeautifulSoup
import requests
from time import sleep
import os
import csv


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}

school = {}


for year in range(103, 111):
    url = f'https://www.cac.edu.tw/cacportal/star_his_report/{year}/{year}_result_standard/one2seven/collegeList_1.php'
    print(f'open {url}')

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    results = soup.find_all('a')
    links = []
    for result in results:
        text = result.select_one('font').get_text()
        name = text.split(')')[1]
        id = text.split(')')[0].split('(')[1]
        if school.get(id):
            if school[id] != name:
                print(f"{year-1} {school[id]} != {year} {name}")
        school[id] = name
    sleep(1)


with open(f'school.csv','w',encoding='utf8', newline='') as csvFile:
    output = csv.writer(csvFile)

    for id, name in school.items():
        output.writerow([id, name])

