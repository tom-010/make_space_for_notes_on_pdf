from PyPDF2 import PdfReader, PdfWriter, Transformation, PageObject
from PyPDF2.generic import RectangleObject
from tqdm import tqdm


margin_left = 0
margin_right = 0
margin_bottom = 0
margin_top = 400

# Open the input PDF file
with open("input.pdf", "rb") as f:
    pdf = PdfReader(f)
    number_of_pages = len(pdf.pages)

    writer = PdfWriter()
    margin = 100
    print(f"Margin: {margin}")

    for i in tqdm(range(number_of_pages)):
        page = pdf.pages[i]

        original_width = float(page.mediabox.width)
        original_height = float(page.mediabox.height)
        width = original_width + margin_left + margin_right
        height = original_height + margin_top + margin_bottom

        # page.cropbox = RectangleObject((0, 0, width + 1000, height + 10000))
        # new_page = writer.add_blank_page(width, height)

        # Merge the original page onto the new page with margins applied
        # new_page.merge_page(page)

        # Calculate the translation to account for margins
        # page.mediabox.lower_left = (margin, margin)
        # page.mediabox.upper_right = (width - margin, height - margin)

        # page.add_transformation(
        #     Transformation().scale(0.5, 0.5)  # .translate(tx=margin, ty=margin)
        # )
        #

        bg = PageObject.create_blank_page(width=width, height=height)

        bg.merge_page(page)
        bg.add_transformation(Transformation().translate(tx=margin_left, ty=margin_top))

        writer.add_page(bg)

    # Write the output to a new PDF file
    with open("output.pdf", "wb") as output_file:
        writer.write(output_file)
