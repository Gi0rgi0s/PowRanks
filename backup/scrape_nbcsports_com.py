import re
import csv
from bs4 import BeautifulSoup
from urllib import request

bs = BeautifulSoup
SITE = 'nbcsports.com'
URL = 'http://www.nbcsports.com/basketball/nba/pbts-power-rankings'

DATE  = '2014-03-07'

#getRanks
	#unique modulus system due to BS behavior and strange class names
#getDatePublished
	#hard coded date

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

class ScrapeNbcSports:

	def __init__(self):
		#Initialize Beautiful Soup
		#Pull NBA.com power rankings and parse
		nba_pr  = request.urlopen(URL).read()
		self.soup = BeautifulSoup(nba_pr)

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

			'Oklahoma City Thunder' : 'OKC',
			'Indiana Pacers' : 'IND',
			'Houston Rockets': 'HOU',
			'Miami Heat' : 'MIA' ,
			'Los Angeles Clippers' : 'LAC',
			'San Antonio Spurs'  : 'SAS',
			'Dallas Mavericks' : 'DAL',
			'Phoenix Suns' : 'PHX',
			'Memphis Grizzlies' : 'MEM',
			'Portland Trail Blazers' : 'POR',
			'Toronto Raptors' : 'TOR',
			'Golden State Warriors' : 'GSW',
			'Chicago Bulls' : 'CHI',
			'Washington Wizards' : 'WAS',
			'Brooklyn Nets' : 'BKN',
			'Atlanta Hawks' : 'ATL',
			'Minnesota Timberwolves' : 'MIN',
			'Charlotte Bobcats' : 'CHA',
			'New Orleans Pelicans' : 'NOH',
			'Detroit Pistons' : 'DET',
			'New York Knicks' : 'NYK',
			'Denver Nuggets' : 'DEN',
			'Utah Jazz' : 'UTA',
			'Orlando Magic' : 'ORL',
			'Cleveland Cavaliers' : 'CLE',
			'Boston Celtics' : 'BOS',
			'Sacramento Kings' : 'SAC',
			'Los Angeles Lakers' : 'LAL',
			'Milwaukee Bucks' : 'MIL',
			'Philadelphia' : 'PHI'
		}[name]

	def getDatePublished(self):
		return(DATE)

		#Put all data in string
	
	def getRanks(self):

		teamList = []
		#Initialize Beautiful Soup
		#Pull NBA.com power rankings and parse
		
		ratings_raw = self.soup.find_all('div','field-item even')

		#Create rankings list

		i = 1
		#IMPROVEMENT: why not create a list with team names and enumerate()
		for rank in ratings_raw:
			if (i - 2) % 4 == 0 and i > 5:
				p = re.search('(\d+)(?:\.\s)([a-zA-Z\s]+)',rank.text)				
				teamList.append((self.nameToShortName(p.group(2).strip()),int(p.group(1))))

			i+=1
			
		teamList.sort()
		teamRanks = [ranks for names,ranks in teamList]
		
		return(teamRanks)	
		
