"""Main entry point for the Fenix Scraper application."""

import argparse
from pathlib import Path

from loguru import logger
from tqdm import tqdm

from fenix_scraper import settings
from fenix_scraper.scrapers.course_scraper import scrape as scrape_course
from fenix_scraper.scrapers.subject_scraper import scrape as scrape_subject

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
# Process the courses from settings
for course in tqdm(settings.courses, desc="Scraping courses"):
    logger.info(f"Scraping course: {course.course_url}")
    course_path = scrape_course(output_path, course.course_url)

    for subject in tqdm(course.subjects, desc="Scraping subjects"):
        logger.info(f"Scraping subject: {subject.subject_url}")
        scrape_subject(course_path, subject.subject_url, subject.sub_pages)
