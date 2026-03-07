"""Module for visiting links on a generic page and handling attachments."""

from pathlib import Path

from fenix_scraper.utils.web_utils import download_attachment


class PageVisitor:
    """Visitor class for handling links and attachments on a generic page."""

    domain_url: str
    attachments_directory: Path
    page_key: str
    blacklisted_attachments: list[str]

    def __init__(
        self,
        domain_url: str,
        attachments_directory: Path,
        page_key: str,
        blacklisted_attachments: list[str] | None = None,
    ) -> None:
        """
        PageVisitor initialization with the necessary information to handle links and attachments.

        Args:
            domain_url (str): The base URL of the domain to resolve relative links.
            attachments_directory (Path): The directory where attachments will be saved.
            page_key (str): A unique key for the page, used in naming attachments.
            blacklisted_attachments (list[str], optional): A list of attachment URLs to ignore. Defaults to None.

        """
        self.domain_url = domain_url
        self.attachments_directory = attachments_directory
        self.page_key = page_key
        self.blacklisted_attachments = blacklisted_attachments or []

    def visit_link(self, ctx: object, href: str, text: str, title: str) -> dict[str, str]:
        """
        Visits a link and handles it based on its type.

        This method comes from the LinkVisitor interface and is called for each link found on the page.
        It checks if the link is a relative URL or an attachment (PDF) and processes it accordingly.

        Args:
            ctx: The context of the visit (not used in this implementation).
            href (str): The URL of the link.
            text (str): The text of the link.
            title (str): The title of the link (not used in this implementation).

        Returns:
            dict[str, str]: A dictionary indicating the type of action to take and the output.

        """
        if href.startswith("/"):
            new_url = f"{self.domain_url}{href}"
            return {"type": "custom", "output": f"[{text}]({new_url})"}

        if not href or not href.endswith(".pdf"):
            return {"type": "continue"}

        filename = href.split("/")[-1]
        new_filename = f"{self.page_key}_{filename}"
        save_path = self.attachments_directory / new_filename

        if href in self.blacklisted_attachments:
            return {"type": "continue"}

        try:
            download_attachment(href, save_path)
            return {"type": "custom", "output": f"[[{new_filename}]] (originally: [link]({href}))"}

        except Exception as e:
            print(f"Failed to download {href}: {e}")
            return {"type": "continue"}
