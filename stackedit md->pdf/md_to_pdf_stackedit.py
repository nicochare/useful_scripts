import sys
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

TEMPLATE_HTML = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>{style}</style>
  <style>
    @page {{
      size: 210mm 380mm;  /* width A4, height 380mm */
      margin: 2cm;
    }}
  </style>
</head>
<body class="stackedit stackedit--pdf">
  <div class="stackedit__html">{html}</div>
</body>
</html>
"""

def md_to_pdf(md_path: Path, css_path: Path, output_pdf_path: Path):
    markdown_text = md_path.read_text(encoding="utf-8")

    html_content = markdown.markdown(markdown_text, extensions=['fenced_code', 'tables'])

    css_text = css_path.read_text(encoding="utf-8")

    html_final = TEMPLATE_HTML.format(
        title=md_path.stem,
        style=css_text,
        html=html_content
    )

    HTML(string=html_final, base_url=".").write_pdf(str(output_pdf_path))
    print(f"✓ Generated: {output_pdf_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python md_to_pdf_stackedit.py file.md stack_edit_style.css")
        sys.exit(1)

    md_file = Path(sys.argv[1])
    css_file = Path(sys.argv[2])

    if not md_file.exists() or not css_file.exists():
        print("Error: .md or .css file not found.")
        sys.exit(1)

    pdf_output = md_file.with_suffix(".pdf")
    md_to_pdf(md_file, css_file, pdf_output)
