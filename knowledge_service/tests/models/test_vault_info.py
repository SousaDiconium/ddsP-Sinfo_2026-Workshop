import pytest
from knowledge_service.models.vault_info import VaultInfoDTO
from pydantic import ValidationError


class TestVaultInfoDTO:
    def test_instantiation(self) -> None:
        # given / when
        dto = VaultInfoDTO(id="vault-1", location="/path/to/vault", description="My personal vault")

        # then
        assert dto.id == "vault-1"
        assert dto.location == "/path/to/vault"
        assert dto.description == "My personal vault"

    def test_missing_description_raises(self) -> None:
        # when / then
        with pytest.raises(ValidationError):
            VaultInfoDTO(id="vault-1", location="/path")  # type: ignore[call-arg]  # missing description

    def test_missing_id_raises(self) -> None:
        # when / then
        with pytest.raises(ValidationError):
            VaultInfoDTO(location="/path", description="desc")  # type: ignore[call-arg]  # missing id
