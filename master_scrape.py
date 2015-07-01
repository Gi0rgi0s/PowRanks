import pymysql
from scrape_nba_com import ScrapeNba
from scrape_espn_com import ScrapeEspn
from scrape_bleacherreport_com import ScrapeBleacherReport
from scrape_foxsports_com import ScrapeFoxSports
from scrape_sbnation_com import ScrapeSbNation
from scrape_cbssports_com import ScrapeCbsSports
from scrape_nbcsports_com import ScrapeNbcSports
from scrape_nbc_com import ScrapeNbc
from scrape_cnnsi_com import ScrapeCnnSi

#----------------------Current Tasks-----------------------
#1. Add try / catch inside all scraper objects
#2. Scrapers should return booleans
#3. Execute scrapers in loop with array pointing to functions
#4. Figure out way to knock out hardcoded URLs

#---------------------Hardcoded URLs-----------------------

URL_CNNSI = 'http://sportsillustrated.cnn.com/nba/news/20140331/nba-power-rankings-spurs-76ers-pacers-heat-knicks/'
URL_BLEACHER_REPORT = 'http://bleacherreport.com/articles/2008630-nba-power-rankings-whos-rising-and-whos-falling-fast-as-playoffs-approach'
URL_NBC = 'http://probasketballtalk.nbcsports.com/2014/03/31/pbt-power-rankings-spurs-running-away-at-top-but-a-new-team-in-cellar/'
#-----------------------Team Names-------------------------
teamNames = ['atl','bkn','bos',	'cha','chi','cle','dal','den','det','gsw','hou','ind','lac','lal','mem','mia','mil','min','noh','nyk','okc','orl','phi','phx','por','sac','sas','tor','uta','was']

#--------------------SQL Functionality---------------------
def checkSql(date,site):
	print(site + ': Checking for existing record...')
	sql = 'SELECT date, site FROM prn WHERE date = \'' + date + '\'  AND site=  \'' + site + '\'';

	cur.execute(sql)
	print(site + ': Duplicate check complete.')

	return(cur.fetchone())

def insertSql(scraper):
	
	url = scraper.getUrl()
	site = scraper.getSite()
	print(site + ': Scraping date published...')
	date = scraper.getDatePublished()
	print(site + ': Scrape complete.')

	if checkSql(date,site) is None:
		print(site + ': Scraping ranks from ' + url + '...')
		ranks = scraper.getRanks()
		print(site + ': Scrape complete.')
		print(site + ': Inserting ranks into database...')
		print(ranks)
		params = '%s,' * 29 + '%s'
		sql  = 'INSERT INTO prn (' + 'date,url,site,' + ','.join(teamNames) + ') VALUES (\'' + date + '\',\'' + url + '\',\'' + site + '\' ,%s);' % params
		#print(sql)
		cur.execute(sql, ranks)
		print(site + ': updated on ' + date + '.')
		print(site + ': Insertion complete.')

	print(site + ': done.')

#---------------Entry Point: Begin Program-----------------

#------------------Initialize Database---------------------
db = pymysql.connect("powranks.com","George","Powrankings1","PowRanks")
cur = db.cursor()

#--------------------Call Scrapers-------------------------
print('//////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
print('||||||||||||||||||NBA Master Scraper|||||||||||||||||')
print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\///////////////////////////')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~~Begin Fast Scrapers~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

##insertSql(ScrapeNba())
#insertSql(ScrapeEspn())
#insertSql(ScrapeFoxSports())
#insertSql(ScrapeSbNation())

#------------HARDCODED
#insertSql(ScrapeCnnSi(URL_CNNSI))
##insertSql(ScrapeBleacherReport(URL_BLEACHER_REPORT))
#(ScrapeNbcSports()) #DATE HARDCODED - COMMENTED BECAUSE IT NEVER UPDATES

#------------Slow  and/or HARDCODED
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~~Begin Slow Scrapers~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

#insertSql(ScrapeNbc(URL_NBC))	 #URL HARDCODED
insertSql(ScrapeCbsSports())

#----------------Commit Changes to Database----------------
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~~~Scrapers Complete~~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

print('Commiting changes to database (if any)...')
db.commit()
print('Commit complete.')
db.close()


print('//////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
print('|||||||||||||||Master Scraper Complete|||||||||||||||')
print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\///////////////////////////')