"""Module for parsing HTML content from Fenix course pages."""

import requests
from bs4 import BeautifulSoup
from loguru import logger


def _get_html_from_url(url: str) -> str:
    """
    Fetch the HTML content of the given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the page.

    """
    cookies = {"i18n.locale": "en-GB"}

    try:
        response = requests.get(url, cookies=cookies, timeout=10)
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
