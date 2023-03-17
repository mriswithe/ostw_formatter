import sys
from itertools import chain
from pathlib import Path
import os

import pytest
import tatsu.exceptions

from pytest import (
    fixture,
    MonkeyPatch,
    TestReport,
    CollectReport,
    CallInfo,
    Function,
)
from tatsu.infos import LineInfo
from typing import TYPE_CHECKING

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
            grammar = compile(
                GRAMMAR_FILE.read_text(),
                colorize=True,
                filename=str(GRAMMAR_FILE.resolve()),
            )
    except tatsu.exceptions.FailedParse as e:
        # # shhhhh traceback too many words
        li: LineInfo = e.tokenizer.line_info(e.pos)
        path = Path(li.filename)
        base_dir = FILE_PARENT.parent
        rel_path = path.relative_to(base_dir)
        sys.stderr.write("\n\n..\\" + str(rel_path.with_suffix(".ebnf")))

        raise
    return grammar


def iter_curated_pairs():
    for d in filter(lambda x: x.is_dir(), CURATED_DIR.glob("*")):
        for f in d.glob("*"):
            yield d.name, f


def iter_ids():
    for name, fp in iter_curated_pairs():
        yield f"{name}-{fp.name}"


@fixture(params=list(iter_curated_pairs()), ids=list(iter_ids()))
def curated_pair(request):
    return request.param


def iter_variable_lines():
    return [line for line in (CURATED_DIR / "variables.del").read_text().splitlines()]


def marked_variable_lines():
    """Uses stupid string in string comparisons to mark different language features in
    the variable soup file"""

    def add_mark(mark_name: str):
        marks.append(getattr(pytest.mark, mark_name)())

    for line in iter_variable_lines():
        marks: list[pytest.mark] = []
        if "[" in line and "]" in line:
            add_mark("array")
        if "globalvar" in line:
            add_mark("globalvar")
        if "define" in line:
            add_mark("define")
        if "playervar" in line:
            add_mark("playervar")
        if "!" in line:
            add_mark("extended")
        if len(marks) == 0:
            yield line
        else:
            yield pytest.param(line, marks=marks)


@fixture(params=marked_variable_lines(), ids=list(range(len(iter_variable_lines()))))
def variable_line(request):
    return request.param
