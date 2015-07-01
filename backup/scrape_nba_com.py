import re
import csv
from bs4 import BeautifulSoup
from urllib import request

SITE = 'nba.com'
URL = 'http://www.nba.com/powerrankings/'

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


class ScrapeNba:

	def __init__(self):
		#Initialize Beautiful Soup
		#Pull NBA.com power rankings and parse
		self.nba_pr  = request.urlopen(URL).read()
		self.soup = BeautifulSoup(self.nba_pr)

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

			'Oklahoma City' : 'okc',
			'Indiana' : 'ind',
			'Houston': 'hou',
			'Miami' : 'mia' ,
			'L.A. Clippers' : 'lac',
			'San Antonio'  : 'sas',
			'Dallas' : 'dal',
			'Phoenix' : 'phx',
			'Memphis' : 'mem',
			'Portland' : 'por',
			'Toronto' : 'tor',
			'Golden State' : 'gsw',
			'Chicago' : 'chi',
			'Washington' : 'was',
			'Brooklyn' : 'bkn',
			'Atlanta' : 'atl',
			'Minnesota' : 'min',
			'Charlotte' : 'cha',
			'New Orleans' : 'noh',
			'Detroit' : 'det',
			'New York' : 'nyk',
			'Denver' : 'den',
			'Utah' : 'uta',
			'Orlando' : 'orl',
			'Cleveland' : 'cle',
			'Boston' : 'bos',
			'Sacramento' : 'sac',
			'L.A. Lakers' : 'lal',
			'Milwaukee' : 'mil',
			'Philadelphia' : 'phi'
		}[name]

	def getDatePublished(self):
		#Initialize Beautiful Soup
		
		#Pull NBA.com power rankings and parse
		
		date_raw = self.soup.find('p', 'nbaStoryByLine')
		
		#Pull date and parse

		#print(date_raw.text)
		p = re.search('(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s(\d+)(?:,)\s(20\d+)',date_raw.text)
		#print(self.date_raw.text)
		#print(p.group(0) + "--")
		date_parsed = [ self.monthToNum(p.group(1)), (p.group(2)), (p.group(3)) ]
		date = date_parsed[2] + '-' + str(date_parsed[0]).zfill(2) + '-' + str(date_parsed[1]).zfill(2)

		return(date)

		#Put all data in string
	
	def getRanks(self):

		teamList = []
		#Initialize Beautiful Soup
		
		#Pull NBA.com power rankings and parse
		
		ratings_raw = self.soup.find_all('td', 'nbaPowerRankingsTableDesc')

		#Create rankings list
		i = 1

		#IMPROVEMENT: why not create a list with team names and enumerate()
		for rank in ratings_raw:
			teamList.append((self.nameToShortName(rank.span.b.text),i))
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
		
