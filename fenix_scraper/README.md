# 🕷️ Fenix Scraper

> CLI tool that scrapes course and subject pages from [Fenix](https://fenix.tecnico.ulisboa.pt) and converts them into Obsidian vault markdown files.

> **Note:** This module is **not part of the workshop**. It's included for transparency so you can see how the sample data in the [`obsidian-vaults/`](../obsidian-vaults/) directory was extracted. You don't need to run it.

[⬅️ Back to main README](../README.md)

---

## 🤔 What does it do?

The scraper authenticates with Fenix using a session cookie, fetches course/subject pages, and converts the HTML into clean Markdown files with YAML frontmatter — ready to be indexed by the [Knowledge Service](../knowledge_service/README.md).

```
Fenix Website (authenticated)
  → HTTP fetch with JSESSION_ID cookie
    → BeautifulSoup HTML parsing
      → html-to-markdown conversion
        → .md files with YAML frontmatter
          → Obsidian Vault directory
```

The output files are structured as an [Obsidian](https://obsidian.md/) vault, making them easy to browse locally and perfect for ingestion into the RAG pipeline.

---

## ⚙️ How it was run

Here's how the sample data was extracted (for reference, not for the workshop):

### 1. Get a Fenix session cookie

1. Log in to [Fenix](https://fenix.tecnico.ulisboa.pt) in your browser
2. Open Developer Tools (F12) → **Application** tab → **Cookies**
3. Copy the value of the `JSESSIONID` cookie

### 2. Set up environment

```bash
# Copy the example env file
cp fenix_scraper/resources/.env.example fenix_scraper/resources/.env
```

Edit the `.env` file and paste your `JSESSIONID`:

```
JSESSION_ID=<your-session-cookie-value>
```

### 3. Run the scraper

```bash
uv run python -m fenix_scraper.main -o ../obsidian-vaults/test-sinfo-fenix-vault
```

This outputs markdown files into the specified vault directory. The scraper is configured via [`fenix_scraper/resources/config.yaml`](./fenix_scraper/resources/config.yaml) which specifies which courses and subjects to scrape.

---

## 📂 Project Structure

```
fenix_scraper/
├── fenix_scraper/
│   ├── __init__.py              # Settings and scraper initialization
│   ├── main.py                  # CLI entry point
│   ├── models/                  # Pydantic models for courses, subjects
│   ├── scrapers/                # Scraping logic (generic + Fenix-specific)
│   ├── resources/
│   │   ├── config.yaml          # Scraper configuration (courses to scrape)
│   │   ├── .env.example         # Environment variables template
│   │   └── .env                 # Your credentials (gitignored)
│   └── utils/                   # Settings, logger, markdown converter
├── pyproject.toml
└── README.md                    # You are here
```

---

## 🧰 Key Dependencies

| Package | Purpose |
|---|---|
| `beautifulsoup4` | HTML parsing |
| `html-to-markdown` | HTML → Markdown conversion |
| `requests` | HTTP client for fetching Fenix pages |
| `pydantic` + `pydantic-settings` | Configuration and data models |
| `loguru` | Logging |

---

## 📦 Installing Dependencies

All dependencies are managed from the **project root**:

```bash
# From the repo root
uv sync --all-packages
```

---

## 🛠️ Development

Run these from inside the `fenix_scraper/` directory:

```bash
# Format + lint (auto-fix)
uv run ruff format && uv run ruff check --fix

# Type check
uv run mypy .
```

---

[⬅️ Back to main README](../README.md)
