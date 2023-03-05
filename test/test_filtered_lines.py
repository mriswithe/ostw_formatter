def test_import_lines_only(import_lines, grammar):
    out = grammar.parse(import_lines)
