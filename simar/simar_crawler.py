from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl('simar_roturas', domain='simar-louresodivelas.pt')
process.start() # the script will block here until the crawling is finished