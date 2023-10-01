# Scrapy settings for ApartamentRentScraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "ApartamentRentScraper"

SPIDER_MODULES = ["ApartamentRentScraper.spiders"]
NEWSPIDER_MODULE = "ApartamentRentScraper.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "ApartamentRentScraper (+http://www.yourdomain.com)"
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64'
# Obey robots.txt rules
ROBOTSTXT_OBEY = True




SELENIUM_DRIVER_NAME = 'undetected'
# SELENIUM_DRIVER_EXECUTABLE_PATH = Put path to your driver here if DRIVER_NAME not undetected
SELENIUM_DRIVER_ARGUMENTS= ['--blink-settings=imagesEnabled=false'] 
# For headless add '--headless'
# to disable images '--blink-settings=imagesEnabled=false'
  
DOWNLOADER_MIDDLEWARES = {
    #  "ApartamentRentScraper.middlewares.SeleniumMiddleware": 800
     }

ITEM_PIPELINES = {
    "ApartamentRentScraper.pipelines.ApartamentScraperPipeline" : 300,
    # "ApartamentRentScraper.pipelines.MySQLPipeline" : 301,
    # "ApartamentRentScraper.pipelines.CassandraPipeline" : 302,
}

# MySQL settings

# MYSQL_URL = "mysql+pymysql://user:password@host:port/dataset"
MYSQL_URL = "mysql+pymysql://root:mysqlpassword@localhost:3306/apartaments"

# Cassandra settings
# ================== 
CASSANDRA_HOST = "localhost"
CASSANDRA_PORT = 9042
CASSANDRA_KEYSPACE = "apartaments" 
# ==================
BATCH_SIZE = 100

# logging

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'log.txt'
LOG_FORMAT = '[%(name)s] %(levelname)s: %(message)s'


# JOBDIR = './jobcache'

DUPEFILTER_DEBUG = True


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "ApartamentRentScraper.middlewares.ApartamentrentscraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "ApartamentRentScraper.middlewares.ApartamentrentscraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "ApartamentRentScraper.pipelines.ApartamentrentscraperPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
