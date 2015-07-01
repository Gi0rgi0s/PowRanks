#Last tested 14-11-11

import re
from bs4 import BeautifulSoup
from urllib import request

NAME = 'bleacherreport.com'
URL = 'http://bleacherreport.com/nba/'

#HARDCODED URL
#URL = 'http://bleacherreport.com/articles/1992194-nba-power-rankings-lay-of-the-land-heading-down-the-stretch'

	#Rankings URL buried, two urllib requests made
	#main page rankings link usually outdated, hardcode new URL everytime
	#14-11-11 Trying to scrape URL automatically
	
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

class ScrapeBleacherReport:

	def __init__(self,URL=URL):

		nba_pre_pr  = request.urlopen(URL).read()
		self.soup = BeautifulSoup(nba_pre_pr)
		pr_url = self.soup.find("a",text="NBA Power Rankings")
		self.nba_pr = request.urlopen(pr_url['href']).read()
		self.soup = BeautifulSoup(self.nba_pr)

		print('----------BleacherReport.com Initialized-------------')

	def getSite(self):
		return(NAME)

	def getUrl(self):
		return(URL)
		
	def getDatePublished(self):

		date_raw = self.soup.find('time')
		p = re.search('(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?:\s)(\d+)(?:\,\s)(\d+)',date_raw.text)
		date = p.group(3) + '-' + str(self.monthToNum(p.group(1))).zfill(2) + '-' + str(p.group(2)).zfill(2)

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
			'Charlotte Hornets' : 'CHA',
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
			'Philadelphia 76ers' : 'PHI'
		}[name]

	def getRanks(self):
	
		teamList = []
		
		ratings_raw = self.soup.find_all('h2','article_page-title')
		#ratings_raw = self.soup.find_all('strong')
		for rank in ratings_raw:
				p = re.search('(\d+)(?:\.\s)(\w+\s\w+\s\w+|\w+\s\w+)',rank.text)
				teamList.append((self.nameToShortName(p.group(2)),int(p.group(1))))
				if p.group(1) == '1':
					break
		
		teamList.sort()
		teamRanks = [ranks for names,ranks in teamList]
		#teamNames = [names for names,ranks in teamList]
		
		return(teamRanks)
