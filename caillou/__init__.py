import click
from dotenv import load_dotenv
from platformdirs import user_config_path


def load_config() -> None:
    """Load an existing configuration or create one if not exists"""
    config_dir = user_config_path(__package__)
    if not config_dir.exists():
        print(f"Creating config in: {config_dir}")
        config_dir.mkdir(parents=True)
    config_file = config_dir / "config"
    if not config_file.exists():
        openai_api_key = input("Please provide an OPENAI_API_KEY: ")
        with open(config_file, "wt") as f:
            f.write(f"OPENAI_API_KEY={openai_api_key}")
    if not load_dotenv(dotenv_path=config_file):
        raise Exception(f"Could not load config from: {config_file}")


@click.group
def cli():
    """AI Assistant in the Command-Line"""


@cli.command
def version():
    """Print current version of the application"""
    import importlib.metadata

    print(importlib.metadata.version(__package__))


@cli.command
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

    load_config()

    prompt = PromptTemplate(
        input_variables=["language", "input_text"],
        template="Could you translate in the language {language} the following text: {input_text}",
    )
    chain = LLMChain(llm=OpenAI(), prompt=prompt)

    response = chain.invoke(input={"language": language, "input_text": " ".join(input_text)})
    print(f"{response['text'].lstrip('\n')}")


@cli.group
def roll() -> None:
    """Launch an application"""
    pass


@roll.command
def translator() -> None:
    """
    Translator application in the terminal to support more complex use-cases
    """
    from caillou.translate.translator import TranslatorApp

    load_config()
    app = TranslatorApp()
    app.run()
