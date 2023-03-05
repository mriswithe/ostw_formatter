from pprint import pprint

from hypothesis.strategies import characters
from pytest import mark
from hypothesis import given, strategies as st


@given(number=st.integers())
@mark.int
def test_int_parsing(number: int, grammar):
    out = grammar.parse(str(number), start="number")
    negorpos = "NEG" if number < 0 else "POS"
    strnum = [str(abs(number))]
    print(out)
    assert out == (negorpos, strnum)


@given(
    number=st.floats(
        allow_nan=False, allow_infinity=False, allow_subnormal=False
    ).filter(lambda x: True if x != 0 and x != -0 else False)
)
@mark.float
def test_float_parsing(number: float, grammar):
    out = grammar.parse(str(number), start="NUMBER")
    print(f"Orig: {number}")
    pprint(out)
    neg = number < 0


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
    pprint(test_str)
    out = grammar.parse(test_str, start="string")
    pprint(out)


@mark.expr
def test_parse_math_expr(grammar):
    pass
