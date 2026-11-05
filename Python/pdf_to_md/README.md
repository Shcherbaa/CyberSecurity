# pdf_to_md

A command-line tool that converts PDF files, or whole folders of them, into clean Markdown. Scanned pages are detected automatically and passed through OCR, so image-only books end up as searchable text too.

## Why

I study from a large library of PDFs: textbooks, course materials and scanned books in French and Russian. PDF is a poor format for note-taking and for working with LLMs: text is hard to search, copy or feed into a model, and scanned pages contain no text at all. This tool turns the whole library into Markdown in one run, ready for my Obsidian notes and for LLM-assisted study.

## Features

- Converts a single PDF or a folder tree, keeping the subfolder structure in the output
- Detects scanned pages by counting visible text and runs OCR only where it is needed
- Ignores the invisible text layer left by old OCR, which often contains garbage instead of Cyrillic
- `--ocr always` mode for PDFs with a broken text layer
- Resumable: files that were already converted are skipped
- Summary at the end (converted / skipped / no text / errors) and a non-zero exit code on failure

## Requirements

- Python 3.10+ (tested on 3.14)
- Python packages: `pip install -r requirements.txt`
- Tesseract language data (`*.traineddata`) for every OCR language. The easiest way to get it is to install [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract), which ships the `tessdata` folder. Not needed with `--ocr off`.

The tool looks for language data in `TESSDATA_PREFIX`, then in `C:\Program Files\Tesseract-OCR\tessdata`; use `--tessdata` to point elsewhere.

## Usage

```bash
# A whole folder, OCR only where needed
python pdf_to_md.py -s ./books -d ./books_md

# One file with a broken text layer, English OCR
python pdf_to_md.py -s ./scan.pdf -d ./out --ocr always -l eng

# Text-only PDFs, no OCR
python pdf_to_md.py -s ./docs -d ./docs_md --ocr off
```

| Option | Default | Description |
|---|---|---|
| `-s, --source` | required | PDF file or folder with PDFs (searched recursively) |
| `-d, --destination` | required | Output folder for `.md` files |
| `--ocr` | `auto` | `auto`: pages without text only; `always`: every page; `off`: no OCR |
| `-l, --lang` | `fra+rus` | Tesseract languages joined with `+` |
| `--dpi` | `300` | Render resolution for OCR |
| `--tessdata` | see above | Folder with `*.traineddata` files |

## Example output

```
❯ python3 -m pdf_to_md -s 'D:\Alert ticket.pdf' -d 'D:\' --ocr off
Consider using the pymupdf_layout package for a greatly improved page layout analysis.
[*] Parsing: Alert ticket.pdf...
Processing D:\Alert ticket.pdf...
[========================================] (1/1)
[+] Saved: D:\Alert ticket.md

[=] Summary: converted 1, already done 0, no text 0, errors 0
```

## How it works

1. For each page, the tool counts characters in the visible text layer. A page with fewer than 20 is treated as a scan.
2. Scanned pages are rendered to an image and run through Tesseract OCR, which produces a new PDF page with a real text layer. Other pages are copied as they are.
3. The resulting document is converted to Markdown by `pymupdf4llm`.

## Limitations

- OCR quality depends on the scan; low-quality pages may need a higher `--dpi`, which is slower.
- Complex layouts (multi-column pages, formulas, nested tables) may not convert cleanly.
- A file is skipped if a non-empty `.md` with the same name already exists; delete it to convert again.