# Bugfix Requirements Document

## Introduction

Deleting a `HistoricoControle` record via `DELETE /delete/controle/{id}` fails with a SQL Server foreign key integrity error. The `AtletaAvatar` table has a `controle_id` column that references `historicocontrole.id` via the constraint `FK__atletaava__contr__2739D489`. Because `ControleRepo.delete_controle()` issues a direct `DELETE` on `historicocontrole` without first removing the dependent `AtletaAvatar` rows, SQL Server rejects the operation. The fix deletes all linked `AtletaAvatar` rows (and their corresponding blobs from the `atleta-controles` Azure Blob Storage container) before deleting the `HistoricoControle` row.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN a `DELETE /delete/controle/{id}` request is made for a `HistoricoControle` record that has one or more linked `AtletaAvatar` rows (`AtletaAvatar.controle_id == id`) THEN the system raises `pyodbc.IntegrityError` (SQLSTATE 23000) with the message "The DELETE statement conflicted with the REFERENCE constraint FK__atletaava__contr__2739D489" and the record is not deleted.

1.2 WHEN `ControleRepo.delete_controle()` is called with a `controle_id` that has associated `AtletaAvatar` rows THEN the system executes `DELETE FROM historicocontrole WHERE id = ?` without first removing the dependent rows, causing the database to reject the statement.

### Expected Behavior (Correct)

2.1 WHEN a `DELETE /delete/controle/{id}` request is made for a `HistoricoControle` record that has one or more linked `AtletaAvatar` rows THEN the system SHALL delete the corresponding blobs from the `atleta-controles` Azure Blob Storage container, delete all `AtletaAvatar` rows where `controle_id == id`, and then delete the `HistoricoControle` row, completing the operation successfully without raising an integrity error.

2.2 WHEN `ControleDeleteUseCase` is called with a `controle_id` that has associated `AtletaAvatar` rows THEN the system SHALL first call `AzureBlobStorage.delete_imagem()` for each linked blob URL, then remove the dependent `AtletaAvatar` rows within the same database session, and then delete the `HistoricoControle` row, committing both DB deletions atomically.

2.3 WHEN an `AtletaAvatar` row linked to the `controle_id` has a `blob_url` that does not exist in Azure Blob Storage THEN the system SHALL log the missing blob and continue deleting the remaining blobs and the database rows, without aborting the operation.

### Unchanged Behavior (Regression Prevention)

3.1 WHEN a `DELETE /delete/controle/{id}` request is made for a `HistoricoControle` record that has no linked `AtletaAvatar` rows THEN the system SHALL CONTINUE TO delete the `HistoricoControle` row successfully and return the deleted record's `id`, without making any Azure Blob Storage calls.

3.2 WHEN `ControleRepo.delete_controle()` is called with a `controle_id` that does not exist in the database THEN the system SHALL CONTINUE TO raise `NoResultFound` (or the equivalent HTTP 404 response), leaving the database and Azure Blob Storage unchanged.

3.3 WHEN `GET /list/controle/{atleta_id}` is called THEN the system SHALL CONTINUE TO return the paginated list of `HistoricoControle` records joined with their associated `AtletaAvatar` blob URLs, unaffected by the delete fix.

3.4 WHEN `POST /create/controle` is called THEN the system SHALL CONTINUE TO create a new `HistoricoControle` record correctly, unaffected by the delete fix.

---

## Bug Condition Pseudocode

**Bug Condition Function** — identifies inputs that trigger the bug:

```pascal
FUNCTION isBugCondition(controle_id)
  INPUT: controle_id of type int
  OUTPUT: boolean

  // Returns true when at least one AtletaAvatar row references this controle_id
  RETURN EXISTS (SELECT 1 FROM atletaavatar WHERE controle_id = controle_id)
END FUNCTION
```

**Property: Fix Checking** — correct behavior for buggy inputs:

```pascal
// Property: Fix Checking — Blobs deleted from Azure, then dependent AtletaAvatar rows removed, then HistoricoControle deleted
FOR ALL controle_id WHERE isBugCondition(controle_id) DO
  avatars ← SELECT blob_url FROM atletaavatar WHERE controle_id = controle_id
  result ← delete_controle'(controle_id)
  ASSERT no_integrity_error(result)
  ASSERT result = {'id': controle_id}
  FOR EACH blob_url IN avatars DO
    ASSERT blob_deleted_from_azure(blob_url) OR blob_not_found_in_azure(blob_url)
  END FOR
  ASSERT NOT EXISTS (SELECT 1 FROM atletaavatar WHERE controle_id = controle_id)
  ASSERT NOT EXISTS (SELECT 1 FROM historicocontrole WHERE id = controle_id)
END FOR
```

**Property: Preservation Checking** — non-buggy inputs are unaffected:

```pascal
// Property: Preservation Checking
FOR ALL controle_id WHERE NOT isBugCondition(controle_id) DO
  ASSERT delete_controle(controle_id) = delete_controle'(controle_id)
END FOR
```
