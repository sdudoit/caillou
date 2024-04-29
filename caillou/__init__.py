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
def translate(language, input_text) -> None:
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


@cli.command
@click.argument("APPLICATION", nargs=1, required=False)
def launch(application) -> None:
    """
    Launch an application with the given name or list the available applications if no name is provided

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
