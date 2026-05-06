from __future__ import annotations

from pathlib import Path

from src.workflow_demo.config_loader import load_run_configuration
from src.workflow_demo.run_workflow import generate_run_report, persist_run_metadata


def test_load_run_configuration_from_explicit_yaml_path(tmp_path: Path) -> None:
    config_path = tmp_path / 'run_config.yaml'
    config_path.write_text(
        'run_name: demo-run\n'
        'config_version: v1\n'
        'input_data_references:\n'
        '  - input-a.csv\n',
        encoding='utf-8',
    )

    config = load_run_configuration(config_path)

    assert config['run_name'] == 'demo-run'
    assert config['config_version'] == 'v1'
    assert config['input_data_references'] == ['input-a.csv']


def test_persist_run_metadata_writes_required_fields(tmp_path: Path) -> None:
    output_dir = tmp_path / 'output'
    output_dir.mkdir()

    metadata_path = persist_run_metadata(
        output_dir=output_dir,
        software_version='0.1.0',
        configuration_version='v1',
        input_data_references=['input-a.csv', 'input-b.csv'],
    )

    assert metadata_path.exists()
    content = metadata_path.read_text(encoding='utf-8')
    assert 'software_version: 0.1.0' in content
    assert 'configuration_version: v1' in content
    assert '- input-a.csv' in content
    assert '- input-b.csv' in content


def test_generate_run_report_shows_metadata_fields(tmp_path: Path) -> None:
    output_dir = tmp_path / 'output'
    output_dir.mkdir()

    metadata_path = persist_run_metadata(
        output_dir=output_dir,
        software_version='0.1.0',
        configuration_version='v1',
        input_data_references=['input-a.csv'],
    )

    report_path = generate_run_report(output_dir=output_dir, metadata_path=metadata_path)

    assert report_path.exists()
    report_text = report_path.read_text(encoding='utf-8')
    assert 'software_version: 0.1.0' in report_text
    assert 'configuration_version: v1' in report_text
    assert 'input_data_references:' in report_text
    assert '- input-a.csv' in report_text
