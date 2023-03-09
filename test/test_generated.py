from hypothesis.strategies import characters
from pytest import mark
from hypothesis import example, given, strategies as st


@mark.int
@given(number=st.integers())
@example(number=0)
@example(number=-0)
def test_int_parsing(number: int, grammar):
    out = grammar.parse(str(number), start="number")
    if number >= 0:
        assert int(out) == number
    else:
        l, r = out
        assert int(l + r) == number


@given(left=st.integers(), right=st.integers(min_value=0))
@mark.float
def test_simple_float(left: int, right: int, grammar):
    num_str = f"{left}.{right}"
    out = grammar.parse(num_str, start="number")
    assert num_str == "".join(out)


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


lowish_int = st.integers(min_value=-1000, max_value=1000)
# lowish_int = st.just(-100)
operators = "+-/*"


@mark.parametrize("op", operators)
@given(
    left=st.integers(),
    right=st.integers(),
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
