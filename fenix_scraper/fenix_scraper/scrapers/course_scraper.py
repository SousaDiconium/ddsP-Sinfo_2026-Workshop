"""Module responsible for scraping course information from Fenix course pages."""

import os
from pathlib import Path

from bs4 import BeautifulSoup
from fenix_scraper.scrapers.generic_scraper import scrape_generic_content
from fenix_scraper.utils.web_utils import parse_html
from fenix_scraper.writers.markdown import write_markdown


def _get_course_id_from_url(course_url: str) -> str:
    """
    Extract the course ID from the given Fenix course URL.

    Args:
        course_url (str): The URL of the Fenix course page.

    Returns:
        str: The extracted course ID.

    """
    # Example URL: https://fenix.tecnico.ulisboa.pt/cursos/leic-a/descricao
    # The course ID is the part after "cursos/" and before the next "/"
    try:
        course_id = course_url.split("/cursos/")[1].split("/")[0]
        return course_id
    except IndexError:
        raise ValueError(f"Invalid course URL format: {course_url}") from None


def _get_course_header(soup: BeautifulSoup) -> str:
    """
    Extract the course header from the given BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the HTML content of the course page.

    Returns:
        str: The extracted course header.

    """
    course_header = soup.find("h2", class_="site-header")
    if course_header is None:
        raise ValueError("Course header not found")

    children = course_header.findChildren()
    if not children:
        raise ValueError("Course header has no children")

    text = getattr(children[0], "text", None)
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Course header child text is missing or invalid")

    return text.strip()


def _scrape_course_description(output_path: Path, course_id: str, course_url: str) -> None:
    """
    Scrape the course description from the given Fenix course URL and save it as a markdown file.

    Args:
        output_path (Path): The directory where the course description markdown file will be saved.
        course_id (str): The ID of the course.
        course_url (str): The URL of the Fenix course page to scrape.

    """
    page_url = f"{course_url}/descricao"
    write_path = output_path / "📄 01 - Course Description.md"

    soup = parse_html(page_url)
    course_name = _get_course_header(soup)

    course_content_markdown = scrape_generic_content(soup, visitor=None)

    tags = [course_id, "course", "description"]
    metadata = {
        "course-id": course_id,
        "course-name": course_name,
        "course-url": course_url,
    }

    write_markdown(write_path, tags, metadata, course_content_markdown)


def _scrape_announcements(output_path: Path, course_id: str, course_url: str) -> None:
    """
    Scrape the course announcements from the given Fenix course URL and save them as markdown files.

    Args:
        output_path (Path): The directory where the course announcements markdown files will be saved.
        course_id (str): The ID of the course.
        course_url (str): The URL of the Fenix course page to scrape.

    """
    page_url = f"{course_url}/anuncios"
    write_path = output_path / "📄 02 - Announcements.md"

    soup = parse_html(page_url)
    course_name = _get_course_header(soup)
    course_content_markdown = scrape_generic_content(soup, visitor=None)

    tags = [course_id, "course", "description"]
    metadata = {
        "course-id": course_id,
        "course-name": course_name,
        "course-url": course_url,
    }

    write_markdown(write_path, tags, metadata, course_content_markdown)


def _scrape_admission_requirements(output_path: Path, course_id: str, course_url: str) -> None:
    """
    Scrape the course admission requirements from the given Fenix course URL and save them as markdown files.

    Args:
        output_path (Path): The directory where the course admission requirements markdown files will be saved.
        course_id (str): The ID of the course.
        course_url (str): The URL of the Fenix course page to scrape.

    """
    page_url = f"{course_url}/regime-de-acesso"
    write_path = output_path / "📄 03 - Admission Requirements.md"

    soup = parse_html(page_url)
    course_name = _get_course_header(soup)
    course_content_markdown = scrape_generic_content(soup, visitor=None)

    tags = [course_id, "course", "admission-requirements"]
    metadata = {
        "course-id": course_id,
        "course-name": course_name,
        "course-url": course_url,
    }

    write_markdown(write_path, tags, metadata, course_content_markdown)


def _scrape_master_transition(output_path: Path, course_id: str, course_url: str) -> None:
    """
    Scrape the course master transition information from the given Fenix course URL and save it as a markdown file.

    Args:
        output_path (Path): The directory where the course master transition markdown file will be saved.
        course_id (str): The ID of the course.
        course_url (str): The URL of the Fenix course page to scrape.

    """
    page_url = f"{course_url}/transicao-para-o-mestrado"
    write_path = output_path / "📄 04 - Master Transition.md"

    soup = parse_html(page_url)
    course_name = _get_course_header(soup)
    course_content_markdown = scrape_generic_content(soup, visitor=None)

    tags = [course_id, "course", "master-transition"]
    metadata = {
        "course-id": course_id,
        "course-name": course_name,
        "course-url": course_url,
    }

    write_markdown(write_path, tags, metadata, course_content_markdown)


def scrape(output_path: Path, course_url: str) -> Path:
    """
    Scrape course information from the given Fenix course URL.

    Args:
        output_path (Path): The directory where the scraped course information will be saved.
        course_url (str): The URL of the Fenix course page to scrape.

    Returns:
        Path: The path to the directory where the scraped course information is saved.

    """
    course_id = _get_course_id_from_url(course_url).upper()
    course_directory = output_path / f"🗂️ Course: {course_id}"
    os.makedirs(course_directory, exist_ok=True)

    _scrape_course_description(course_directory, course_id, course_url)
    _scrape_announcements(course_directory, course_id, course_url)
    _scrape_admission_requirements(course_directory, course_id, course_url)
    _scrape_master_transition(course_directory, course_id, course_url)

    return course_directory
