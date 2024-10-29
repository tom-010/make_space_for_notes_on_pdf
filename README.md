Make space for Notes on PDF
===========================

I have a tablet with a pen as ebook-reader. 
I like to make notes on the side of the PDFs when reading. 
Often there is not enough space on the margins. 

I also like to draw diagrams and notes on the PDF. 
There is not enough space at the top and bottom. 
This leads to bad nodes and diagrams I can not decypher later.

This tool adds margins left and right of the text and adds 
blank pages between each page. With this I have enough space
for my thoughts and ideas and space to learn.

# Features

* Add margins left and right of the document
* Add a blank page after each page in the PDF

Before:

![before](docs/before.png)

After:

![after](docs/after.png)


## Usage

See `scripts/example_usage.sh` for a runnable script, that is also
checked by the test-suite (e2e).

Common use-case is to run 

```python3
python3 cli.py path/to/pdf-file.pdf
```

This creates a file called `path/to/pdf-file_margins.pdf` as output.

Or you can process a directory via 

```python3
python3 cli.py path/to/dir/with/pdfs/
```

If there is a `path/to/dir/with/pdfs/a.pdf` there is now a 
`path/to/dir/with/pdfs/a_margins.pdf` as output.

If you want to know more, check

```python3
python3 cli.py --help
```

## More information

If you nee to know details, check out `make_space_for_notes_on_pdf/cli.py`. It is pretty straightforward.

## Limitations and next Steps

- Output-directory, not only suffix for output-files 
- FastAPI server in Dockerfile to make installation easy (with Gradio UI)
- Make it intallable (as python-package)
- Add nix-package
- Detect if 2 columns and be smart where to add margins (1 column, only right margin)
- Add background, like raster, dots, etc.

## Next steps

- Make it installable
- Push to pypi
- Set into metadata that margins were added
- One or two columns?

## Thank you

This is just a wrapper around 

* pdfcropmargins  
* PyPDF2
