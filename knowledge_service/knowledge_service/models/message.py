"""Defines the data model for a message in the knowledge service."""

from pydantic import BaseModel


class MessageDTO(BaseModel):
    """
    Represents a message in the conversation.

    Attributes:
        content (str): The content of the message.
        timestamp (str): The timestamp when the message was created.

    """

    content: str
    timestamp: str
