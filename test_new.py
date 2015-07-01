import pymysql
from scrape_nba_com1 import ScrapeNba
from scrape_espn_com import ScrapeEspn
from scrape_bleacherreport_com import ScrapeBleacherReport
from scrape_foxsports_com import ScrapeFoxSports
from scrape_cbssports_com import ScrapeCbsSports
from scrape_sbnation_com import ScrapeSbNation
from scrape_nbcsports_com import ScrapeNbcSports
from scrape_nbc_com import ScrapeNbc
from scrape_cnnsi_com import ScrapeCnnSi
	
def testScraper(scraper):
		
		print(scraper.getSite())
		print(scraper.getDatePublished())
		print(scraper.getRanks())		
		print('Test concluded.')
		
testScraper(ScrapeBleacherReport())
