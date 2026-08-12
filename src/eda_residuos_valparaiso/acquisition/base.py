from __future__ import annotations

from pathlib import Path

from ..schemas import SourceRecord


def actionable_missing_source(source: SourceRecord) -> str:
    return (
        f"Falta '{source.dataset_id}'. Método: {source.acquisition_method}. "
        f"Coloque el archivo en '{source.local_path}'. Fuente: {source.source_url or 'pendiente'}"
    )


def local_source_exists(source: SourceRecord, root: Path = Path(".")) -> bool:
    return (root / source.local_path).exists()
