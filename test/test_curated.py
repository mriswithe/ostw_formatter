from pytest import mark
from rich.pretty import pprint


@mark.parametrize("filename", ["enum"])
def test_curated(grammar, read_curated_file, filename: str):
    out = grammar.parse(read_curated_file(f"{filename}.ostw"), trace=True)
    pprint(out)


def test_just_enum(grammar, read_curated_file):

    out = grammar.parse(read_curated_file("enum.ostw"), start="enums_test", trace=True)
    print("\n")
    pprint(out)


def test_expr(grammar):
    sample = "0.016 + Nodes.Length / 40 * 0.016 + Nodes.Length * 0.016"
    # sample = "0.016 + Nodes.Length"
    sample = "Nodes.Length.Stuff.Such(a,b,x=y).stuff"
    sample = "Nodes.Length.Stuff.Such().stuff.such.What(a,b)"
    # sample = "What()"
    out = grammar.parse(sample, start="expr", trace=True)
    print("\n")

    pprint(sample)
    pprint(out)
