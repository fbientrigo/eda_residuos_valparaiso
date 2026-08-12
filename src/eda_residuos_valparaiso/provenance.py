from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from .schemas import SourceRecord


def load_source_registry(path: Path) -> list[SourceRecord]:
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    return [SourceRecord.model_validate(item) for item in raw.get("sources", [])]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolved_manifest(records: list[SourceRecord], root: Path = Path(".")) -> pd.DataFrame:
    now = datetime.now(timezone.utc).isoformat()
    rows: list[dict[str, object]] = []
    for record in records:
        local = root / record.local_path
        is_file = local.is_file()
        exists = local.exists()
        rows.append(
            {
                **record.model_dump(),
                "acquired_at": now if exists else "",
                "checksum": sha256_file(local) if is_file else "",
                "processing_status": "available" if exists else "missing",
            }
        )
    return pd.DataFrame(rows)
