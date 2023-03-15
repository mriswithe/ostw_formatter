from rich.pretty import pprint


def test_curated_files(curated_pair, grammar):
    rule, src = curated_pair
    src_text = src.read_text("utf-8")
    print(f"\nsrc:{src_text}")
    out = grammar.parse(src_text, start=rule, trace=True)

    pprint(out)


def test_curated_variable(variable_line, grammar):
    """Pass or fail, wants a declaration with or without assignment"""
    print("\n")
    print(f"{variable_line=}")
    out = grammar.parse(variable_line, start="one_decl", trace=True)
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
