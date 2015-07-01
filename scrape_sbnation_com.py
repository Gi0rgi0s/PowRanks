import re
from bs4 import BeautifulSoup
from urllib import request

SITE = 'sbnation.com'
URL = 'http://www.sbnation.com/nba-power-rankings/'

#__init__

	#Rankings URL buried, two urllib requests made

#getRanks

	#Ranking number can be scraped

#nameToShortName

	#Full team names, exception 76ers

#getDatePublsihed

	#date needed to be encoded to utf-8

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
			
class ScrapeSbNation:

	def __init__(self,URL=URL):
		#Pull power rankings and parse	
		#Find power ranks link on main page		
		
		nba_pre_pr  = request.urlopen(URL).read()
		self.soup = BeautifulSoup(nba_pre_pr)
		pr_url = self.soup.find('div','m-block__body')
		self.nba_pr = request.urlopen(pr_url.header.h3.a['href']).read()
		self.soup = BeautifulSoup(self.nba_pr)
		print('---------------SbNation.com Initialized--------------')

		
	def getSite(self):
		return(SITE)
		
	def getUrl(self):
		return(URL)
	
	def getDatePublished(self):
		
		date_raw = self.soup.find('p','m-entry__byline')
		regex = '(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?:\s)(\d+)(?:\s)(\d+)'
		p = re.search(regex,str(date_raw.text.encode('utf-8')))
		
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

	def getRanks(self):
		teamRanks = ''

		teamList = []
		ratings_raw = self.soup.find_all('h4')

		for rank in ratings_raw:
			p = re.search('(\d+)(?:\.\s)([a-zA-Z\s]+)',rank.text)
			if(p is not None):
				#print(p.group(0))
				#print(p.group(1))
				#print(p.group(2).strip() + '---')
				teamList.append((self.nameToShortName(p.group(2).strip()),int(p.group(1))))

		teamList.sort()
		teamRanks = [ranks for names,ranks in teamList]
		#teamNames = [names for names,ranks in teamList]
		return(teamRanks)