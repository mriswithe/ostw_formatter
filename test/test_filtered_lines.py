from pytest import mark


def test_import_lines_only(import_lines, grammar):
    grammar.parse(import_lines)


@mark.skip()
def test_variable_declaration_lines(declaration_lines, grammar):
    grammar.parse(declaration_lines)
