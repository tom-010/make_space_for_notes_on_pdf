import pikepdf
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import RectangleObject

def add_margins_to_pdf(input_pdf_path, output_pdf_path, margin_size=20):
    # Load the original PDF using pikepdf to access page sizes
    with pikepdf.open(input_pdf_path) as pdf:
        new_pdf_writer = PdfWriter()
        
        for page_num, page in enumerate(pdf.pages):
            # Get the original page dimensions
            original_width = page.MediaBox[2]
            original_height = page.MediaBox[3]
            
            # Define new dimensions with added margins
            new_width = original_width + 2 * margin_size
            new_height = original_height + 2 * margin_size
            
            # Adjust page dimensions using PyPDF2
            new_page = new_pdf_writer.add_blank_page(width=new_width, height=new_height)
            
            # Set a translation matrix to move the original content by margin size
            new_page.merge_page(
                PdfReader(input_pdf_path).pages[page_num],
                transformation_matrix=[1, 0, 0, 1, margin_size, margin_size]
            )
        
        # Save to output file
        with open(output_pdf_path, "wb") as output_pdf_file:
            new_pdf_writer.write(output_pdf_file)

# Example usage:
add_margins_to_pdf("input.pdf", "output_with_margins.pdf", margin_size=50)
