import re
import csv
from bs4 import BeautifulSoup
from urllib import request

#Team name, No city

SITE = 'foxsports.com'
URL = 'http://msn.foxsports.com/nba/powerRankings'


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

class ScrapeFoxSports:

	def __init__(self):

		nba_pr  = request.urlopen(URL).read()
		self.soup = BeautifulSoup(nba_pr)

	def getSite(self):
		return(SITE)
	
	def getUrl(self):
		return(URL)

	def getDatePublished(self):
		date_raw = self.soup.find('div','pr_artical_content')
		date_parsed = re.search('(?:\s)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?:\w+\s)(\d+)(?:,\s)(\d+)',date_raw.i.text)
		date = date_parsed.group(3) + '-' + str(self.monthToNum(date_parsed.group(1))).zfill(2) + '-' + str(date_parsed.group(2)).zfill(2)
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
	
	def getRanks(self):
		#Create rankings list
		ratings_raw = self.soup.find_all('a','teamLogo')
		i = 1
		teamList = []
		for rank in ratings_raw:
			teamList.append((self.nameToShortName(rank.text.strip()),i))
			i+=1

		teamList.sort()
		teamRanks = [ranks for names,ranks in teamList]

		return(teamRanks)