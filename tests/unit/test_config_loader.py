from __future__ import annotations

from pathlib import Path

from src.workflow_demo.config_loader import load_run_configuration


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
