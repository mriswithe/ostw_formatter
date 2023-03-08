from rich.pretty import pprint


def test_curated(curated_pair, grammar, record_property):
    rule, src = curated_pair
    out = grammar.parse(src.read_text("utf-8"), start=rule)
    pprint(out)


def test_expr(grammar):
    sample = "0.016 + Nodes.Length / 40 * 0.016 + Nodes.Length * 0.016"
    # sample = "0.016 + Nodes.Length"
    sample = "Nodes.Length.Stuff.Such(a,b,x=y).stuff"
    sample = "Nodes.Length.Stuff.Such().stuff.such.What(a,b)"
    # sample = "What()"
    out = grammar.parse(sample, start="expr")
    print("\n")

    pprint(sample)
    pprint(out)
