import re
import csv
from bs4 import BeautifulSoup
from urllib import request

SITE = 'cnnsi.com'

#HARDCODED URL
URL = 'http://sportsillustrated.cnn.com/nba/news/20140310/nba-power-rankings-los-angeles-clippers-miami-heat/'

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


class ScrapeCnnSi:

	def __init__(self,URL=URL):
		#Initialize Beautiful Soup
		#Pull NBA.com power rankings and parse
		self.nba_pr  = request.urlopen(URL).read()
		self.soup = BeautifulSoup(self.nba_pr)
		print('----------------CNNSi.com Initialized----------------')

	def getSite(self):
		return(SITE)
		
	def getUrl(self):
		return(URL)
		
	def monthToNum(self,date): #IMPROVEMENT: make this enum type

		return{
				'January' : 1,
				'February' : 2,
				'March' : 3,
				'April' : 4,
				'May' : 5,
				'June' : 6,
				'July' : 7,
			 	'August' : 8,
				'September' : 9, 
				'October' : 10,
				'November' : 11,
				'December' : 12
		}[date]

	def nameToShortName(self,name):

		return{

			'thunder' : 'OKC',
			'pacers' : 'IND',
			'rockets': 'HOU',
			'heat' : 'MIA' ,
			'clippers' : 'LAC',
			'spurs'  : 'SAS',
			'mavericks' : 'DAL',
			'suns' : 'PHX',
			'grizzlies' : 'MEM',
			'trail_blazers' : 'POR',
			'raptors' : 'TOR',
			'warriors' : 'GSW',
			'bulls' : 'CHI',
			'wizards' : 'WAS',
			'nets' : 'BKN',
			'hawks' : 'ATL',
			'timberwolves' : 'MIN',
			'bobcats' : 'CHA',
			'pelicans' : 'NOH',
			'pistons' : 'DET',
			'knicks' : 'NYK',
			'nuggets' : 'DEN',
			'jazz' : 'UTA',
			'magic' : 'ORL',
			'cavaliers' : 'CLE',
			'celtics' : 'BOS',
			'kings' : 'SAC',
			'lakers' : 'LAL',
			'bucks' : 'MIL',
			'76ers' : 'PHI'
		}[name]

	def getDatePublished(self):
	
		date_raw = self.soup.find('div', id='cnnTimeStamp')
		
		p = re.search('(January|February|March|April|May|June|July|August|September|October|November|December)\s(\d+)(?:,\s)(20\d+)',date_raw.div.text)
		date_parsed = [ self.monthToNum(p.group(1)), (p.group(2)), (p.group(3)) ]
		date = date_parsed[2] + '-' + str(date_parsed[0]).zfill(2) + '-' + str(date_parsed[1]).zfill(2)
		
		return(date)

		#Put all data in string
	
	def getRanks(self):

		teamList = []
		#Initialize Beautiful Soup
		
		#Pull NBA.com power rankings and parse
		
		ratings_raw = self.soup.find_all('td', 'col1')
		
		#Create rankings list
		i = 0

		#IMPROVEMENT: why not create a list with team names and enumerate()
		for rank in ratings_raw:
		#	teamList.append((self.nameToShortName(rank.span.b.text),i))
			i+=1
			if i % 2 != 0:
				p = re.search('(?:/teams/)([\d\w]+)([?:/])',rank.a['href'])
				teamList.append((self.nameToShortName(p.group(1)),int((i+1)/2)))
	
		teamList.sort()
		teamRanks = [ranks for names,ranks in teamList]

		return(teamRanks)	
		
