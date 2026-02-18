"""Initializes the knowledge service application."""

from knowledge_service.loaders.obsidian_loader import ObsidianLoader
from knowledge_service.logger import setup_logger
from knowledge_service.services.ai_service import AIService
from knowledge_service.settings import Settings

# Initialize settings and logger
settings = Settings()
setup_logger(settings)

# Initialize services
ai_service = AIService(settings)

# Initialize loaders
obsidian_loader = ObsidianLoader(settings)
