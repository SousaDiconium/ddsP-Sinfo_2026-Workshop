"""Main module for the Fenix Scraper package."""

from fenix_scraper.utils.logger import setup_logger
from fenix_scraper.utils.settings import Settings

# Initialize settings and logger
settings = Settings()
setup_logger(settings)
