from __future__ import annotations

from pathlib import Path

from .base import actionable_missing_source
from ..schemas import SourceRecord


def require_census_source(source: SourceRecord, root: Path = Path(".")) -> Path:
    path = root / source.local_path
    if not path.exists():
        raise FileNotFoundError(actionable_missing_source(source))
    return path
