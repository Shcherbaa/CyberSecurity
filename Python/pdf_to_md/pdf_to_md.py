import os
import pathlib
import sys
import click
import pymupdf
import pymupdf4llm

# Folder with fra/rus.traineddata; override with --tessdata or TESSDATA_PREFIX
DEFAULT_TESSDATA = os.environ.get(
    "TESSDATA_PREFIX", r"C:\Program Files\Tesseract-OCR\tessdata"
)
# A page with fewer text characters than this is treated as a scan
MIN_TEXT_CHARS = 20


def needs_ocr(page: pymupdf.Page) -> bool:
  # Count only visible text: pymupdf4llm ignores the invisible (type 3) layer
  # of an old OCR pass, and it often holds garbage instead of Cyrillic
  visible = sum(
      len(span["chars"])
      for span in page.get_texttrace()
      if span["type"] != 3 and span.get("opacity", 1) > 0
  )
  return visible < MIN_TEXT_CHARS


def build_ocr_doc(
    src: pymupdf.Document, mode: str, lang: str, dpi: int, tessdata: str
) -> tuple[pymupdf.Document, int]:
  """Build a copy of the document with scanned pages replaced by OCR versions."""
  out = pymupdf.open()
  ocr_pages = 0
  with click.progressbar(range(src.page_count), label="    OCR") as pages:
    for i in pages:
      page = src[i]
      if mode == "always" or needs_ocr(page):
        pix = page.get_pixmap(dpi=dpi)
        ocr_pdf = pymupdf.open(
            "pdf", pix.pdfocr_tobytes(language=lang, tessdata=tessdata)
        )
        out.insert_pdf(ocr_pdf)
        ocr_pdf.close()
        ocr_pages += 1
      else:
        out.insert_pdf(src, from_page=i, to_page=i)
  return out, ocr_pages


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]),
    help="Convert a PDF file or a directory of PDFs to Markdown for LLMs.",
)
@click.option(
    "-s",
    "--source",
    required=True,
    type=click.Path(exists=True, resolve_path=True, path_type=pathlib.Path),
    help="Path to a source folder with PDFs or to a single .pdf file.",
)
@click.option(
    "-d",
    "--destination",
    required=True,
    type=click.Path(file_okay=False, resolve_path=True, path_type=pathlib.Path),
    help="Target directory for the .md files.",
)
@click.option(
    "--ocr",
    type=click.Choice(["auto", "always", "off"]),
    default="auto",
    show_default=True,
    help="auto: OCR only pages without text; always: OCR every page "
    "(for PDFs with a broken text layer); off: no OCR.",
)
@click.option(
    "-l", "--lang", default="fra+rus", show_default=True,
    help="Tesseract languages joined with '+'.",
)
@click.option(
    "--dpi", default=300, show_default=True, help="Render resolution for OCR."
)
@click.option(
    "--tessdata", default=DEFAULT_TESSDATA, show_default=True,
    help="Folder with *.traineddata files.",
)
def convert_pdfs(
    source: pathlib.Path,
    destination: pathlib.Path,
    ocr: str,
    lang: str,
    dpi: int,
    tessdata: str,
) -> None:
  if ocr != "off":
    missing = [
        l for l in lang.split("+")
        if not (pathlib.Path(tessdata) / f"{l}.traineddata").is_file()
    ]
    if missing:
      click.echo(
          f"[-] Missing language data {missing} in {tessdata}", err=True
      )
      sys.exit(1)

  destination.mkdir(parents=True, exist_ok=True)

  if source.is_file():
    if source.suffix.lower() != ".pdf":
      click.echo(f"[-] Error: {source.name} is not a PDF file.", err=True)
      sys.exit(1)
    pdf_files = [source]
    base = source.parent
  else:
    pdf_files = sorted(source.rglob("*.pdf"))
    base = source

  if not pdf_files:
    click.echo(f"[!] No PDF files found in: {source}")
    return

  converted = skipped = empty = failed = 0

  for pdf_file in pdf_files:
    # Keep the subfolder structure so files with the same name don't overwrite each other
    output_file = destination / pdf_file.relative_to(base).with_suffix(".md")

    if output_file.exists() and output_file.stat().st_size > 0:
      click.echo(f"[=] Already converted, skipping: {output_file.name}")
      skipped += 1
      continue

    src = doc = None
    try:
      click.echo(f"[*] Parsing: {pdf_file.name}...")
      src = pymupdf.open(pdf_file)
      doc = src
      if ocr != "off":
        doc, ocr_pages = build_ocr_doc(src, ocr, lang, dpi, tessdata)
        click.echo(f"    OCR pages: {ocr_pages} of {src.page_count}")

      md_text = pymupdf4llm.to_markdown(
          doc, page_chunks=False, show_progress=True
      )

      if not md_text.strip():
        click.echo(
            f"[!] No text found even after OCR: {pdf_file.name}, skipping",
            err=True,
        )
        empty += 1
        continue

      output_file.parent.mkdir(parents=True, exist_ok=True)
      output_file.write_text(md_text, encoding="utf-8")
      click.echo(f"[+] Saved: {output_file}")
      converted += 1
    except Exception as e:
      click.echo(f"[-] Error while processing {pdf_file.name}: {e}", err=True)
      failed += 1
    finally:
      if doc is not None and doc is not src:
        doc.close()
      if src is not None:
        src.close()

  click.echo(
      f"\n[=] Summary: converted {converted}, already done {skipped}, "
      f"no text {empty}, errors {failed}"
  )
  if failed:
    sys.exit(1)


if __name__ == "__main__":
  convert_pdfs()
