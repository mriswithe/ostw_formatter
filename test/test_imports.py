# noinspection PyUnresolvedReferences
def test_imports():
    """Simply testing that I can import the package"""
    import ostw

    from tatsu.grammars import Grammar

    assert isinstance(ostw.OstwGrammar, Grammar)
