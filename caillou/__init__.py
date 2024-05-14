import click

from caillou.config import load_config


@click.group
def cli() -> None:
    """AI Assistant in the Command-Line"""


@cli.command
def version() -> None:
    """Print current version of the application"""
    import importlib.metadata

    print(importlib.metadata.version(str(__package__)))


@cli.command
@click.argument("LANGUAGE")
@click.argument("INPUT_TEXT", nargs=-1)
def translate(language: str, input_text: tuple | str) -> None:
    """
    Translate a text into another language

    \b
    LANGUAGE     The language used to translate (e.g. "French", "FR", "Nederlands", "Italiano" etc.)
    INPUT_TEXT   The text to translate
    """

    from caillou.translate import Translator

    # Load config
    config = load_config()

    # Create the appropriate Translator according to config
    translator = Translator(config)

    # Use Translator to translate inputs
    response = translator.translate(language, " ".join(input_text))
    print(response)

    # Add Footer
    print(f"\n(Generated with LLM: {translator.llm_id})")


@cli.command
@click.argument("QUESTION", nargs=1)
def query(question: str) -> None:
    """
    Query some information from a Database using natural language

    \b
    QUESTION    The question in natural language
    """
    from operator import itemgetter

    from langchain.chains import create_sql_query_chain
    from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
    from langchain_community.utilities.sql_database import SQLDatabase
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import PromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_openai.chat_models import ChatOpenAI

    connection_string = "postgresql://postgres:mypassword@localhost/dvdrental"

    db = SQLDatabase.from_uri(connection_string)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    query_gen_chain = create_sql_query_chain(llm, db)

    query_exec_tool = QuerySQLDataBaseTool(db=db)

    answer_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

           Question: {question}
           SQL Query: {query}
           SQL Result: {result}
           Answer: """
    )

    rephrase_answer = answer_prompt | llm | StrOutputParser()

    chain = (
        RunnablePassthrough.assign(query=query_gen_chain).assign(result=itemgetter("query") | query_exec_tool)
        | rephrase_answer
    )

    response = chain.invoke({"question": question})
    print(response)


@cli.command
@click.argument("APPLICATION", nargs=1, required=False)
def roll(application: str) -> None:
    """
    Launch an application or list available applications

    \b
    APPLICATION     The name of the application to launch
    """

    from importlib import import_module

    if not application:
        module = import_module("caillou.apps")
        print("Here is a list of available applications:")
        for app in getattr(module, "__all__"):
            print(f" - {app}")
    else:
        try:
            module = import_module(f"{__package__}.apps.{application}.__main__")
        except ImportError:
            raise Exception(f"Cannot load the expected application module: {__package__}.apps.{application}.__main__")

        try:
            func = getattr(module, "main")
        except AttributeError:
            raise Exception(f"Cannot find the expected main function in: {__package__}.apps.{application}.__main__")

        func()
