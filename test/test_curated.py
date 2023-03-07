from pprint import pprint

import rich
from pytest import mark


@mark.parametrize("filename", ["enum", "struct", "global_func", "variables"])
def test_curated(grammar, read_curated_file, filename: str):
    grammar.parse(read_curated_file(f"{filename}.ostw"))


def test_expr(grammar):
    sample = "0.016 + Nodes.Length / 40 * 0.016 + Nodes.Length * 0.016"
    # sample = "0.016 + Nodes.Length"
    sample = "Nodes.Length.Stuff.Such(a,b,x=y).stuff"
    sample = "Nodes.Length.Stuff.Such().stuff.such.What(a,b)"
    # sample = "What()"
    out = grammar.parse(sample, start="test_start", trace=True, parseinfo=False)
    print("\n")
    from rich.pretty import pprint

    pprint(sample)
    pprint(out)
