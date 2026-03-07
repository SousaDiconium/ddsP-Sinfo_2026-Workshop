"""Module for parsing HTML content from Fenix course pages."""

from pathlib import Path

import requests
from bs4 import BeautifulSoup
from fenix_scraper import settings
from loguru import logger

COOKIES = {
    "i18n.locale": "en-GB",
    "JSESSIONID": settings.jsession_id,
}


def _get_html_from_url(url: str) -> str:
    """
    Fetch the HTML content of the given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the page.

    """
    try:
        response = requests.get(url, cookies=COOKIES, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        raise


def parse_html(url: str) -> BeautifulSoup:
    """
    Parse the HTML content from the given URL.

    Args:
        url (str): The URL to parse.

    Returns:
        BeautifulSoup: The parsed HTML content of the page.

    """
    html_doc = _get_html_from_url(url)
    soup = BeautifulSoup(html_doc, "html.parser")
    return soup


def download_attachment(url: str, save_path: Path) -> None:
    """
    Download an attachment from the given URL and save it to the specified filename.

    Args:
        url (str): The URL of the attachment to download.
        save_path (Path): The local path where the attachment will be saved.

    """
    try:
        logger.info(f"Downloading attachment from {url} to {save_path}")
        response = requests.get(url, cookies=COOKIES, stream=True, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors

        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        logger.debug(f"Downloaded {url} to {save_path}")
    except requests.RequestException as e:
        logger.error(f"Error downloading attachment from {url}: {e}")
        raise
