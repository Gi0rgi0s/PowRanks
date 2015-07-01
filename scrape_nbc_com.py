import re
import csv
from bs4 import BeautifulSoup
from urllib import request

SITE = 'nbcsports.com'
URL = 'http://probasketballtalk.nbcsports.com/2014/03/10/pbt-power-rankings-tell-me-again-how-the-spurs-are-too-old/'

#SLOW website
#URL hardcoded

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


class ScrapeNbc:

	def __init__(self,URL=URL):
		#Initialize Beautiful Soup
		nba_pr  = request.urlopen(URL).read()
		self.soup = BeautifulSoup(nba_pr)
		print('----------------NBC.com Initialized------------------')

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

			'Thunder' : 'OKC',
			'Pacers' : 'IND',
			'Rockets': 'HOU',
			'Heat' : 'MIA' ,
			'Clippers' : 'LAC',
			'Spurs'  : 'SAS',
			'Mavericks' : 'DAL',
			'Suns' : 'PHX',
			'Grizzlies' : 'MEM',
			'Trail Blazers' : 'POR',
			'Raptors' : 'TOR',
			'Warriors' : 'GSW',
			'Bulls' : 'CHI',
			'Wizards' : 'WAS',
			'Nets' : 'BKN',
			'Hawks' : 'ATL',
			'Timberwolves' : 'MIN',
			'Bobcats' : 'CHA',
			'Pelicans' : 'NOH',
			'Pistons' : 'DET',
			'Knicks' : 'NYK',
			'Nuggets' : 'DEN',
			'Jazz' : 'UTA',
			'Magic' : 'ORL',
			'Cavaliers' : 'CLE',
			'Celtics' : 'BOS',
			'Kings' : 'SAC',
			'Lakers' : 'LAL',
			'Bucks' : 'MIL',
			'76ers' : 'PHI'
		}[name]

	def getDatePublished(self):
		#Initialize Beautiful Soup
		
		#Pull NBA.com power rankings and parse
		
		self.date_raw = self.soup.find('p', 'image_item_date')
		
		#Pull date and parse
		#print(date_raw.text)
		p = re.search('(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s(\d+)(?:,)\s(20\d+)',self.date_raw.text)
		#print(self.date_raw.text)
		#print(p.group(0) + "--")
		date_parsed = [ self.monthToNum(p.group(1)), (p.group(2)), (p.group(3)) ]
		date = date_parsed[2] + '-' + str(date_parsed[0]).zfill(2) + '-' + str(date_parsed[1]).zfill(2)

		return(date)

		#Put all data in string
	
	def getRanks(self):
		print('hello ranks')
		teamList = []

		
		#Pull NBA.com power rankings and parse
		
		ratings_raw = self.soup.find_all('strong')

		#Create rankings list
		i = 1

		for rank in ratings_raw:
			p = re.search('(?:\.\s)([\da-zA-Z\s]+)(?:\()',rank.text)
			teamList.append((self.nameToShortName(p.group(1).strip()),i))
			i+=1
		
		teamList.sort()
		teamRanks = [ranks for names,ranks in teamList]
		
		"""
		#Write to file
		f = open('myfile.txt','a')
		f.write(out)
		f.close()
		"""

		return(teamRanks)	
		
