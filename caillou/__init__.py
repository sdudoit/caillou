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

    response = chain.invoke(
        input={"language": language, "input_text": " ".join(input_text)}
    )
    print(f"{response['text'].lstrip('\n')}")


@main.group
def roll() -> None:
    """Launch an application"""
    pass


@roll.command
def translator() -> None:
    """
    Translator application in the terminal to support more complex use-cases
    """
    from caillou.translate.translator import TranslatorApp

    app = TranslatorApp()
    app.run()
