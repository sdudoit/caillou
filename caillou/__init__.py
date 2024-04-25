from pathlib import Path

import click
from dotenv import load_dotenv


@click.group
def main():
    """AI Assistant in the Command-Line"""
    load_dotenv()


@main.command
@click.argument("LANGUAGE")
@click.argument("INPUT_TEXT", nargs=-1)
def tr(language, input_text) -> None:
    """
    Translate a text into another language (e.g. "tr FR This is a rock-solid application")

    \b
    LANGUAGE     The language used to translate (e.g. "French", "FR", "Nederlands", "Italiano" etc.)
    INPUT_TEXT   The text to translate
    """
    from langchain.chains.llm import LLMChain
    from langchain.prompts import PromptTemplate
    from langchain_openai.llms import OpenAI

    prompt = PromptTemplate(
        input_variables=["language", "input_text"],
        template="Could you translate in the language {language} the following text: {input_text}",
    )
    chain = LLMChain(llm=OpenAI(), prompt=prompt)

    response = chain.invoke(input={"language": language, "input_text": input_text})
    print(f"{response['text'].lstrip('\n')}")


@main.command
@click.argument(
    "PDF_FILE", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
@click.argument("QUERY")
def query(pdf_file: Path, query: str) -> None:
    """
    Submit a query in natural language about the content of the given PDF file

    \b
    PDF_FILE    PDF file where the AI Assistant must look for information
    \b
    QUERY       A query in natural language about the content of the PDF File surrounded with quotes
    """

    from tempfile import TemporaryDirectory

    from langchain.chains import RetrievalQA
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_community.vectorstores.chroma import Chroma
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    from .redundant_retriver import RedundantFilterRetriever

    # Load PDF and split in chunks of text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    loader = PyPDFLoader(pdf_file)
    chunks = loader.load_and_split(text_splitter)

    # Define embeddings function to use
    embeddings = OpenAIEmbeddings()

    # Load chunks in DB
    tmp_dir = TemporaryDirectory("caillou")
    db = Chroma.from_documents(
        chunks, embedding=embeddings, persist_directory=tmp_dir.name
    )

    # Create Chain
    retriever = RedundantFilterRetriever(embeddings=embeddings, chroma=db)
    chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(), retriever=retriever, chain_type="stuff"
    )

    # Invoke with query
    response = chain.invoke(query)
    print(response["result"])


@main.group
def roll() -> None:
    """Launch application"""
    pass


@roll.command
def translate() -> None:
    from caillou.translate.translate import TranslatorApp

    app = TranslatorApp()
    app.run()
