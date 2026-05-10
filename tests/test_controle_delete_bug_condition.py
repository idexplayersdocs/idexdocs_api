"""
Bug Condition Exploration Test - FK Integrity Error on Delete with Linked Avatars

**Validates: Requirements 1.1, 1.2**

This test encodes the EXPECTED behavior after the fix is applied:
- ControleDeleteUseCase accepts a `storage_service` parameter
- When a controle_id has linked AtletaAvatar rows, the use case deletes
  the blobs from Azure and removes the dependent rows before deleting
  the HistoricoControle record
- The operation completes without raising IntegrityError

On UNFIXED code, this test is EXPECTED TO FAIL because:
- ControleDeleteUseCase.__init__() does not accept `storage_service`
- The current code does not delete dependent AtletaAvatar rows
"""

import sys
from unittest.mock import MagicMock, patch

# Patch environment variables and modules before importing source code
# that triggers DB connection at import time
_env_patch = patch.dict(
    'os.environ',
    {
        'MSSQL_USER': 'test',
        'MSSQL_SA_PASSWORD': 'test',
        'MSSQL_HOSTNAME': 'localhost',
        'APPLICATION_DB': 'testdb',
        'STORAGE_ACCOUNT': 'https://fake.blob.core.windows.net',
        'TOKEN_KEY': 'test-secret-key',
    },
)
_env_patch.start()

# Mock the pyodbc and sqlmodel engine creation to avoid real DB connections
_mock_create_engine = patch('sqlmodel.create_engine', return_value=MagicMock())
_mock_create_engine.start()

_mock_metadata = patch('sqlmodel.SQLModel.metadata.create_all')
_mock_metadata.start()

# Pre-register src.main as a mock module to prevent circular import
# (src.main.__init__ imports routes which import composers which import the use case)
import src.main.adapters.azure_blob_storage  # noqa: E402 - this module is safe to import directly

sys.modules.setdefault('src.main', MagicMock())

from hypothesis import given, settings  # noqa: E402
from hypothesis import strategies as st  # noqa: E402

from src.presentation.http_types.http_request import HttpRequest  # noqa: E402
from src.use_cases.controle_delete import ControleDeleteUseCase  # noqa: E402


# Strategy: generate a list of 1+ AtletaAvatar-like objects with random blob_urls
avatar_strategy = st.lists(
    st.fixed_dictionaries(
        {
            'id': st.integers(min_value=1, max_value=10000),
            'blob_url': st.text(
                alphabet=st.characters(whitelist_categories=('L', 'N', 'P')),
                min_size=10,
                max_size=100,
            ).map(
                lambda s: f'https://storage.blob.core.windows.net/atleta-controles/{s}'
            ),
            'controle_id': st.just(None),  # will be set per test
        }
    ),
    min_size=1,
    max_size=5,
)


def _make_avatar_mock(avatar_dict, controle_id):
    """Create a mock AtletaAvatar object from a dict."""
    avatar = MagicMock()
    avatar.id = avatar_dict['id']
    avatar.blob_url = avatar_dict['blob_url']
    avatar.controle_id = controle_id
    return avatar


@given(
    controle_id=st.integers(min_value=1, max_value=10000),
    avatar_dicts=avatar_strategy,
)
@settings(max_examples=50, deadline=None)
def test_delete_controle_with_linked_avatars_completes_without_integrity_error(
    controle_id, avatar_dicts
):
    """
    Property 1: Bug Condition - FK Integrity Error on Delete with Linked Avatars

    For any controle_id with 1+ linked AtletaAvatar rows, the fixed
    ControleDeleteUseCase.execute() SHALL:
    - Complete without raising IntegrityError
    - Return {'id': controle_id}
    - Call AzureBlobStorage.delete_imagem() for each avatar's blob
    - Leave no AtletaAvatar rows for the controle_id after deletion

    **Validates: Requirements 1.1, 1.2**
    """
    # Arrange: create mock avatars linked to this controle_id
    avatars = [_make_avatar_mock(d, controle_id) for d in avatar_dicts]

    # Mock the repository
    mock_repo = MagicMock()
    mock_repo.get_avatars_by_controle_id.return_value = avatars
    mock_repo.delete_controle.return_value = {'id': controle_id}

    # Mock the storage service
    mock_storage = MagicMock()

    # Act: instantiate the use case with storage_service (expected behavior)
    # On UNFIXED code, this will raise TypeError because __init__ does not
    # accept storage_service parameter
    use_case = ControleDeleteUseCase(
        controle_repository=mock_repo,
        storage_service=mock_storage,
    )

    http_request = HttpRequest(path_params={'id': controle_id})
    result = use_case.execute(http_request)

    # Assert: operation completes without IntegrityError
    assert result == {'id': controle_id}

    # Assert: delete_imagem was called for each avatar's blob
    assert mock_storage.delete_imagem.call_count == len(avatars)
    for avatar in avatars:
        blob_name = avatar.blob_url.split('atleta-controles/')[1]
        mock_storage.delete_imagem.assert_any_call(
            'atleta-controles', blob_name
        )

    # Assert: the repo's delete_controle was called (which handles DB row deletion)
    mock_repo.delete_controle.assert_called_once_with(controle_id)

    # Assert: get_avatars_by_controle_id was called to fetch linked avatars
    mock_repo.get_avatars_by_controle_id.assert_called_once_with(controle_id)
