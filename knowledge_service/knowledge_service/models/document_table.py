"""DTOs and models related to document tables in the knowledge service."""

from pydantic import BaseModel


class DocumentTableDTO(BaseModel):
    """
    DTO representing a document table and its associated metadata.

    Attributes:
        source: The name of the document table.
        document_count: The total number of documents in the table.

    """

    source: str
    document_count: int


class CreateTableRequestDTO(BaseModel):
    """
    DTO for creating a new document table.

    Attributes:
        table_name: The name of the table to create.

    """

    table_name: str


class FileUploadResponseDTO(BaseModel):
    """
    DTO for the response after uploading and ingesting a file.

    Attributes:
        table_name: The table the file was ingested into.
        file_name: The original name of the uploaded file.
        chunks_created: The number of document chunks created.
        message: A human-readable status message.

    """

    table_name: str
    file_name: str
    chunks_created: int
    message: str
