from pytest import mark


@mark.parametrize("filename", ["enum", "struct", "global_func", "variables"])
def test_curated(grammar, read_curated_file, filename: str):
    grammar.parse(read_curated_file(f"{filename}.ostw"))


def test_expr(grammar):
    out = grammar.parse(
        "(0.016 + Nodes.Length / 40 * 0.016 + Nodes.Length * 0.016)", start="expr"
    )
    assert len(out) == 1
