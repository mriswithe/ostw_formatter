from rich.pretty import pprint
from pytest import mark

# noinspection PyUnresolvedReferences
def test_imports():
    """Simply testing that I can import the package"""
    import ostw

    from tatsu.grammars import Grammar

    assert isinstance(ostw.OstwGrammar, Grammar)


@mark.skip("Not ready for this yet")
def test_corpus(grammar, corpus_files):
    for fp in corpus_files:
        print(f"\nTesting: {fp}\n\n")
        out = grammar.parse(fp.read_text("utf-8"))
        pprint(out)
