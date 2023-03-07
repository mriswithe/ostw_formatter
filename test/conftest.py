import traceback
from itertools import chain
from pathlib import Path

from _pytest.monkeypatch import MonkeyPatch
from pytest import fixture
from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
    from tatsu.grammars import Grammar

FILE_PARENT = Path(__file__).parent
GRAMMAR_DIR = FILE_PARENT.parent / "ostw" / "grammar"
GRAMMAR_FILE = GRAMMAR_DIR / "main.ebnf"
CORPUS = list((FILE_PARENT / "corpus").rglob("*.del"))
CORPUS_ALL_LINES = list(
    chain.from_iterable(f.read_text("utf8").splitlines() for f in CORPUS)
)
CURATED_DIR = FILE_PARENT / "curated"

TRACE = os.environ.get("TRACE", False)


@fixture(scope="session")
def all_lines():
    return CORPUS_ALL_LINES


@fixture(scope="session")
def corpus_files():
    return CORPUS


@fixture
def filter_all_lines(all_lines):
    def inner(filter_: str) -> str:
        return "\n".join([line for line in all_lines if filter_ in line])

    return inner


@fixture
def import_lines(filter_all_lines):
    return filter_all_lines("import")


@fixture
def declaration_lines(filter_all_lines):
    return "\n".join(
        filter(
            lambda x: x if "class " not in x else None,
            [filter_all_lines(i) for i in ["globalvar", "playervar"]],
        )
    )


@fixture(scope="session")
def grammar() -> "Grammar":
    from tatsu import compile

    try:
        with MonkeyPatch.context() as mp:
            mp.chdir(GRAMMAR_DIR)
            return compile(
                GRAMMAR_FILE.read_text(),
                colorize=True,
                filename=str(GRAMMAR_FILE.resolve()),
            )
    except:
        # shhhhh traceback too many words
        traceback.print_exc(limit=1)
        raise Exception("Unable to Compile") from None


@fixture()
def read_curated_file():
    def inner(filename: str) -> str:
        return (CURATED_DIR / filename).read_text("utf-8")

    return inner
