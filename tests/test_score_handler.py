import json
from pathlib import Path

import pytest

from utils.score_handler import ScoreHandler


@pytest.fixture
def score_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    filepath = tmp_path / 'highscore.json'
    monkeypatch.setattr(ScoreHandler, '_HIGHSCORE_FILE', filepath)
    return filepath


def test_load_from_existing_file(score_file: Path) -> None:
    score_file.write_text(json.dumps({'highscore': 42}))
    assert ScoreHandler._load_highscore() == 42


def test_load_returns_zero_when_file_missing(score_file: Path) -> None:
    assert ScoreHandler._load_highscore() == 0


def test_load_returns_zero_for_missing_key(score_file: Path) -> None:
    score_file.write_text(json.dumps({}))
    assert ScoreHandler._load_highscore() == 0


def test_save_creates_file(score_file: Path) -> None:
    ScoreHandler._save_highscore(99)
    assert score_file.exists()
    assert json.loads(score_file.read_text()) == {'highscore': 99}


def test_save_overwrites_existing(score_file: Path) -> None:
    score_file.write_text(json.dumps({'highscore': 10}))
    ScoreHandler._save_highscore(99)
    assert json.loads(score_file.read_text()) == {'highscore': 99}


def test_handle_highscore_saves_when_higher(score_file: Path) -> None:
    score_file.write_text(json.dumps({'highscore': 50}))
    ScoreHandler.handle_highscore(100)
    assert json.loads(score_file.read_text()) == {'highscore': 100}


def test_handle_highscore_skips_when_lower(score_file: Path) -> None:
    score_file.write_text(json.dumps({'highscore': 200}))
    ScoreHandler.handle_highscore(100)
    assert json.loads(score_file.read_text()) == {'highscore': 200}
