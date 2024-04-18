import click


@click.group
def main():
    """AI Assistant in the Command-Line"""
    pass

@main.command
@click.argument("PDF_FILE")
def discuss(pdf_file) -> None:
    """
    Discuss about the given PDF file

    \b
    PDF_FILE    PDF file where the AI Assistant must look for information
    """
    pass

