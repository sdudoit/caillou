import click
from pathlib import Path

@click.group
def main():
    """AI Assistant in the Command-Line"""
    pass

@main.command
@click.argument("PDF_FILE", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def discuss(pdf_file: Path) -> None:
    """
    Discuss about the given PDF file

    \b
    PDF_FILE    PDF file where the AI Assistant must look for information
    """
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    # Load PDF and split in chunks of text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )    
    loader = PyPDFLoader(pdf_file)
    chunks = loader.load_and_split(text_splitter)

    for chunk in chunks:
        chunk.metadata = {
            "page": chunk.metadata["page"],
            "text": chunk.page_content,
            "pdf_name": pdf_file.name
        }
        print(chunk.metadata["page"], chunk.metadata["pdf_name"])


    # Store PDF split in Vector DB


 
