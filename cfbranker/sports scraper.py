import copper
import numpy as np
import pandas as pd
import requests
import urllib2
from bs4 import BeautifulSoup
from datetime import datetime, date
import csv
import os
import re
#copper.project.path = '../../'




def getCSVFiles(year):


    csv_path ='Teamlist.csv'
    f_obj=open(csv_path, "rb") 
    reader = csv.DictReader(f_obj, delimiter=',')

    
    BASE_URL = 'http://www.sports-reference.com{0}{1}/gamelog/'

    BASE_GAME_URL = 'http://espn.go.com/nba/boxscore?gameId={0}'
    for team in reader:
        print(team["link"])
        rows = []
    #for index, row in teams.iterrows():
    # for index, row in teams[:1].iterrows():
        #_team = row['name']
       #print(_team)
       
       
        try:
            TEAM_URL= BASE_URL.format(team["link"],year)
            print TEAM_URL
           # r = requests.get(BASE_URL.format(row['url]))
           

            html = urllib2.urlopen(TEAM_URL).read()
            bs= BeautifulSoup(html)

            

            
            ## Defense
            r = requests.get(TEAM_URL)
            table = bs.find(lambda tag: tag.name =='table' and tag.has_key('id') and tag['id'] =="defense")
            #headerstable = table.find_all('tr', class_="")
            headers = [header.text for header in table.find_all('th',colspan="",align=re.compile('t'))]
            

         
            for row in table.find_all('tr'):
                print row
                rows.append([val.text.encode('utf8') for val in row.find_all('td')])
                filepath = os.path.dirname(os.path.realpath(__file__)) + '/schools/' + team["teamName"] + '/' + year + '/'
                filename = filepath + team["teamName"] + ' ' + year + ' defense.csv'
                os.umask(0)
                if not os.path.exists(filepath):
                    os.makedirs(filepath, 777)
                with open(filename,'wb+') as f:
                    writer=csv.writer(f)
                    writer.writerow("Rk,Date,At,Opponent,Result,Pass_Cmp,Pass_Att,Pass_Pct,Pass_Yds,Pass_TD,Rush_Att,Rush_Yds,Rush_Avg,Rush_TD,Tot_Plays,Tot_Yds,Tot_Avg,FirstDn_Pass,FirstDn_Rush,FirstDn_Pen,FirstDn_Tot,Pen_No.,Pen_Yds,TO_Fum,TO_Int,TO_Tot".split(","))
                    writer.writerows(row for row in rows if row)
                    
        except:
            filepath =os.path.dirname(os.path.realpath(__file__)) + '/schools/' + team["teamName"] + '/' + year + '/'
            filename = filepath + team["teamName"] + ' ' + year + ' defense.csv'
            os.umask(0)
            if not os.path.exists(filepath):
                os.makedirs(filepath, 777)
            f = open(filename,'wb+')
            f.close()
            

        try:
            ##Offense 
            
            rows = []
            r = requests.get(TEAM_URL)
            table = bs.find(lambda tag: tag.name =='table' and tag.has_key('id') and tag['id'] =="offense")
            #headerstable = table.find_all('tr', class_="")
            headers = [header.text for header in table.find_all('th',colspan="",align=re.compile('t'))]
            

         
            for row2 in table.find_all('tr'):
                print row2
                rows.append([val.text.encode('utf8') for val in row2.find_all('td')])
                filepath = os.path.dirname(os.path.realpath(__file__)) + '/schools/' + team["teamName"] + '/' + year + '/'
                filename = filepath + team["teamName"] + ' ' + year + ' offense.csv'
               # os.umask(0)
                #if not os.path.exists(filepath):
                 #   os.makedirs(filepath, 777)
                with open(filename,'wb+') as f:
                    writer=csv.writer(f)
                    writer.writerow("Rk,Date,At,Opponent,Result,Pass_Cmp,Pass_Att,Pass_Pct,Pass_Yds,Pass_TD,Rush_Att,Rush_Yds,Rush_Avg,Rush_TD,Tot_Plays,Tot_Yds,Tot_Avg,FirstDn_Pass,FirstDn_Rush,FirstDn_Pen,FirstDn_Tot,Pen_No.,Pen_Yds,TO_Fum,TO_Int,TO_Tot".split(","))
                    writer.writerows(row2 for row2 in rows if row2)
        except:
            filepath = os.path.dirname(os.path.realpath(__file__)) + '/schools/' + team["teamName"] + '/' + year + '/'
            filename = filepath + team["teamName"] + ' ' + year + ' offense.csv'
            f=open(filename,'wb+')    
            f.close()
        
        
        
for x in range (1995,2016):

    year = str(x)
    getCSVFiles(year)    
        
        
        
        
        
        
        
      

#dic = {'id': game_id, 'date': dates, 'home_team': home_team, 'visit_team': visit_team, 
 #       'home_team_score': home_team_score, 'visit_team_score': visit_team_score}
        
#games = pd.DataFrame(dic).drop_duplicates(cols='id').set_index('id')
#print(games)
#copper.save(games, 'games.csv')