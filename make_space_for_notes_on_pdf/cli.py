import click
from pathlib import Path
from tqdm import tqdm
from make_space_for_notes_on_pdf.add_margins import add_margins


@click.command()
@click.argument(
    "input_file_or_dir",
    type=click.Path(exists=True, dir_okay=True, file_okay=True, path_type=Path),
)
@click.option(
    "--left",
    type=float,
    default=150,
    help="Left margin in points or relative (default: 0)",
)
@click.option(
    "--right",
    type=float,
    default=150,
    help="Right margin in points or relative (default: 0)",
)
@click.option(
    "--top", type=float, default=0, help="Top margin in points or relative (default: 0)"
)
@click.option(
    "--bottom",
    type=float,
    default=0,
    help="Bottom margin in points or relative (default: 0)",
)
@click.option("--force", is_flag=True, help="Force overwrite of existing files")
@click.option(
    "--force-relative",
    is_flag=True,
    help="Force to interpret margins as relative margins",
)
def cli(
    input_file_or_dir: Path,
    left: float,
    right: float,
    top: float,
    bottom: float,
    force: bool = False,
    force_relative: bool = False,
):
    # Check if the input is a file or a directory
    file = input_file_or_dir

    # If it's a file, apply margins and add blank pages to the single file
    if input_file_or_dir.is_file():
        file = input_file_or_dir
        target = file.with_name(f"{file.stem}_margins{file.suffix}")
        add_margins(
            file,
            target,
            left=left,
            right=right,
            top=top,
            bottom=bottom,
            force_relative=force_relative,
        )

    # If it's a directory, recursively process all PDFs in the directory
    else:
        # Collect all PDF files in the directory, excluding files already processed
        files = [
            f for f in input_file_or_dir.rglob("*.pdf") if "_margins" not in file.stem
        ]

        # Progress bar to track processing of multiple files
        for file in tqdm(files):
            if "_margins" in file.stem:
                continue
            target = file.with_name(f"{file.stem}_margins{file.suffix}")
            add_margins(
                file,
                target,
                left=left,
                right=right,
                top=top,
                bottom=bottom,
                force_relative=force_relative,
            )


# Entry point to the script
if __name__ == "__main__":
    cli()  # Invoke the CLI command
