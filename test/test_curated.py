from pytest import mark


@mark.parametrize("filename", ["enum", "struct", "global_func", "variables"])
def test_curated(grammar, read_curated_file, filename: str):
    grammar.parse(read_curated_file(f"{filename}.ostw"))
