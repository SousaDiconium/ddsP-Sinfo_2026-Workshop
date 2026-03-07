"""Module for scraping generic content from a webpage and converting it to markdown format."""

from bs4 import BeautifulSoup
from fenix_scraper.scrapers.generic_page_visitor import PageVisitor
from html_to_markdown import ConversionOptions, convert_with_visitor


def scrape_generic_content(soup: BeautifulSoup, visitor: PageVisitor | None) -> str:
    """
    Scrape generic content from the given BeautifulSoup object and convert it to markdown format.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the HTML content to scrape.
        visitor (PageVisitor | None): The visitor instance to handle link processing during conversion.

    Returns:
        str: The scraped content in markdown format.

    """
    blacklisted_ids = ["myModal"]

    content_block = soup.find("div", id="content-block")
    if content_block is None:
        raise ValueError("content-block div not found")

    children = [child for child in content_block.find_all(recursive=False) if child.get("id") not in blacklisted_ids]
    content = "".join(str(child) for child in children)

    options = ConversionOptions(
        heading_style="atx",
        list_indent_width=2,
    )

    markdown = convert_with_visitor(str(content), options, visitor=visitor)
    return markdown
