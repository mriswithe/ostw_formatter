from pprint import pprint

from hypothesis.strategies import characters
from pytest import mark
from hypothesis import given, strategies as st, example


@mark.int
@given(number=st.integers())
@example(number=0)
@example(number=-0)
def test_int_parsing(number: int, grammar):
    out = grammar.parse(str(number), start="number")
    strnum = [str(abs(number))]
    if number > 0:
        assert ("POS", strnum) == out
    elif number < 0:
        assert ("NEG", strnum) == out
    elif number == 0:
        # Zero
        assert ("POS", strnum) == out
    elif number == -0:
        assert ("NEG", strnum) == out
    print(f"\n{number=}\n{out=}\n{strnum=}")


@given(left=st.integers(), right=st.integers(min_value=1))
@mark.float
def test_simple_float(left: int, right: int, grammar):
    num_str = f"{left}.{right}"
    p, (l, r) = grammar.parse(num_str, start="number")
    assert int(r) == right
    if left >= 0:
        assert int(l) == left
        assert p == "POS"
    else:
        assert int("-" + l) == left
        assert p == "NEG"
    print(f'Left: {left}\tParsed Left: {"-" if p == "NEG" else ""}{l}')
    print(f"Right: {right}\tParsed Right: {r}")


@mark.parametrize("delim", ('"', "'"))
@given(
    gened=st.text(
        characters(blacklist_categories=("Cs",), blacklist_characters=["\n"]),
        min_size=1,
    )
)
@mark.string
def test_string_parsing(gened: str, delim: str, grammar):
    test_str = delim + gened.replace(delim, f"\\{delim}") + delim

    out = grammar.parse(test_str, start="string")
    print(f"\n{gened=}\n{out=}")


# lowish_int = st.integers(min_value=-1000, max_value=1000)
lowish_int = st.just(-100)
operators = "+-/*"


@mark.parametrize("op", operators)
@given(
    left=lowish_int,
    right=lowish_int,
)
@mark.expr
def test_parse_math_expr(op: str, left: int, right: int, grammar):
    test_expr = f"{left} {op} {right}"
    out = grammar.parse(
        test_expr,
        start="math",
        trace=True,
    )
    print(f"{test_expr}\n{out}")
