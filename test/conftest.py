from itertools import chain
from pathlib import Path

from pytest import fixture
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tatsu.grammars import Grammar

FILE_PARENT = Path(__file__).parent
GRAMMAR_FILE = FILE_PARENT.parent / "grammar" / "main.ebnf"
CORPUS = (FILE_PARENT / "corpus").rglob("*.del")
CORPUS_ALL_LINES = list(
    chain.from_iterable(f.read_text("utf8").splitlines() for f in CORPUS)
)
CURATED_DIR = FILE_PARENT / "curated"


@fixture(scope="session")
def all_lines():
    return CORPUS_ALL_LINES


@fixture
def filter_all_lines(all_lines):
    def inner(filter_: str) -> str:
        return "\n".join([line for line in all_lines if filter_ in line])

    return inner


@fixture
def import_lines(filter_all_lines):
    return filter_all_lines("import")


@fixture
def grammar() -> "Grammar":
    from tatsu import compile

    return compile(GRAMMAR_FILE.read_text(), colorize=True)


@fixture()
def read_curated_file():
    def inner(filename: str) -> str:
        return (CURATED_DIR / filename).read_text("utf-8")

    return inner
