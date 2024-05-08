from __future__ import annotations

import json
from importlib import resources as impresources
from typing import Any

import pyperclip
from textual.app import App, ComposeResult, on
from textual.binding import Binding
from textual.widgets import Button, Footer, Header, Select, Static, TextArea
from textual.widgets._select import NoSelection

from caillou.config import load_config
from caillou.translate import Translator


class CustomTextArea(TextArea):
    """Custom TextArea to add custom bindings"""

    BINDINGS = [Binding("ctrl+a", "select_all", "Select All", show=False, priority=True)]


class LanguageSelector(Select["str"]):
    """Custom Select for languages"""

    def __init__(
        self,
        *,
        prompt: str = "Select",
        allow_blank: bool = True,
        value: Any | NoSelection = ...,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ):
        languages_file = impresources.files(__package__) / "languages.json"
        with languages_file.open() as f:
            doc = json.load(f)

        languages = [(x["name"], x["name"]) for x in doc.values()]
        super().__init__(
            options=languages,
            prompt=prompt,
            allow_blank=allow_blank,
            value=value,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )


class TranslatorApp(App):
    """Translator Application"""

    CSS_PATH = "styles.tcss"

    def __init__(self, translator: Translator):
        super().__init__()
        self.translator = translator
        self.title = f"TranslatorApp using LLM: {self.translator.llm_id}"

    def compose(self) -> ComposeResult:
        """Compose the UI"""
        yield Header()
        yield CustomTextArea(id="input_text")
        yield Button(id="paste_button", label="<< Paste", variant="default")
        yield Button(id="translate_button", label="Translate to", variant="primary")
        yield LanguageSelector(
            id="language_selector",
            prompt="Select target language",
            value="French",
        )
        yield Static()
        yield CustomTextArea(id="output_text", read_only=True)
        yield Button(id="copy_button", label="Copy >>", variant="default")
        yield Footer()

    def on_mount(self) -> None:
        """Called when app starts."""
        self.query_one("#input_text", expect_type=TextArea).focus()

    @on(Button.Pressed, "#translate_button")
    def translate(self) -> None:
        language = self.query_one("#language_selector", expect_type=Select).value
        input_text = self.query_one("#input_text", expect_type=TextArea).text
        if input_text.strip() and language:
            response = self.translator.translate(str(language), input_text)
            output_textarea = self.query_one("#output_text", expect_type=TextArea)
            output_textarea.clear()
            output_textarea.insert(response)

    @on(Button.Pressed, "#copy_button")
    def copy(self) -> None:
        pyperclip.copy(self.query_one("#output_text", expect_type=TextArea).text)

    @on(Button.Pressed, "#paste_button")
    def paste(self) -> None:
        input_textarea = self.query_one("#input_text", expect_type=TextArea)
        input_textarea.clear()
        input_textarea.insert(pyperclip.paste())


def main() -> None:
    config = load_config()
    app = TranslatorApp(Translator(config))
    app.run()


if __name__ == "__main__":
    main()
