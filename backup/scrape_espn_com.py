import re
from bs4 import BeautifulSoup
from urllib import request


#Odd, Even class names
#Hardcoded year
#Redundant "Los Angeles"

YEAR = '2014'
boolNOLA = True
SITE = 'espn.com'
URL = 'http://espn.go.com/nba/powerrankings'

abr_list = ['ATL',
		'BKN',
		'BOS',
		'CHA',
		'CHI',
		'CLE',
		'DAL',
		'DEN',
		'DET',
		'GSW',
		'HOU',
		'IND',
		'LAC',
		'LAL',
		'MEM',
		'MIA',
		'MIL',
		'MIN',
		'NOH',
		'NYK',
		'OKC',
		'ORL',
		'PHI',
		'PHX',
		'POR',
		'SAC',
		'SAS',
		'TOR',
		'UTA',
		'WAS']



class ScrapeEspn:
	def __init__(self):

		nba_pr  = request.urlopen(URL).read()
		self.soup = BeautifulSoup(nba_pr)

	def getSite(self):
		return(SITE)

	def getUrl(self):
		return(URL)
		
	def getDatePublished(self):
		
		date_raw = self.soup.find('cite','source')

		p = re.search('(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?:\w+\s)(\d+)',date_raw.text)
		date_parsed = [ self.monthToNum(p.group(1)), (p.group(2))]
		date = YEAR + '-' + str(date_parsed[0]).zfill(2) + '-' + str(date_parsed[1]).zfill(2)
		
		return(date)
		
	def monthToNum(self,date):
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

			'Oklahoma City' : 'OKC',
			'Indiana' : 'IND',
			'Houston': 'HOU',
			'Miami' : 'MIA' ,
			'Clippers' : 'LAC',
			'San Antonio'  : 'SAS',
			'Dallas' : 'DAL',
			'Phoenix' : 'PHX',
			'Memphis' : 'MEM',
			'Portland' : 'POR',
			'Toronto' : 'TOR',
			'Golden State' : 'GSW',
			'Chicago' : 'CHI',
			'Washington' : 'WAS',
			'Brooklyn' : 'BKN',
			'Atlanta' : 'ATL',
			'Minnesota' : 'MIN',
			'Charlotte' : 'CHA',
			'New Orleans' : 'NOH',
			'Detroit' : 'DET',
			'New York' : 'NYK',
			'Denver' : 'DEN',
			'Utah' : 'UTA',
			'Orlando' : 'ORL',
			'Cleveland' : 'CLE',
			'Boston' : 'BOS',
			'Sacramento' : 'SAC',
			'Los Angeles' : 'LAL',
			'Milwaukee' : 'MIL',
			'Philadelphia' : 'PHI'
		}[name]

	def isLa(self,team):
		global boolNOLA
		if team == 'Los Angeles' and boolNOLA == True:
			team = 'Clippers'
			boolNOLA = False
		return(team)
			
	def getRanks(self):
	
		teamList = []
		
		#Pull NBA.com power rankings and parse
		ratings_raw_odd = self.soup.find_all('tr', 'oddrow')
		ratings_raw_even = self.soup.find_all('tr', 'evenrow')

		i = 1

		for even, odd in zip(ratings_raw_even, ratings_raw_odd):
			p = re.search('(?:[0-9]+)([A-Za-z]+\s?[A-Za-z]+?)(?:[0-9]+?)',odd.text)
			teamList.append((self.nameToShortName(self.isLa(p.group(1))),i)) 
			p = re.search('(?:[0-9]+)([A-Za-z]+\s?[A-Za-z]+?)(?:[0-9]+?)',even.text)
			teamList.append((self.nameToShortName(self.isLa(p.group(1))),i+1))
			i+=2

		teamList.sort()

		teamRanks = [ranks for names,ranks in teamList]
		#teamNames = [names for names,ranks in teamList]

		return(teamRanks)

"""
		#Write to file
		f = open('myfile.txt','a')
		f.write(out)
		f.close()
"""


