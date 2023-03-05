def test_import_lines_only(import_lines, grammar):
    grammar.parse(import_lines)


def test_variable_declaration_lines(declaration_lines, grammar):
    grammar.parse(declaration_lines)
