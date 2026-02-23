"""Module responsible for scraping subject information from Fenix subject pages."""

import os
from pathlib import Path

from bs4 import BeautifulSoup
from fenix_scraper.parsers.html import parse_html
from fenix_scraper.utils.settings import SubjectSubPageSettings
from fenix_scraper.writers.markdown import write_markdown
from html_to_markdown import ConversionOptions, convert


def _get_subject_id_from_url(subject_url: str) -> str:
    """
    Extract the subject ID from the given Fenix subject URL.

    Args:
        subject_url (str): The URL of the Fenix subject page.

    Returns:
        str: The extracted course ID.

    """
    # Example URL: https://fenix.tecnico.ulisboa.pt/disciplinas/FP451795/2017-2018/1-semestre
    # The subject ID is the part after "disciplinas/" and before the next "/"
    try:
        subject_id = subject_url.split("/disciplinas/")[1].split("/")[0]
        return subject_id
    except IndexError:
        raise ValueError(f"Invalid subject URL format: {subject_url}") from None


def _get_subject_header(soup: BeautifulSoup) -> str:
    """
    Extract the subject header from the given BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the HTML content of the subject page.

    Returns:
        str: The extracted subject header.

    """
    subject_header = soup.find("h2", class_="site-header")
    if subject_header is None:
        raise ValueError("Subject header not found")

    children = subject_header.findChildren()
    if not children:
        raise ValueError("Subject header has no children")

    text = getattr(children[0], "text", None)
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Subject header child text is missing or invalid")

    return text.strip()


def _scrape_generic_content(soup: BeautifulSoup) -> str:
    """
    Scrape generic content from the given BeautifulSoup object and convert it to markdown format.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the HTML content to scrape.

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
    return convert(str(content), options)


def _scrape_subject_initial_page(output_path: Path, subject_id: str, subject_url: str) -> None:
    """
    Scrape the subject initial page from the given Fenix subject URL and save it as a markdown file.

    Args:
        output_path (Path): The directory where the subject initial page markdown file will be saved.
        subject_id (str): The ID of the subject.
        subject_url (str): The URL of the Fenix subject page to scrape.

    """
    page_url = f"{subject_url}/pagina-inicial"
    write_path = output_path / "📄 01 - Initial Page.md"

    soup = parse_html(page_url)
    subject_name = _get_subject_header(soup)

    subject_content_markdown = _scrape_generic_content(soup)

    tags = [subject_id, "subject", "initial-page"]
    metadata = {
        "subject-id": subject_id,
        "subject-name": subject_name,
        "subject-url": subject_url,
    }

    write_markdown(write_path, tags, metadata, subject_content_markdown)


def _scrape_subject_sub_page(
    output_path: Path, subject_id: str, subject_url: str, sub_page: tuple[int, SubjectSubPageSettings]
) -> None:
    """
    Scrape a specific subject sub-page from the given Fenix subject URL and save it as a markdown file.

    Args:
        output_path (Path): The directory where the subject sub-page markdown file will be saved.
        subject_id (str): The ID of the subject.
        subject_url (str): The URL of the Fenix subject page to scrape.
        sub_page (tuple[int, SubjectSubPageSettings]): A tuple containing the index and settings for the
            subject sub-pageto scrape.

    """
    sub_page_index, sub_page_settings = sub_page
    page_url = f"{subject_url}{sub_page_settings.url_suffix}"
    write_path = output_path / f"📄 {sub_page_index + 2:02d} - {sub_page_settings.name}.md"

    soup = parse_html(page_url)
    subject_name = _get_subject_header(soup)

    subject_content_markdown = _scrape_generic_content(soup)

    tags = [subject_id, "subject", sub_page_settings.name.lower().replace(" ", "-")]
    metadata = {
        "subject-id": subject_id,
        "subject-name": subject_name,
        "subject-url": page_url,
    }

    write_markdown(write_path, tags, metadata, subject_content_markdown)


def scrape(output_path: Path, subject_url: str, subject_subpages: list[SubjectSubPageSettings]) -> None:
    """
    Scrape subject information from the given Fenix subject URL.

    Args:
        output_path (Path): The directory where the scraped subject information will be saved.
        subject_url (str): The URL of the Fenix subject page to scrape.
        subject_subpages (list[SubjectSubPageSettings]): List of sub-pages within the subject.

    """
    subject_id = _get_subject_id_from_url(subject_url).upper()
    subject_directory = output_path / f"📁 Subject: {subject_id}"
    os.makedirs(subject_directory, exist_ok=True)

    _scrape_subject_initial_page(subject_directory, subject_id, subject_url)
    for sub_page in enumerate(subject_subpages):
        _scrape_subject_sub_page(subject_directory, subject_id, subject_url, sub_page)
