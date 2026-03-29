from pathlib import Path
from typing import cast

import pytest
from knowledge_service.loaders.obsidian_loader import ObsidianLoader
from knowledge_service.utils.settings import Settings, SettingsSource
from pytest_mock import MockerFixture


@pytest.fixture
def vault(tmp_path: Path) -> SettingsSource:
    return SettingsSource(id="vault-1", location=str(tmp_path), description="Test vault")


@pytest.fixture
def settings(mocker: MockerFixture, vault: SettingsSource) -> Settings:
    mock_settings = mocker.MagicMock(spec=Settings)
    mock_settings.obsidian_sources = [vault]
    return cast(Settings, mock_settings)


@pytest.fixture
def loader(settings: Settings) -> ObsidianLoader:
    return ObsidianLoader(settings)


class TestObsidianLoaderInit:
    def test_initialization(self, mocker: MockerFixture) -> None:
        # given
        mock_settings = mocker.MagicMock(spec=Settings)

        # when
        result = ObsidianLoader(mock_settings)

        # then
        assert result._settings is mock_settings


class TestGetVaultConfig:
    def test_returns_correct_config(self, loader: ObsidianLoader, vault: SettingsSource, tmp_path: Path) -> None:
        # when
        result = loader.get_vault_config("vault-1")

        # then
        assert result.id == vault.id
        assert result.location == str(tmp_path)

    def test_raises_when_vault_not_found(self, loader: ObsidianLoader) -> None:
        # when / then
        with pytest.raises(ValueError, match="unknown-vault"):
            loader.get_vault_config("unknown-vault")


class TestProcessFile:
    def test_markdown(self, loader: ObsidianLoader, tmp_path: Path) -> None:
        # given
        md_file = tmp_path / "note.md"
        md_file.write_text("# Hello\nThis is a note.", encoding="utf-8")

        # when
        document = loader.process_file(md_file)

        # then
        assert document is not None
        assert document.content == "# Hello\nThis is a note."
        assert document.meta["source"] == str(md_file)

    def test_txt(self, loader: ObsidianLoader, tmp_path: Path) -> None:
        # given
        txt_file = tmp_path / "readme.txt"
        txt_file.write_text("Plain text content.", encoding="utf-8")

        # when
        document = loader.process_file(txt_file)

        # then
        assert document is not None
        assert document.content == "Plain text content."
        assert document.meta["source"] == str(txt_file)

    def test_pdf(self, loader: ObsidianLoader, tmp_path: Path, mocker: MockerFixture) -> None:
        # given
        pdf_file = tmp_path / "report.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 fake content")
        mocker.patch("knowledge_service.loaders.obsidian_loader.pymupdf4llm.to_markdown", return_value="## PDF Content")

        # when
        document = loader.process_file(pdf_file)

        # then
        assert document is not None
        assert document.content == "## PDF Content"
        assert document.meta["source"] == str(pdf_file)

    def test_unsupported_extension(self, loader: ObsidianLoader, tmp_path: Path, mocker: MockerFixture) -> None:
        # given
        img_file = tmp_path / "photo.jpg"
        img_file.write_bytes(b"fake image data")
        mock_logger = mocker.patch("knowledge_service.loaders.obsidian_loader.logger")

        # when
        document = loader.process_file(img_file)

        # then
        assert document is None
        mock_logger.warning.assert_called_once()


class TestLoadDocuments:
    def test_yields_all_supported_files(self, loader: ObsidianLoader, tmp_path: Path, mocker: MockerFixture) -> None:
        # given
        (tmp_path / "note.md").write_text("Note content", encoding="utf-8")
        (tmp_path / "readme.txt").write_text("Readme content", encoding="utf-8")
        mocker.patch("knowledge_service.loaders.obsidian_loader.pymupdf4llm.to_markdown", return_value="PDF content")
        (tmp_path / "report.pdf").write_bytes(b"%PDF fake")

        # when
        documents = list(loader.load_documents("vault-1"))

        # then
        assert len(documents) == 3
        sources = {doc.meta["source"] for doc in documents}
        assert str(tmp_path / "note.md") in sources
        assert str(tmp_path / "readme.txt") in sources
        assert str(tmp_path / "report.pdf") in sources

    def test_skips_hidden_files(self, loader: ObsidianLoader, tmp_path: Path) -> None:
        # given
        (tmp_path / "visible.md").write_text("Visible", encoding="utf-8")
        (tmp_path / ".hidden.md").write_text("Hidden", encoding="utf-8")

        # when
        documents = list(loader.load_documents("vault-1"))

        # then
        assert len(documents) == 1
        assert documents[0].meta["source"] == str(tmp_path / "visible.md")

    def test_skips_files_in_hidden_directories(self, loader: ObsidianLoader, tmp_path: Path) -> None:
        # given
        hidden_dir = tmp_path / ".obsidian"
        hidden_dir.mkdir()
        (hidden_dir / "config.md").write_text("Internal config", encoding="utf-8")
        (tmp_path / "note.md").write_text("Real note", encoding="utf-8")

        # when
        documents = list(loader.load_documents("vault-1"))

        # then
        assert len(documents) == 1
        assert documents[0].meta["source"] == str(tmp_path / "note.md")

    def test_skips_unsupported_file_types(self, loader: ObsidianLoader, tmp_path: Path) -> None:
        # given
        (tmp_path / "image.png").write_bytes(b"fake png")
        (tmp_path / "archive.zip").write_bytes(b"fake zip")

        # when
        documents = list(loader.load_documents("vault-1"))

        # then
        assert documents == []
