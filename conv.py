from PyPDF2 import PdfReader, PdfWriter, Transformation, PageObject
from PyPDF2.generic import RectangleObject
from tqdm import tqdm
from pathlib import Path
import math


def add_margins(
    input_path: str | Path,
    output_path: str | Path = None,
    margin_left=0,
    margin_right=0,
    margin_top=0,
    margin_bottom=0,
    force_relative=False,
):
    if not output_path:
        output_path = input_path

    input_path = Path(input_path)
    output_path = Path(output_path)

    assert margin_right >= 0, "right margin can not be negative"
    assert margin_left >= 0, "left margin can not be negative"
    assert margin_top >= 0, "top margin can not be negative"
    assert margin_bottom >= 0, "bottom margin can not be negative"

    with input_path.open("rb") as f:
        pdf = PdfReader(f)
        writer = PdfWriter()

        for page in tqdm(pdf.pages):
            # calculate the target size
            original_width = float(page.mediabox.width)
            original_height = float(page.mediabox.height)

            if force_relative:
                margin_right = math.ceil(original_width * margin_right)
                margin_left = math.ceil(original_width * margin_left)
                margin_top = math.ceil(original_height * margin_top)
                margin_bottom = math.ceil(original_height * margin_bottom)
            else:
                if margin_right < 1:
                    margin_right = math.ceil(original_width * margin_right)
                if margin_left < 1:
                    margin_left = math.ceil(original_width * margin_left)
                if margin_top < 1:
                    margin_top = math.ceil(original_height * margin_top)
                if margin_bottom < 1:
                    margin_bottom = math.ceil(original_height * margin_bottom)

            width = original_width + margin_left + margin_right
            height = original_height + margin_top + margin_bottom

            # create a page with the desired measures and place the original page on top
            bg = PageObject.create_blank_page(width=width, height=height)
            bg.merge_page(page)
            bg.add_transformation(
                Transformation().translate(tx=margin_left, ty=margin_bottom)
            )

            writer.add_page(bg)

        # Write the output to a new PDF file
        with output_path.open("wb") as output_file:
            writer.write(output_file)


add_margins(
    "input.pdf",
    "output.pdf",
    margin_left=0.0,
    margin_right=0.3,
    margin_top=0,
    margin_bottom=0.5,
)
