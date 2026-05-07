"""
Implements:
- SwR-007
- SwR-008

Design:
- DDS-007
- DDS-008
"""
from __future__ import annotations

from pathlib import Path

import yaml


def persist_run_metadata(
    *,
    output_dir: str | Path,
    software_version: str,
    configuration_version: str,
    input_data_references: list[str],
) -> Path:
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = target_dir / 'run_metadata.yaml'
    payload = {
        'software_version': software_version,
        'configuration_version': configuration_version,
        'input_data_references': input_data_references,
    }
    metadata_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding='utf-8')
    return metadata_path


def generate_run_report(*, output_dir: str | Path, metadata_path: str | Path) -> Path:
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    metadata_file = Path(metadata_path)
    metadata = yaml.safe_load(metadata_file.read_text(encoding='utf-8'))
    report_path = target_dir / 'run_report.txt'
    lines = [
        'run_report',
        f"software_version: {metadata['software_version']}",
        f"configuration_version: {metadata['configuration_version']}",
        'input_data_references:',
    ]
    for item in metadata['input_data_references']:
        lines.append(f'- {item}')
    report_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return report_path
