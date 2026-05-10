# controle-delete-fk-constraint Bugfix Design

## Overview

`DELETE /delete/controle/{id}` crashes with a SQL Server FK integrity error because
`AtletaAvatar` rows reference `historicocontrole.id` via `controle_id`
(constraint `FK__atletaava__contr__2739D489`). The current `ControleRepo.delete_controle()`
issues a direct `DELETE` on `historicocontrole` without first removing the dependent rows.

The fix adds a pre-deletion step that:
1. Fetches all `AtletaAvatar` rows linked to the `controle_id`.
2. Deletes their blobs from the `atleta-controles` Azure Blob Storage container via
   `AzureBlobStorage.delete_imagem()` (missing blobs are logged and skipped).
3. Deletes the `AtletaAvatar` DB rows and the `HistoricoControle` row atomically within
   the same session.

The change is minimal and surgical: only the delete path is touched; list, create, and
all other endpoints are unaffected.

---

## Glossary

- **Bug_Condition (C)**: `EXISTS (SELECT 1 FROM atletaavatar WHERE controle_id = :id)` —
  the `HistoricoControle` being deleted has at least one dependent `AtletaAvatar` row.
- **Property (P)**: After a successful delete, no `AtletaAvatar` rows with
  `controle_id == id` remain in the DB, all their blobs have been removed from Azure
  (or logged as missing), and the `HistoricoControle` row is gone.
- **Preservation**: All behavior for inputs where `¬C(X)` holds — i.e., deletes of
  controles with no linked avatars, 404 responses for non-existent ids, list, and create
  endpoints — must remain byte-for-byte identical to the current implementation.
- **`ControleRepo`**: Class in `src/repository/repo_controle.py` that owns all DB
  operations for `HistoricoControle` and `AtletaAvatar`.
- **`ControleDeleteUseCase`**: Class in `src/use_cases/controle_delete.py` that
  orchestrates the delete flow.
- **`AzureBlobStorage`**: Adapter in `src/main/adapters/azure_blob_storage.py` with
  `delete_imagem(container, blob_name)` for blob deletion.
- **`controle_id`**: The `AtletaAvatar.controle_id` FK column that references
  `historicocontrole.id`.
- **`atleta-controles`**: The Azure Blob Storage container that holds controle blobs.

---

## Bug Details

### Bug Condition

The bug manifests when `DELETE /delete/controle/{id}` is called for a `HistoricoControle`
record that has one or more `AtletaAvatar` rows with `controle_id == id`.
`ControleRepo.delete_controle()` executes `DELETE FROM historicocontrole WHERE id = ?`
without first removing the dependent rows, causing SQL Server to raise an FK integrity
error and roll back the transaction.

**Formal Specification:**

```
FUNCTION isBugCondition(controle_id)
  INPUT: controle_id of type int
  OUTPUT: boolean

  RETURN EXISTS (SELECT 1 FROM atletaavatar WHERE controle_id = controle_id)
END FUNCTION
```

### Examples

- **Triggers bug**: `controle_id = 42` has 2 `AtletaAvatar` rows →
  `pyodbc.IntegrityError` is raised, record is NOT deleted.
- **Triggers bug**: `controle_id = 7` has 1 `AtletaAvatar` row with a missing blob in
  Azure → without the fix, still crashes on the DB delete; with the fix, the missing
  blob is logged and the delete completes.
- **Does NOT trigger bug**: `controle_id = 99` has 0 `AtletaAvatar` rows →
  current code deletes successfully; fix must preserve this behavior.
- **Does NOT trigger bug**: `controle_id = 999` does not exist →
  `NoResultFound` is raised; fix must preserve this behavior.

---

## Expected Behavior

### Preservation Requirements

**Unchanged Behaviors:**

- `DELETE /delete/controle/{id}` for a controle with **no** linked `AtletaAvatar` rows
  must continue to delete the `HistoricoControle` row and return `{'id': controle_id}`
  without making any Azure Blob Storage calls.
- `DELETE /delete/controle/{id}` for a non-existent `controle_id` must continue to
  raise `NoResultFound` (surfaced as HTTP 404), leaving DB and Azure unchanged.
- `GET /list/controle/{atleta_id}` must continue to return the paginated list of
  `HistoricoControle` records joined with their `AtletaAvatar` blob URLs, unaffected.
- `POST /create/controle` must continue to create `HistoricoControle` records correctly,
  unaffected.

**Scope:**

All inputs where `isBugCondition(controle_id)` is `false` — including controles with no
avatars, non-existent ids, and all non-delete endpoints — must be completely unaffected
by this fix.

---

## Hypothesized Root Cause

Based on the bug description and code inspection:

1. **Missing dependent-row deletion in `ControleRepo.delete_controle()`**: The method
   calls `session.delete(controle)` directly on the `HistoricoControle` object without
   first deleting `AtletaAvatar` rows that reference it. SQL Server enforces the FK
   constraint `FK__atletaava__contr__2739D489` and rejects the statement.

2. **No cascade configured on the ORM relationship**: `HistoricoControle` has no
   `Relationship` back-reference to `AtletaAvatar` in `model_objects.py`, and
   `AtletaAvatar.controle_id` is defined without `ondelete="CASCADE"`, so SQLModel/
   SQLAlchemy does not automatically handle the child rows.

3. **No blob cleanup in the use case**: `ControleDeleteUseCase` has no reference to
   `AzureBlobStorage`, so even if the DB issue were resolved (e.g., by adding a DB
   cascade), orphaned blobs would remain in the `atleta-controles` container.

---

## Correctness Properties

Property 1: Bug Condition - FK-safe deletion with blob cleanup

_For any_ `controle_id` where `isBugCondition(controle_id)` is `true` (i.e., at least
one `AtletaAvatar` row references it), the fixed `ControleDeleteUseCase.execute()` SHALL:
- delete each linked blob from the `atleta-controles` container (logging and continuing
  on `ResourceNotFoundError`),
- delete all `AtletaAvatar` rows with `controle_id == id` within the same DB session,
- delete the `HistoricoControle` row in the same DB session commit,
- return `{'id': controle_id}` without raising an integrity error.

**Validates: Requirements 2.1, 2.2, 2.3**

Property 2: Preservation - No-avatar and non-existent controle behavior unchanged

_For any_ `controle_id` where `isBugCondition(controle_id)` is `false` (no linked
`AtletaAvatar` rows, or the id does not exist), the fixed `ControleDeleteUseCase.execute()`
SHALL produce exactly the same result as the original implementation — deleting the
`HistoricoControle` row and returning `{'id': controle_id}` when the record exists, or
raising `NoResultFound` when it does not — without making any Azure Blob Storage calls.

**Validates: Requirements 3.1, 3.2**

---

## Fix Implementation

### Changes Required

#### File: `src/repository/repo_controle.py`

**New method — `get_avatars_by_controle_id`**

Add a method that returns all `AtletaAvatar` rows linked to a given `controle_id`.
This is called by the use case before deletion so it can collect blob URLs.

```python
def get_avatars_by_controle_id(self, controle_id: int) -> list[AtletaAvatar]:
    with self.session_factory() as session:
        query = select(AtletaAvatar).where(
            AtletaAvatar.controle_id == controle_id
        )
        return list(session.exec(query).all())
```

**Modified method — `delete_controle`**

Extend the existing session to also delete all linked `AtletaAvatar` rows before
deleting the `HistoricoControle` row, keeping both deletions in a single `commit()`.

```python
def delete_controle(self, controle_id: int):
    with self.session_factory() as session:
        controle: HistoricoControle = session.exec(
            select(HistoricoControle).where(
                HistoricoControle.id == controle_id
            )
        ).one()  # raises NoResultFound if not found — preserved behavior

        # Delete dependent AtletaAvatar rows first to satisfy FK constraint
        avatars = session.exec(
            select(AtletaAvatar).where(
                AtletaAvatar.controle_id == controle_id
            )
        ).all()
        for avatar in avatars:
            session.delete(avatar)

        session.delete(controle)
        session.commit()

        return {'id': controle.id}
```

> **Note:** `get_avatars_by_controle_id` is called by the use case *before* this method
> to collect blob URLs for Azure deletion. The repo method re-queries inside its own
> session to keep the session scope clean.

---

#### File: `src/use_cases/controle_delete.py`

**Inject `AzureBlobStorage` and add blob deletion logic**, following the same pattern
as `DeleteFilesUseCase` in `src/use_cases/files_delete.py`.

```python
import logging

from azure.core.exceptions import ResourceNotFoundError

from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_controle import ControleRepo

logger = logging.getLogger(__name__)


class ControleDeleteUseCase:

    CONTAINER_NAME = 'atleta-controles'

    def __init__(
        self,
        controle_repository: ControleRepo,
        storage_service: AzureBlobStorage,
    ):
        self.controle_repository = controle_repository
        self.storage_service = storage_service

    def execute(self, http_request: HttpRequest):
        controle_id: int = http_request.path_params.get('id')
        return self._delete_controle(controle_id)

    def _delete_controle(self, controle_id: int):
        # 1. Fetch linked avatars (blob URLs) before any deletion
        avatars = self.controle_repository.get_avatars_by_controle_id(controle_id)

        # 2. Delete blobs from Azure (missing blobs are logged, not fatal)
        for avatar in avatars:
            self._delete_blob(avatar.blob_url)

        # 3. Delete AtletaAvatar DB rows + HistoricoControle atomically
        return self.controle_repository.delete_controle(controle_id)

    def _delete_blob(self, blob_url: str) -> None:
        blob_name = self._extrair_blob_path_name(self.CONTAINER_NAME, blob_url)
        try:
            self.storage_service.delete_imagem(self.CONTAINER_NAME, blob_name)
        except ResourceNotFoundError:
            logger.warning(
                'Blob not found in Azure, skipping: container=%s blob=%s',
                self.CONTAINER_NAME,
                blob_name,
            )

    def _extrair_blob_path_name(self, container: str, blob_url: str) -> str:
        parts = blob_url.split(container)
        result = parts[1] if len(parts) > 1 else ''
        return result[1:]  # strip leading slash
```

---

#### File: `src/main/composers/controle_delete_composer.py`

**Inject `AzureBlobStorage` into the use case.**

```python
from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.controllers.controle_delete_controler import (
    ControleDeleteController,
)
from src.repository.repo_controle import ControleRepo
from src.use_cases.controle_delete import ControleDeleteUseCase


def controle_delete_composer():
    controle_repository = ControleRepo()
    storage_service = AzureBlobStorage()

    use_case = ControleDeleteUseCase(
        controle_repository=controle_repository,
        storage_service=storage_service,
    )
    controller = ControleDeleteController(use_case=use_case)

    return controller.handle
```

---

## Testing Strategy

### Validation Approach

The testing strategy follows a two-phase approach: first, surface counterexamples that
demonstrate the bug on unfixed code, then verify the fix works correctly and preserves
existing behavior.

### Exploratory Bug Condition Checking

**Goal**: Surface counterexamples that demonstrate the bug BEFORE implementing the fix.
Confirm or refute the root cause analysis. If we refute, we will need to re-hypothesize.

**Test Plan**: Write unit tests that call `ControleRepo.delete_controle()` (or the full
use case) with a `controle_id` that has linked `AtletaAvatar` rows in the DB (or via
mocks), and assert that the operation completes without raising an integrity error. Run
these tests on the UNFIXED code to observe the `IntegrityError` and confirm the root cause.

**Test Cases**:

1. **Single avatar linked**: Call `delete_controle(controle_id)` where one `AtletaAvatar`
   row exists with `controle_id == id` → will raise `IntegrityError` on unfixed code.
2. **Multiple avatars linked**: Call `delete_controle(controle_id)` where two or more
   `AtletaAvatar` rows exist → will raise `IntegrityError` on unfixed code.
3. **Avatar with missing blob**: Call use case with a `controle_id` whose avatar has a
   `blob_url` that does not exist in Azure → should log and continue on fixed code; on
   unfixed code, crashes before even reaching Azure.
4. **Avatar with valid blob**: Call use case with a `controle_id` whose avatar has a
   valid `blob_url` → blob deletion is called; DB delete completes on fixed code.

**Expected Counterexamples**:

- `pyodbc.IntegrityError` with message referencing `FK__atletaava__contr__2739D489`
  when `delete_controle` is called with a `controle_id` that has linked `AtletaAvatar`
  rows.

### Fix Checking

**Goal**: Verify that for all inputs where the bug condition holds, the fixed function
produces the expected behavior.

**Pseudocode:**

```
FOR ALL controle_id WHERE isBugCondition(controle_id) DO
  avatars ← get_avatars_by_controle_id(controle_id)
  result  ← ControleDeleteUseCase_fixed.execute(controle_id)
  ASSERT result = {'id': controle_id}
  ASSERT no IntegrityError raised
  FOR EACH avatar IN avatars DO
    ASSERT blob_deleted_from_azure(avatar.blob_url)
           OR blob_not_found_logged(avatar.blob_url)
  END FOR
  ASSERT NOT EXISTS (SELECT 1 FROM atletaavatar WHERE controle_id = controle_id)
  ASSERT NOT EXISTS (SELECT 1 FROM historicocontrole WHERE id = controle_id)
END FOR
```

### Preservation Checking

**Goal**: Verify that for all inputs where the bug condition does NOT hold, the fixed
function produces the same result as the original function.

**Pseudocode:**

```
FOR ALL controle_id WHERE NOT isBugCondition(controle_id) DO
  ASSERT delete_controle_original(controle_id) = delete_controle_fixed(controle_id)
END FOR
```

**Testing Approach**: Property-based testing is recommended for preservation checking
because:
- It generates many test cases automatically across the input domain.
- It catches edge cases that manual unit tests might miss.
- It provides strong guarantees that behavior is unchanged for all non-buggy inputs.

**Test Plan**: Observe behavior on UNFIXED code first for controles with no linked
avatars and for non-existent ids, then write property-based tests capturing that behavior.

**Test Cases**:

1. **No-avatar preservation**: `delete_controle(controle_id)` where no `AtletaAvatar`
   rows exist → must return `{'id': controle_id}` and make zero Azure calls, both before
   and after the fix.
2. **Not-found preservation**: `delete_controle(controle_id)` for a non-existent id →
   must raise `NoResultFound` both before and after the fix.
3. **List endpoint preservation**: `GET /list/controle/{atleta_id}` must return the same
   paginated results before and after the fix.
4. **Create endpoint preservation**: `POST /create/controle` must create records
   correctly before and after the fix.

### Unit Tests

- Test `get_avatars_by_controle_id` returns the correct `AtletaAvatar` list for a given
  `controle_id` (including empty list when none exist).
- Test `delete_controle` (fixed) deletes `AtletaAvatar` rows and `HistoricoControle` in
  a single commit when avatars are present.
- Test `delete_controle` (fixed) still raises `NoResultFound` for a non-existent id.
- Test `ControleDeleteUseCase._delete_blob` calls `storage_service.delete_imagem` with
  the correct container and blob name.
- Test `ControleDeleteUseCase._delete_blob` catches `ResourceNotFoundError`, logs a
  warning, and does not re-raise.
- Test `ControleDeleteUseCase._extrair_blob_path_name` correctly strips the container
  prefix and leading slash from a blob URL.

### Property-Based Tests

- Generate random lists of `AtletaAvatar` blob URLs for a `controle_id` and verify that
  after the fixed delete: all blobs were attempted for deletion and all DB rows are gone.
- Generate random `controle_id` values with no linked avatars and verify the fixed use
  case produces the same result as the original (preservation property).
- Generate random blob URLs (including malformed ones) and verify
  `_extrair_blob_path_name` always returns a string without a leading slash.

### Integration Tests

- End-to-end: create a `HistoricoControle` + linked `AtletaAvatar` rows with real (or
  mocked) Azure blobs, call `DELETE /delete/controle/{id}`, assert HTTP 200, assert DB
  rows are gone, assert blobs were deleted.
- End-to-end: create a `HistoricoControle` with no linked avatars, call
  `DELETE /delete/controle/{id}`, assert HTTP 200 and no Azure calls made.
- End-to-end: call `DELETE /delete/controle/{id}` for a non-existent id, assert HTTP 404.
