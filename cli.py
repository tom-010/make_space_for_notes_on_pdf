"""
This script provides a command-line interface (CLI) for adding margins to PDF files
within a directory or for a single file. Additionally, it inserts a blank page after 
each original page in the PDF. The goal is to enable users to easily apply custom 
left and right margins to their PDFs and add spacing with blank pages.

The script can process individual files or recursively process all PDFs in a directory.

Usage Example:
    python script_name.py /path/to/file_or_directory --left 200 --right 200 --force

Dependencies:
    - click (for CLI options)
    - tqdm (for progress indication)
    - pdf-crop-margins (must be installed for margin functionality)
    - PyPDF2 (for PDF manipulation, like adding blank pages)
"""
import click
from pathlib import Path
import os
from tqdm import tqdm
from PyPDF2 import PdfReader, PdfWriter
from pdfCropMargins import crop


def add_margins_and_blank_pages(path: Path, target: Path, left: int = 0, right: int = 0, force: bool = False):
    """
    Adds left and right margins to a PDF file using `pdf-crop-margins` utility.
    Inserts a blank page after every page of the original PDF.

    Parameters:
        path (Path): The path to the input PDF file.
        target (Path): The path to the output file with margins and blank pages applied.
        left (int): The amount of left margin in points.
        right (int): The amount of right margin in points.
        force (bool): Whether to overwrite the target file if it already exists.
    
    Raises:
        AssertionError: If the input file does not exist.
    """
    # Check if the input PDF file exists
    assert path.exists(), f'File {path} does not exist'
    
    # If target file exists and force is not enabled, skip processing
    if target.exists() and not force:
        return
    
    # Create the target directory if it doesn't exist
    target.parent.mkdir(parents=True, exist_ok=True)
    
    # First, we apply margins using the `pdf-crop-margins` tool
    temp_output = path.with_name(f'{path.stem}_temp{path.suffix}')
    bottom = 0
    top = 0
    
    args = ['-o', temp_output, '-p', 100, '-a4', -left, -bottom, -right, -top, path]
    args = [str(arg) for arg in args]
    crop(args)
    # ALTERNATIVE os.system(f'pdf-crop-margins -o "{temp_output}" -p 100 -a4 {-left} {-bottom} {-right} {-top} "{path}"')

    # crop(["-p", "20", "-u", "-s", "paper1.pdf"])

    # Now, we handle the insertion of blank pages using PyPDF2
    reader = PdfReader(temp_output)
    writer = PdfWriter()

    # Iterate through all the pages of the original PDF
    for page in reader.pages:
        writer.add_page(page)  # Add original page
        writer.add_blank_page()  # Add a blank page after it
    
    # Write the new PDF with added blank pages
    with open(target, 'wb') as out_file:
        writer.write(out_file)
    
    # Remove the temporary file with margins
    os.remove(temp_output)


@click.command()
@click.argument('input_file_or_dir', type=click.Path(exists=True, dir_okay=True, file_okay=True, path_type=Path))
@click.option('--left', type=int, default=150, help='Left margin in points (default: 0)')
@click.option('--right', type=int, default=150, help='Right margin in points (default: 0)')
@click.option('--force', is_flag=True, help='Force overwrite of existing files')
def cli(input_file_or_dir: Path, left: int, right: int, force: bool = False):
    """
    CLI command for applying margins to PDF files and inserting blank pages.
    
    Parameters:
        input_file_or_dir (Path): Path to the input PDF file or directory of PDFs.
        left (int): Left margin in points (default: 200 in this example).
        right (int): Right margin in points (default: 200 in this example).
        force (bool): If set, forces overwriting of existing output files.
    
    Example:
        python script.py /path/to/pdf --left 150 right 150 force
    """
    
    # Check if the input is a file or a directory
    f = input_file_or_dir

    # If it's a file, apply margins and add blank pages to the single file
    if input_file_or_dir.is_file():
        target = f.with_name(f'{f.stem}_margins{f.suffix}')
        add_margins_and_blank_pages(input_file_or_dir, target, left=left, right=right, force=force)
    
    # If it's a directory, recursively process all PDFs in the directory
    else:
        # Collect all PDF files in the directory, excluding files already processed
        files = [f for f in input_file_or_dir.rglob('*.pdf') if '_margins' not in f.stem]
        
        # Progress bar to track processing of multiple files
        for f in tqdm(files):
            if '_margins' in f.stem:
                continue
            target = f.with_name(f'{f.stem}_margins{f.suffix}')
            add_margins_and_blank_pages(f, target, left=left, right=right, force=force)

# Entry point to the script
if __name__ == '__main__':
    cli()  # Invoke the CLI command
