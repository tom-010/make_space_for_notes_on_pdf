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

FEATURES:

* Add margins left and right of the document
* Add a blank page after each page in the PDF


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