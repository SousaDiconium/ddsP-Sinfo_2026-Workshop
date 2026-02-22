"""Main entry point for the Fenix Scraper application."""

import argparse
from pathlib import Path

from loguru import logger
from tqdm import tqdm

from fenix_scraper import settings
from fenix_scraper.scrapers.course_scraper import scrape

logger.info("Starting Fenix Scraper...")

parser = argparse.ArgumentParser(
    prog="Fenix Scraper",
    description="A web scraper for the Fenix course pages.",
    epilog="Use this tool to scrape course information from the Fenix platform.",
)

# Add arguments to the parser
parser.add_argument(
    "-o", "--output-folder", type=str, default="../knowledge", help="The folder where scraped data will be saved."
)
# Process the arguments
args = parser.parse_args()

output_path = Path(args.output_folder)
# Process the courses from settigns
for course_url in tqdm(settings.courses, desc="Scraping courses"):
    logger.info(f"Scraping course: {course_url}")

    try:
        scrape(output_path, course_url)
    except Exception as e:
        logger.error(f"Error scraping course {course_url}: {e}")
