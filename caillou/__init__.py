import click
from dotenv import load_dotenv


@click.group
def main():
    """AI Assistant in the Command-Line"""
    load_dotenv()


@main.command
@click.argument("TO_LANGUAGE")
@click.argument("SENTENCE")
def translate(to_language, sentence) -> None:
    """
    Translate into the given language the given sentence

    \b
    TO_LANGUAGE     The language in which the sentence must be translated (e.g. French, English, Dutch, Italian etc.)
    SENTENCE        The sentence to translate surrounded met quotes (e.g. "This is my sentence to translate")
    """
    from langchain.chains.llm import LLMChain
    from langchain.prompts import PromptTemplate
    from langchain_openai.llms import OpenAI

    prompt = PromptTemplate(
        input_variables=["language", "sentence"],
        template="Could you translate in the language {language} the following sentence: {sentence}",
    )
    chain = LLMChain(llm=OpenAI(), prompt=prompt)

    response = chain.invoke(input={"language": to_language, "sentence": sentence})
    print(f"{response['text']}")


# @main.command
# @click.argument("QUESTION")
# @click.argument(
#     "PDF_FILE", type=click.Path(exists=True, dir_okay=False, path_type=Path)
# )
# def ask(question: str, pdf_file: Path) -> None:
#     """
#     Ask a question about the given PDF file

#     \b
#     QUESTION    A question in natural language
#     \b
#     PDF_FILE    PDF file where the AI Assistant must look for information
#     """
#
#     from langchain.chains import RetrievalQA
#     from langchain.embeddings.base import Embeddings
#     from langchain.schema import BaseRetriever
#     from langchain_community.document_loaders import PyPDFLoader
#     from langchain_community.vectorstores.chroma import Chroma
#     from langchain_openai import ChatOpenAI, OpenAIEmbeddings
#     from langchain_text_splitters import RecursiveCharacterTextSplitter

#     load_dotenv()

#     # Load PDF and split in chunks of text
#     # text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
#     # loader = PyPDFLoader(pdf_file)
#     # chunks = loader.load_and_split(text_splitter)
#     embeddings = OpenAIEmbeddings()

#     # db = Chroma.from_documents(
#     #     chunks,
#     #     embedding=embeddings,
#     #     persist_directory="tests/embeddings"
#     # )

#     class RedundantFilterRetriever(BaseRetriever):
#         embeddings: Embeddings
#         chroma: Chroma

#         def get_relevant_documents(self, query):
#             # calculate embeddings for the 'query' string
#             emb = self.embeddings.embed_query(query)

#             # take embeddings and feed them into that
#             # max_marginal_relevance_search_by_vector
#             return self.chroma.max_marginal_relevance_search_by_vector(
#                 embedding=emb, lambda_mult=0.8
#             )

#         async def aget_relevant_documents(self):
#             return []

#     # Store PDF chunks in Vector DB
#     db = Chroma(persist_directory="tests/embeddings", embedding_function=embeddings)
#     # retriever = RedundantFilterRetriever(embeddings=embeddings, chroma=db)

#     chat = ChatOpenAI()

#     chain = RetrievalQA.from_chain_type(
#         llm=chat, retriever=db.as_retriever(), chain_type="stuff"
#     )

#     result = chain.invoke(question)

#     print(result["result"])

#     # Chroma.from_documents(embedding=embedding)

#     # for index, chunk in enumerate(chunks, start=1):
#     #     chunk.metadata = {
#     #         "page": chunk.metadata["page"],
#     #         "pdf_name": pdf_file.name,
#     #     }
#     #     collection.add(ids=[f"{index}"], metadatas=[chunk.metadata], documents=[chunk.page_content])

#     # # Query
#     # results = collection.query(
#     #     query_texts=["Cornerstone"],
#     #     n_results=3,
#     # )

#     # for r in results.documents:
#     #     print(r)
