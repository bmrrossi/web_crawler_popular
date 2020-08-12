BOT_NAME = 'web_crawler_popular'

SPIDER_MODULES = ['web_crawler_popular.spiders']
NEWSPIDER_MODULE = 'web_crawler_popular.spiders'

CLOSESPIDER_TIMEOUT = 180

DOWNLOAD_TIMEOUT = 200
DOWNLOAD_DELAY = 5

DEPTH_LIMIT = 15

EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
    'scrapy.extensions.closespider.CloseSpider': 1
}