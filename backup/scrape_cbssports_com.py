import re
import csv
import html5lib
from bs4 import BeautifulSoup
from urllib import request
import requests
from selenium import webdriver

#needs selenium

SITE = 'cbssports.com'
URL = 'http://www.cbssports.com/nba/powerrankings/'

abr_list = ['atl',
	'bkn',
	'bos',
	'cha',
	'chi',
	'cle',
	'dal',
	'den',
	'det',
	'gsw',
	'hou',
	'ind',
	'lac',
	'lal',
	'mem',
	'mia',
	'mil',
	'min',
	'noh',
	'nyk',
	'okc',
	'orl',
	'phi',
	'phx',
	'por',
	'sac',
	'sas',
	'tor',
	'uta',
	'was']

class ScrapeCbsSports:

	def __init__(self):
		#Initialize Beautiful Soup
		#Pull NBA.com power rankings and parse
		#print(self.nba_pr)
		browser = webdriver.Firefox()
		browser.get(URL)
		self.nba_pr  = browser.page_source
		self.soup = BeautifulSoup(self.nba_pr)
		browser.close()
	
	def getSite(self):
		return(SITE)

	def getUrl(self):
		return(URL)

	def monthToNum(self,date): #IMPROVEMENT: make this enum type

		return{
				'Jan' : 1,
				'Feb' : 2,
				'Mar' : 3,
				'Apr' : 4,
				'May' : 5,
				'Jun' : 6,
				'Jul' : 7,
			 	'Aug' : 8,
				'Sep' : 9, 
				'Oct' : 10,
				'Nov' : 11,
				'Dec' : 12
		}[date]

	def nameToShortName(self,name):

		return{

			'OKC' : 'okc',
			'IND' : 'ind',
			'HOU': 'hou',
			'MIA' : 'mia' ,
			'LAC' : 'lac',
			'SA'  : 'sas',
			'DAL' : 'dal',
			'PHO' : 'phx',
			'MEM' : 'mem',
			'POR' : 'por',
			'TOR' : 'tor',
			'GS' : 'gsw',
			'CHI' : 'chi',
			'WAS' : 'was',
			'BKN' : 'bkn',
			'ATL' : 'atl',
			'MIN' : 'min',
			'CHA' : 'cha',
			'NO' : 'noh',
			'DET' : 'det',
			'NY' : 'nyk',
			'DEN' : 'den',
			'UTA' : 'uta',
			'ORL' : 'orl',
			'CLE' : 'cle',
			'BOS' : 'bos',
			'SAC' : 'sac',
			'LAL' : 'lal',
			'MIL' : 'mil',
			'PHI' : 'phi'
		}[name]

	def getDatePublished(self):

		date_raw = self.soup.find('time')['datetime']
		
		#Pull NBA.com power rankings and parse		
		p = re.search('\d+-\d+-\d+',date_raw)
		date =  p.group(0)
		
		return(date)

		#Put all data in string
	
	def getRanks(self):
				
		ratings_raw = self.soup.find_all('td','teamRankLogo')

		#Create rankings list
		i = 1		
		teamList = []
		
		for rank in ratings_raw:
			teamList.append((self.nameToShortName(re.search('([A-Z]+)',rank.a['href']).group(0)),i))
			i+=1
			
		teamList.sort()
		teamRanks = [ranks for names,ranks in teamList]

		return(teamRanks)	
		
