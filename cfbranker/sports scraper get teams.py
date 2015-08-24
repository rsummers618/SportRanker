import copper
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import re
#copper.project.path = '../../'

url = 'http://www.sports-reference.com/cfb/schools/'
r = requests.get(url)

soup = BeautifulSoup(r.text)
tables = soup.find_all('tr')


def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)


teams = []
prefix_1 = []
prefix_2 = []
teams_urls = []
data = ["link,teamName".split(",")]
for table in tables:
    lis = table.find_all('a', href=True)
    for li in lis:
        try:
            line = [li['href'],li.contents[0]]
        except:
            continue
        regexp = re.compile(r'schools')
        if regexp.search(li['href']) is not None:
        
            data.append(line)
            print li['href']
            print li.contents[0]
        #info = li.h5.a
        #teams.append(info.text)
        #url = info['href']
        #teams_urls.append(url)
        #prefix_1.append(url.split('/')[-2])
        #prefix_2.append(url.split('/')[-1])


        
csv_writer(data,"TeamlistPROG.csv")     
#dic = {'url': teams_urls, 'prefix_2': prefix_2, 'prefix_1': prefix_1}
#teams = pd.DataFrame(dic, index=teams)
#teams.index.name = 'team'
#print(teams)
#copper.save(teams, 'teams')
