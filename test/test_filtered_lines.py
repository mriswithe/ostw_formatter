from pytest import mark
from rich.pretty import pprint


def test_import_lines_only(import_lines, grammar):
    print("\n")
    pprint(import_lines)
    pprint(grammar.parse(import_lines, start="start"))


def test_variable_declaration_lines(declaration_lines, grammar):
    out = grammar.parse(declaration_lines, start="multiple_declarations", trace=True)

    print("\n")
    pprint(out)
