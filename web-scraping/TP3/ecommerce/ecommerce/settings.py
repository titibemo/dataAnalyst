# Scrapy settings for the ecommerce project
#
# This file contains the main configuration for the Scrapy spider.
# Only important and commonly used settings are included.
# Full documentation:
# https://docs.scrapy.org/en/latest/topics/settings.html
# https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# ----------------------
# Basic project settings DO NOT TOUCH !
# ----------------------
BOT_NAME = "ecommerce"  # Name of the Scrapy bot

SPIDER_MODULES = ["ecommerce.spiders"]  # Location of spider modules
NEWSPIDER_MODULE = "ecommerce.spiders"  # Default module for new spiders

ADDONS = {}  # Placeholder for additional custom settings

# ----------------------
# Crawl behavior
# ----------------------
ROBOTSTXT_OBEY = True  # Respect robots.txt rules

# Control the number of concurrent requests and throttling
CONCURRENT_REQUESTS_PER_DOMAIN = 1  # Limit requests per domain
DOWNLOAD_DELAY = 1                   # Delay between requests (seconds)

# ----------------------
# Feed export encoding
# ----------------------
FEED_EXPORT_ENCODING = "utf-8"  # Ensure exported files use UTF-8 encoding

# ----------------------
# Item pipelines
# ----------------------
# Defines the order in which pipelines are applied (lower values processed first)
ITEM_PIPELINES = {
    "ecommerce.pipelines.DuplicatesPipeline": 100,         # Remove duplicate items
    "ecommerce.pipelines.PriceConversionPipeline": 200,    # Convert price strings to float
    "ecommerce.pipelines.ExcelWriterPipeline": 300,        # Save items to Excel
    "ecommerce.pipelines.JsonArchivePipeline": 400,        # Archive items in JSON
}

# ----------------------
# Downloader middlewares
# ----------------------
# Custom middlewares for modifying requests (e.g., User-Agent rotation)
DOWNLOADER_MIDDLEWARES = {
    "ecommerce.middlewares.UserAgentMiddleware": 500,
}

# ----------------------
# Logging settings
# ----------------------
LOG_ENABLED = True                  # Enable logging
LOG_FILE = 'log/rapport.log'        # Log file path
LOG_LEVEL = 'INFO'                  # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL

