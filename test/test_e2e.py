from pathlib import Path
from PyPDF2 import PdfReader
import os

def test_e2e():

    pdf_path = Path('test/test_data/in_margins.pdf')
    pdf_path.unlink(missing_ok=True)

    os.system('./scripts/example_usage.sh')

    pdf_path = Path('test/test_data/in_margins.pdf')
    assert pdf_path.exists(), f'File {pdf_path} does not exist'


    reader = PdfReader(str(pdf_path))
        
    # Get the number of pages
    num_pages = len(reader.pages)


    expected = [
        {'Page': 1, 'Width (pts)': 912, 'Height (pts)': 792, 'Number of characters': 5403},
        {'Page': 2, 'Width (pts)': 912, 'Height (pts)': 792, 'Number of characters': 0},
        {'Page': 3, 'Width (pts)': 912, 'Height (pts)': 792, 'Number of characters': 5726},
        {'Page': 4, 'Width (pts)': 912, 'Height (pts)': 792, 'Number of characters': 0},
        {'Page': 5, 'Width (pts)': 912, 'Height (pts)': 792, 'Number of characters': 5296},
        {'Page': 6, 'Width (pts)': 912, 'Height (pts)': 792, 'Number of characters': 0},
        {'Page': 7, 'Width (pts)': 912, 'Height (pts)': 792, 'Number of characters': 5284},
        {'Page': 8, 'Width (pts)': 912, 'Height (pts)': 792, 'Number of characters': 0},
        {'Page': 9, 'Width (pts)': 912, 'Height (pts)': 792, 'Number of characters': 4489},
        {'Page': 10, 'Width (pts)': 912, 'Height (pts)': 792, 'Number of characters': 0},
        {'Page': 11, 'Width (pts)': 912, 'Height (pts)': 792, 'Number of characters': 7447},
        {'Page': 12, 'Width (pts)': 912, 'Height (pts)': 792, 'Number of characters': 0},
        {'Page': 13, 'Width (pts)': 912, 'Height (pts)': 792, 'Number of characters': 331},
        {'Page': 14, 'Width (pts)': 912, 'Height (pts)': 792, 'Number of characters': 0}
    ]

    actual = []

    # Loop through each page and extract the required info
    page_info = []
    for i in range(num_pages):
        page = reader.pages[i]
        
        # Get page size (in points, where 1 point = 1/72 inch)
        width = page.mediabox.width
        height = page.mediabox.height
        
        # Extract text and count the number of characters
        text = page.extract_text()
        num_chars = len(text) if text else 0
        
        # Append the info to the list
        actual.append({
            'Page': i + 1,
            'Width (pts)': width,
            'Height (pts)': height,
            'Number of characters': num_chars
        })


    for i, (exp, act) in enumerate(zip(expected, actual)):
        assert exp == act, f'Page {i + 1} does not match'
