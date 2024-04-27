import os

import click

from caillou.config import load_config


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
    from caillou.translate import OpenAITranslator

    load_config()

    translator = OpenAITranslator(api_key=os.environ["OPENAI_API_KEY"])
    response = translator.translate(language, " ".join(input_text))
    print(f"{response['text'].lstrip('\n')}")
