from tatsu import compile
from pathlib import Path

_FILE_DIR = Path(__file__).parent.absolute()
_GRAMMAR_DIR = _FILE_DIR / "grammar"
_MAIN_FILE = _GRAMMAR_DIR / "main.ebnf"
_old_cwd = Path.cwd()

OstwGrammar = compile(_MAIN_FILE.read_text(), filename=str(_MAIN_FILE.absolute()))
