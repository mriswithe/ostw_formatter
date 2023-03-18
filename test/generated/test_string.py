from _pytest.mark import MARK_GEN
from hypothesis import given, strategies as st
from hypothesis.strategies import characters


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


@mark.parametrize("delim", ('"', "'"))
@given(
    import_name=st.text(
        min_size=1,
        alphabet=st.characters(
            blacklist_categories=("Cs",), blacklist_characters=["\n", "'", '"']
        ),
    )
)
def test_import_string(import_name: str, delim: str, grammar):
    test_str = f"import {delim}{import_name}{delim};"
    out = grammar.parse(test_str, rule="import")
    assert out[0][0]["import_name"][1] == import_name
