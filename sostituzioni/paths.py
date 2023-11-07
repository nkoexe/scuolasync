from pathlib import Path

ROOT = Path(__file__).resolve().parent

DATABASE = ROOT / 'database' / 'test.db'
CONFIGURAZIONE = ROOT / 'database' / 'configurazione.json'

FLASK_TEMPLATES = ROOT / 'view' / 'templates'
FLASK_STATIC = ROOT / 'view' / 'static'

# todo: file not needed, use paths in configuration instead
