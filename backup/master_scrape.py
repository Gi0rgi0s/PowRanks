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

teamNames = ['atl',
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

db = pymysql.connect("powranks.com","George","Powrankings1","PowRanks")
cur = db.cursor()

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
		params = '%s,' * 29 + '%s'
		sql  = 'INSERT INTO prn (' + 'date,url,site,' + ','.join(teamNames) + ') VALUES (\'' + date + '\',\'' + url + '\',\'' + site + '\' ,%s);' % params
		#print(sql)
		cur.execute(sql, ranks)
		print(site + ': Insertion complete.')
		print(ranks)
		print(site + ': updated on ' + date + '.')
		print(site + ': Inserting ranks complete.')
	print(site + ': done.')
	
#--------------------Call Scrapers-------------------------

print('--------------------------------------------Scraping Nba')
insertSql(ScrapeNba())
print('--------------------------------------------Scraping Espn')
insertSql(ScrapeEspn())
print('--------------------------------------------Scraping FoxSports')
insertSql(ScrapeFoxSports())
print('--------------------------------------------Scraping SbNation')
insertSql(ScrapeSbNation())
print('--------------------------------------------Scraping NbcSports')

#------------HARDCODES
insertSql(ScrapeNbcSports()) #DATE HARDCODED
print('--------------------------------Scraping CnnSi')
insertSql(ScrapeCnnSi()) #URL HARDCODED
print('--------------------------------------------Scraping BleacherReport')# URL HARDCODED
insertSql(ScrapeBleacherReport()) #URL HARDCODED

#------------Slow  and/or HARDCODED
print('--------------------------------------------Scraping Nbc')
insertSql(ScrapeNbc()) #URL_HARDCODED
print('--------------------------------------------Scraping CbsSports')
insertSql(ScrapeCbsSports())

print('Commiting changes to database (if any)...')
db.commit()
print('Commit complete.')
db.close()
print('All done.')