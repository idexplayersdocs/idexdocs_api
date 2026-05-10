# Implementation Plan

- [x] 1. Write bug condition exploration test
  - **Property 1: Bug Condition** - FK Integrity Error on Delete with Linked Avatars
  - **CRITICAL**: This test MUST FAIL on unfixed code - failure confirms the bug exists
  - **DO NOT attempt to fix the test or the code when it fails**
  - **NOTE**: This test encodes the expected behavior - it will validate the fix when it passes after implementation
  - **GOAL**: Surface counterexamples that demonstrate the bug exists
  - **Scoped PBT Approach**: Scope the property to concrete failing cases: `controle_id` with 1+ linked `AtletaAvatar` rows
  - Install `hypothesis` if not present (`pip install hypothesis` and add to `requirements/test.txt`)
  - Create test file `tests/test_controle_delete_bug_condition.py`
  - Mock `ControleRepo` session to simulate `AtletaAvatar` rows referencing `controle_id`
  - Use `hypothesis` to generate random lists of `AtletaAvatar` (1 to N items with random `blob_url` strings) for a given `controle_id`
  - Assert that `ControleDeleteUseCase.execute()` completes without raising `IntegrityError`
  - Assert result equals `{'id': controle_id}`
  - Assert `AzureBlobStorage.delete_imagem()` was called for each avatar's blob
  - Assert no `AtletaAvatar` rows remain for the `controle_id` after deletion
  - Run test on UNFIXED code
  - **EXPECTED OUTCOME**: Test FAILS (this is correct - it proves the bug exists because the current code has no `storage_service` parameter and does not delete dependent rows)
  - Document counterexamples found (e.g., "ControleDeleteUseCase.__init__() got unexpected keyword argument 'storage_service'" or "IntegrityError on FK constraint")
  - Mark task complete when test is written, run, and failure is documented
  - _Requirements: 1.1, 1.2_

- [x] 2. Write preservation property tests (BEFORE implementing fix)
  - **Property 2: Preservation** - No-Avatar and Non-Existent Controle Behavior Unchanged
  - **IMPORTANT**: Follow observation-first methodology
  - Create test file `tests/test_controle_delete_preservation.py`
  - Observe: calling `ControleRepo.delete_controle(controle_id)` where no `AtletaAvatar` rows exist returns `{'id': controle_id}` on unfixed code
  - Observe: calling `ControleRepo.delete_controle(non_existent_id)` raises `NoResultFound` on unfixed code
  - Write property-based test with `hypothesis`: for all `controle_id` values with no linked `AtletaAvatar` rows, `delete_controle(controle_id)` returns `{'id': controle_id}` and makes zero Azure Blob Storage calls
  - Write property-based test: for all non-existent `controle_id` values, `delete_controle(controle_id)` raises `NoResultFound`
  - Use mocked DB session to simulate the no-avatar scenario (session.exec returns empty list for AtletaAvatar query, returns HistoricoControle for main query)
  - Verify tests pass on UNFIXED code (these scenarios work correctly today)
  - **EXPECTED OUTCOME**: Tests PASS (this confirms baseline behavior to preserve)
  - Mark task complete when tests are written, run, and passing on unfixed code
  - _Requirements: 3.1, 3.2_

- [x] 3. Fix for FK constraint violation on controle delete with linked avatars

  - [x] 3.1 Add `get_avatars_by_controle_id()` method to `ControleRepo`
    - Open `src/repository/repo_controle.py`
    - Add method that queries `AtletaAvatar` rows where `controle_id == id`
    - Returns `list[AtletaAvatar]` (empty list when none exist)
    - _Bug_Condition: isBugCondition(controle_id) = EXISTS(SELECT 1 FROM atletaavatar WHERE controle_id = controle_id)_
    - _Requirements: 2.1, 2.2_

  - [x] 3.2 Modify `delete_controle()` in `ControleRepo` to delete linked `AtletaAvatar` rows
    - Open `src/repository/repo_controle.py`
    - Within the existing session, query all `AtletaAvatar` rows with `controle_id == id`
    - Delete each `AtletaAvatar` row via `session.delete(avatar)` before deleting `HistoricoControle`
    - Keep both deletions in a single `session.commit()` for atomicity
    - Preserve existing `NoResultFound` behavior for non-existent ids
    - _Bug_Condition: isBugCondition(controle_id) = EXISTS(SELECT 1 FROM atletaavatar WHERE controle_id = controle_id)_
    - _Expected_Behavior: Delete AtletaAvatar rows first, then HistoricoControle, commit atomically_
    - _Preservation: NoResultFound still raised for non-existent ids; no-avatar deletes still work identically_
    - _Requirements: 1.1, 1.2, 2.1, 2.2, 3.1, 3.2_

  - [x] 3.3 Refactor `ControleDeleteUseCase` to inject `AzureBlobStorage` and delete blobs
    - Open `src/use_cases/controle_delete.py`
    - Add `AzureBlobStorage` as constructor parameter (`storage_service`)
    - Add `CONTAINER_NAME = 'atleta-controles'` class attribute
    - In `_delete_controle()`: call `get_avatars_by_controle_id(controle_id)` to fetch avatar list
    - For each avatar, extract blob name using `_extrair_blob_path_name(container, blob_url)` (split on container name, take right part, strip leading slash)
    - Call `storage_service.delete_imagem(container, blob_name)` wrapped in try/except `ResourceNotFoundError` (log warning and continue)
    - Then call `self.controle_repository.delete_controle(controle_id)` for atomic DB deletion
    - Add `_delete_blob()` and `_extrair_blob_path_name()` helper methods following `files_delete.py` pattern
    - _Bug_Condition: isBugCondition(controle_id) = EXISTS(SELECT 1 FROM atletaavatar WHERE controle_id = controle_id)_
    - _Expected_Behavior: Blobs deleted from Azure (ResourceNotFoundError caught and logged), then DB rows deleted atomically_
    - _Preservation: When no avatars exist, no Azure calls are made; delete proceeds as before_
    - _Requirements: 2.1, 2.2, 2.3, 3.1_

  - [x] 3.4 Update `controle_delete_composer.py` to inject `AzureBlobStorage`
    - Open `src/main/composers/controle_delete_composer.py`
    - Import `AzureBlobStorage` from `src.main.adapters.azure_blob_storage`
    - Instantiate `AzureBlobStorage()` and pass as `storage_service` to `ControleDeleteUseCase`
    - _Requirements: 2.1, 2.2_

  - [x] 3.5 Verify bug condition exploration test now passes
    - **Property 1: Expected Behavior** - FK-Safe Deletion with Blob Cleanup
    - **IMPORTANT**: Re-run the SAME test from task 1 - do NOT write a new test
    - The test from task 1 encodes the expected behavior (no IntegrityError, blobs deleted, result = {'id': controle_id})
    - When this test passes, it confirms the expected behavior is satisfied
    - Run bug condition exploration test from step 1
    - **EXPECTED OUTCOME**: Test PASSES (confirms bug is fixed)
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 3.6 Verify preservation tests still pass
    - **Property 2: Preservation** - No-Avatar and Non-Existent Controle Behavior Unchanged
    - **IMPORTANT**: Re-run the SAME tests from task 2 - do NOT write new tests
    - Run preservation property tests from step 2
    - **EXPECTED OUTCOME**: Tests PASS (confirms no regressions)
    - Confirm all tests still pass after fix (no regressions)

- [x] 4. Checkpoint - Ensure all tests pass
  - Run full test suite: `pytest -s -x --cov=src -vv`
  - Ensure all property-based tests (bug condition + preservation) pass
  - Ensure no other existing tests are broken by the changes
  - Ask the user if questions arise
