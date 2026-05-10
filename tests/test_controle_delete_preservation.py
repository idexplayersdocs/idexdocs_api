"""
Preservation Property Tests - No-Avatar and Non-Existent Controle Behavior Unchanged

**Validates: Requirements 3.1, 3.2**

These tests verify that the CURRENT behavior is preserved after the fix:
- Deleting a controle with NO linked AtletaAvatar rows returns {'id': controle_id}
  and makes zero Azure Blob Storage calls.
- Deleting a non-existent controle_id raises NoResultFound.

These tests confirm baseline behavior that must be preserved after the fix is applied.
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
from sqlalchemy.orm.exc import NoResultFound  # noqa: E402

from src.presentation.http_types.http_request import HttpRequest  # noqa: E402
from src.use_cases.controle_delete import ControleDeleteUseCase  # noqa: E402


@given(
    controle_id=st.integers(min_value=1, max_value=10000),
)
@settings(max_examples=50, deadline=None)
def test_delete_controle_no_linked_avatars_returns_id(controle_id):
    """
    Property 2a: Preservation - No-Avatar Controle Deletion

    For any controle_id with NO linked AtletaAvatar rows,
    delete_controle(controle_id) returns {'id': controle_id}
    and makes zero Azure Blob Storage calls.

    **Validates: Requirements 3.1**
    """
    # Arrange: mock the repository to simulate a controle with no linked avatars
    mock_repo = MagicMock()
    mock_repo.get_avatars_by_controle_id.return_value = []  # no linked avatars
    mock_repo.delete_controle.return_value = {'id': controle_id}

    # Mock storage service
    mock_storage = MagicMock()

    use_case = ControleDeleteUseCase(
        controle_repository=mock_repo,
        storage_service=mock_storage,
    )

    http_request = HttpRequest(path_params={'id': controle_id})

    # Act
    result = use_case.execute(http_request)

    # Assert: returns {'id': controle_id}
    assert result == {'id': controle_id}

    # Assert: the repository's delete_controle was called with the correct id
    mock_repo.delete_controle.assert_called_once_with(controle_id)

    # Assert: no Azure Blob Storage calls were made (no avatars to delete)
    assert mock_storage.delete_imagem.call_count == 0


@given(
    controle_id=st.integers(min_value=1, max_value=10000),
)
@settings(max_examples=50, deadline=None)
def test_delete_controle_non_existent_raises_no_result_found(controle_id):
    """
    Property 2b: Preservation - Non-Existent Controle Raises NoResultFound

    For any non-existent controle_id, delete_controle(controle_id)
    raises NoResultFound, leaving the database and Azure Blob Storage unchanged.

    **Validates: Requirements 3.2**
    """
    # Arrange: mock the repository to raise NoResultFound (simulating non-existent id)
    mock_repo = MagicMock()
    mock_repo.get_avatars_by_controle_id.return_value = []  # no avatars found
    mock_repo.delete_controle.side_effect = NoResultFound(
        f'No row was found for controle_id={controle_id}'
    )

    # Mock storage service
    mock_storage = MagicMock()

    use_case = ControleDeleteUseCase(
        controle_repository=mock_repo,
        storage_service=mock_storage,
    )

    http_request = HttpRequest(path_params={'id': controle_id})

    # Act & Assert: NoResultFound is raised
    try:
        use_case.execute(http_request)
        assert False, 'Expected NoResultFound to be raised'
    except NoResultFound:
        pass  # Expected behavior

    # Assert: the repository's delete_controle was called with the correct id
    mock_repo.delete_controle.assert_called_once_with(controle_id)

    # Assert: no Azure Blob Storage calls were made
    assert mock_storage.delete_imagem.call_count == 0
