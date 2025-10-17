"""
Useful constant variables.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ASSETS_PATH = PROJECT_ROOT / "words"
CRAWLER_CONFIG_PATH = PROJECT_ROOT / "scraper_config.json"

CONFIG_DIR = PROJECT_ROOT / "config"

NUM_ARTICLES_UPPER_LIMIT = 150
TIMEOUT_LOWER_LIMIT = 0
TIMEOUT_UPPER_LIMIT = 60

print(ASSETS_PATH)