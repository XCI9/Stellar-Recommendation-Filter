from bs4 import BeautifulSoup
import requests
from time import sleep
import os

year = 110
url = f'https://www.cac.edu.tw/cacportal/star_his_report/{year}/{year}_result_standard/one2seven/collegeList_1.php'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")

results = soup.find_all('a')

links = []
for result in results:
    name = result.select_one('font').get_text()
    link = result['href']
    link = link.split('.',1)[-1]
    links.append((name,link))

if not os.path.exists(f"pdf/{year}"):
    os.makedirs(f"pdf/{year}")


for school, pdfPath in links:
    url = f'https://www.cac.edu.tw/cacportal/star_his_report/{year}/{year}_result_standard/one2seven' + pdfPath
    pdf = requests.get(url, stream=True, headers=headers)

    savePath = pdfPath.split('/')[-1]
    with open(f"pdf/{year}/{savePath}", 'wb') as f:
        f.write(pdf.content)
    print(f"successfully download {savePath}")
    sleep(1)

