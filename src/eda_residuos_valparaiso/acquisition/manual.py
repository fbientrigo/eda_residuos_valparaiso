from __future__ import annotations

from ..schemas import SourceRecord


def manual_instructions(source: SourceRecord) -> str:
    return (
        f"[{source.dataset_id}] {source.title}\n"
        f"  Institución: {source.institution}\n"
        f"  Fuente: {source.source_url or 'sin URL primaria registrada'}\n"
        f"  Guardar en: {source.local_path}\n"
        f"  Formato esperado: {source.expected_format}\n"
    )
