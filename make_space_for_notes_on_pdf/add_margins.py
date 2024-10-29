from PyPDF2 import PdfReader, PdfWriter, Transformation, PageObject
from tqdm import tqdm
from pathlib import Path
import math


def add_margins(
    input_path: str | Path,
    output_path: str | Path = None,
    left=0,
    right=0,
    top=0,
    bottom=0,
    force_relative=False,
):
    if not output_path:
        output_path = input_path

    input_path = Path(input_path)
    output_path = Path(output_path)

    assert right >= 0, "right margin can not be negative"
    assert left >= 0, "left margin can not be negative"
    assert top >= 0, "top margin can not be negative"
    assert bottom >= 0, "bottom margin can not be negative"

    with input_path.open("rb") as f:
        pdf = PdfReader(f)
        writer = PdfWriter()

        for page in tqdm(pdf.pages):
            # calculate the target size
            original_width = float(page.mediabox.width)
            original_height = float(page.mediabox.height)

            if force_relative:
                right = math.ceil(original_width * right)
                left = math.ceil(original_width * left)
                top = math.ceil(original_height * top)
                bottom = math.ceil(original_height * bottom)
            else:
                if right < 1:
                    right = math.ceil(original_width * right)
                if left < 1:
                    left = math.ceil(original_width * left)
                if top < 1:
                    top = math.ceil(original_height * top)
                if bottom < 1:
                    bottom = math.ceil(original_height * bottom)

            top = int(top)
            bottom = int(bottom)
            left = int(left)
            right = int(right)

            width = original_width + left + right
            height = original_height + top + bottom

            # create a page with the desired measures and place the original page on top
            bg = PageObject.create_blank_page(width=width, height=height)
            bg.merge_page(page)
            bg.add_transformation(Transformation().translate(tx=left, ty=bottom))

            writer.add_page(bg)

        # Write the output to a new PDF file
        with output_path.open("wb") as output_file:
            writer.write(output_file)
