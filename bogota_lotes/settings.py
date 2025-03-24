from dotenv import load_dotenv
import os

load_dotenv()

BOT_NAME = 'bogota_lotes'

SPIDER_MODULES = ['bogota_lotes.spiders']
NEWSPIDER_MODULE = 'bogota_lotes.spiders'

VERSION = '2.1.0'

# Database settings for local MongoDB
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'bogota_lotes'

# Collection names with default values
MONGO_COLLECTION_RAW = os.getenv('MONGO_COLLECTION_RAW', 'scrapy_bogota_lotes')
MONGO_COLLECTION_PROCESSED = os.getenv('MONGO_COLLECTION_PROCESSED', 'scrapy_bogota_lotes_processed')

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "bogota_lotes (+http://erik172.cloud)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = { 
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'bogota_lotes.pipelines.MongoDBPipeline': 500
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEED_EXPORT_ENCODING = 'utf-8'

# Logging settings
LOG_STDOUT = False