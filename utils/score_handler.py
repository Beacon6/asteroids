import json
import logging
import os

from core import BASE_DIR

logger = logging.getLogger(__name__)


class ScoreHandler:
    _HIGHSCORE_FILE = BASE_DIR / 'highscore.json'

    @staticmethod
    def handle_highscore(score: int) -> None:
        if score > ScoreHandler._load_highscore():
            ScoreHandler._save_highscore(score)
            logger.info(f'New highscore: {score}')

    @staticmethod
    def _load_highscore() -> int:
        if not ScoreHandler._HIGHSCORE_FILE.exists():
            return 0
        with open(ScoreHandler._HIGHSCORE_FILE) as f:
            highscore: dict[str, int] = json.load(f)
            return highscore.get('highscore', 0)

    @staticmethod
    def _save_highscore(score: int) -> None:
        highscore_data = {'highscore': score}
        tmp_file = ScoreHandler._HIGHSCORE_FILE.with_suffix('.tmp')
        with open(tmp_file, 'w') as f:
            json.dump(highscore_data, f)
            os.replace(tmp_file, ScoreHandler._HIGHSCORE_FILE)
