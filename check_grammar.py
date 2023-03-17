from pathlib import Path

import tatsu.exceptions
from tatsu.infos import LineInfo


def failure_context(e: tatsu.exceptions.FailedParse, context: int = 5):
    li: LineInfo = e.tokenizer.line_info(e.pos)
    max_line = li.line + context
    min_line = li.line - context
    crappy_line = "#############################################"
    out_lines = [crappy_line]
    for idx, line in enumerate(Path(li.filename).read_text("utf-8").splitlines()):
        if idx < min_line or idx > max_line:
            continue
        if idx == li.line:
            line = f"{line}<-------- THIS IS WHERE IT BROKE"
        out_lines.append(line)
    out_lines.append(crappy_line)
    return "\n".join(out_lines)


def main():
    try:
        import ostw
    except tatsu.exceptions.FailedParse as e:
        print(failure_context(e))


if __name__ == "__main__":

    main()
