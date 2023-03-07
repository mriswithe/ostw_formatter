from pytest import mark


@mark.parametrize("filename", ["enum"])
def test_curated(grammar, read_curated_file, filename: str):
    grammar.parse(read_curated_file(f"{filename}.ostw"))


def test_expr(grammar):
    sample = "0.016 + Nodes.Length / 40 * 0.016 + Nodes.Length * 0.016"
    # sample = "0.016 + Nodes.Length"
    sample = "Nodes.Length.Stuff.Such(a,b,x=y).stuff"
    sample = "Nodes.Length.Stuff.Such().stuff.such.What(a,b)"
    # sample = "What()"
    out = grammar.parse(sample, start="expr", trace=True)
    print("\n")
    from rich.pretty import pprint

    pprint(sample)
    pprint(out)
