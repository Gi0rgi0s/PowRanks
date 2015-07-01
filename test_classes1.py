import pymysql
from scrape_nba_com1 import ScrapeNba
from scrape_espn_com import ScrapeEspn
from scrape_bleacherreport_com import ScrapeBleacherReport
from scrape_foxsports_com import ScrapeFoxSports
from scrape_sbnation_com import ScrapeSbNation
from scrape_cbssports_com import ScrapeCbsSports
from scrape_nbcsports_com import ScrapeNbcSports


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
	sql = 'SELECT date, site FROM pr WHERE date = \'' + date + '\'  AND site=  \'' + site + '\'';
	cur.execute(sql)
	return(cur.fetchone())

def insertSql(scraper):

	date = scraper.getDatePublished()
	site = scraper.getSite()

	if checkSql(date,site) is None:
		ranks = scraper.getRanks()
		params = '%s,' * 29 + '%s'
		sql  = 'INSERT INTO pr (' + 'date,site,' + ','.join(teamNames) + ') VALUES (\'' + date + '\',\'' + site + '\',%s);' % params		
		cur.execute(sql, ranks)
		print(ranks)
		print(site + ' updated on ' + date + '.')
	print(site + ' done.')
	
#--------------------Call Scrapers-------------------------
insertSql(ScrapeNba())
insertSql(ScrapeEspn())
insertSql(ScrapeBleacherReport())
insertSql(ScrapeFoxSports())
insertSql(ScrapeNbcSports())
insertSql(ScrapeCbsSports())
insertSql(ScrapeSbNation())
db.commit()
db.close()

	
print('All done.')