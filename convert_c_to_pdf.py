#!/usr/bin/env python3
# This was completely done by AI but I found it cool and useful enough to add it.
"""
convert_c_to_pdf.py

Converts all **.c** and **.h** files in a directory (recursive search)
to PDF files with *Atom One Dark* style syntax highlighting. The final PDF
occupies **100% of the A4 page** (without margins) and is saved in a subfolder
**output** located next to the script.

Each PDF keeps the original extension in the name (e.g..
`file.c.pdf` and `file.h.pdf`) to avoid collisions when both files exist.

---
Requirements
-----------

```bash
pip install pygments weasyprint
```

> Debian/Ubuntu:
>
> ```bash
> sudo apt-get install python3-cairocffi libpango-1.0-0 libcairo2 gdk-pixbuf2.0-0 libffi-dev
> ```

---
Usage
---

```bash
python convert_c_to_pdf.py /path/to/directory
```
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import CLexer
from pygments.style import Style
from pygments.token import (
    Comment,
    Generic,
    Keyword,
    Literal,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
)
from weasyprint import HTML


class AtomOneDarkStyle(Style):
    """*Atom One Dark* theme for Pygments (simplified palette)."""

    background_color = "#282c34"
    default_style = ""

    styles = {
        Text: "#abb2bf",
        Comment: "italic #5c6370",
        Keyword: "#c678dd",
        Name.Builtin: "#e6c07b",
        Name.Function: "#61aeee",
        Name.Class: "#e6c07b",
        Name.Exception: "#e06c75",
        Name.Decorator: "#c678dd",
        Name.Variable: "#d19a66",
        Name.Constant: "#56b6c2",
        Literal: "#56b6c2",
        String: "#98c379",
        Number: "#d19a66",
        Operator: "#56b6c2",
        Punctuation: "#abb2bf",
        Generic.Heading: "#61aeee",
        Generic.Subheading: "#61aeee",
        Generic.Deleted: "#e06c75",
        Generic.Inserted: "#98c379",
        Generic.Error: "#e06c75",
        Generic.Emph: "italic",
        Generic.Strong: "bold",
    }


# ---------------------------------------------------------------------------
# Auxiliary functions
# ---------------------------------------------------------------------------

def discover_sources(root: Path) -> Iterable[Path]:
    for pattern in ("*.c", "*.h"):
        yield from root.rglob(pattern)


def convert_file_to_pdf(src: Path, dst: Path) -> None:
    """Converts *src* (= .c / .h) to PDF and saves it to *dst*."""
    try:
        code = src.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        print(f"[ERROR] No se pudo leer {src}: {exc}", file=sys.stderr)
        return

    formatter = HtmlFormatter(
        style=AtomOneDarkStyle,
        full=False,
        linenos="table",
        noclasses=False,
    )

    highlighted = highlight(code, CLexer(), formatter)

    html_doc = f"""<!DOCTYPE html>
<html lang=\"es\">
<head>
<meta charset=\"utf-8\">
<style>
@page {{
    size: A4;
    margin: 0;
    background: {AtomOneDarkStyle.background_color};
}}
html, body {{
    margin: 0;
    padding: 0;
    background: {AtomOneDarkStyle.background_color};
}}
{formatter.get_style_defs('.highlight')}
</style>
<title>{src.name}</title>
</head>
<body>
{highlighted}
</body>
</html>"""

    dst.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_doc, base_url=".").write_pdf(str(dst))


def process_directory(root: Path, output_dir: Path) -> None:
    sources = list(discover_sources(root))
    if not sources:
        print("[INFO] No .c/.h files found in", root)
        return

    for src in sources:
        relative = src.relative_to(root)
        pdf_name = f"{relative.name}.pdf"
        dst = output_dir / relative.parent / pdf_name
        convert_file_to_pdf(src, dst)
        print(f"[OK] {src} → {dst}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Converts all .c and .h files to PDF (Atom One Dark theme, A4 no margins)."
    )
    parser.add_argument("directory", type=Path, help="Root directory")
    args = parser.parse_args()

    root = args.directory.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"{root} is not a valid directory.")

    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    process_directory(root, output_dir)


if __name__ == "__main__":
    main()
