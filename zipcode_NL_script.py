#by github.com/msklc

import requests
import bs4
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import string
import datetime

#Create number list (4-digit) and alphabet list (2-character) for zipcode list
num_list=np.arange(1000,10000)

alph_list=[]
alph=list(string.ascii_uppercase)
for n in alph:
    for m in alph:
        temp=n+m
        alph_list.append(temp)


#Create variables
zipcode_list=[]
place_list=[]
gemeente_list=[]
province_list=[]
lat_list=[]
lon_list=[]

#Scrape the zipcode list
print('Scraping started at {}'.format(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
for num in num_list:    
    url='http://www.geonames.org/postalcode-search.html?q={}&country=NL'.format(num)
    try:
        r=requests.get(url)
        soup=BeautifulSoup(r.text,'html.parser')
        data=soup.find('p').text.strip()
        if 'No rows found' in data:
            None
        else:
            for alph in alph_list:
                try:
                    url='http://www.geonames.org/postalcode-search.html?q={}+{}&country=NL'.format(num,alph)
                    r=requests.get(url)
                    soup=BeautifulSoup(r.text,'html.parser')
                    place=soup.find('table',{'class':'restable'}).find_all('td')[1].text.strip()
                    place_list.append(place)
                    zipcode=soup.find('table',{'class':'restable'}).find_all('td')[2].text.strip().replace(' ','')
                    zipcode_list.append(zipcode)
                    province=soup.find('table',{'class':'restable'}).find_all('td')[4].text.strip()
                    province_list.append(province)
                    gemeente=soup.find('table',{'class':'restable'}).find_all('td')[5].text.strip()
                    gemeente_list.append(gemeente)
                    coordinate=soup.find('table',{'class':'restable'}).find_all('tr')[2].text.strip().split('/')
                    lat_list.append(coordinate[0])
                    lon_list.append(coordinate[1])           
                except:
                    None
            print('{} is scraped at {}'.format(num,datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
    except:
        None

print('Scraping finished at {}'.format(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))

#Save The result to pandas-dataframe and save
NL_zipcode=pd.DataFrame({'Zipcode':zipcode_list, 'Place':place_list, 'Gemeente':gemeente_list, 'Province':province_list, 'Latitude':lat_list, 'Longitude':lon_list})
NL_zipcode.to_csv('NL_zipcode.csv')
print('Totally {} row data is scraped and saved'.format(NL_zipcode.shape[0]))