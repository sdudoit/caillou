from __future__ import annotations

import json
from importlib import resources as impresources
from typing import Any

import clipboard as cb
from textual.app import App, ComposeResult, on
from textual.binding import Binding
from textual.widgets import Button, Footer, Select, Static, TextArea
from textual.widgets._select import NoSelection


class CustomTextArea(TextArea):

    BINDINGS = [
        Binding("ctrl+a", "select_all", "Select All", show=False, priority=True)
    ]


class LanguageSelector(Select):

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
        with languages_file.open("rt") as f:
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
    """Translate a text into a target language"""

    TITLE = "Caillou Translate"

    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
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
        # Give the input focus, so we can start typing straight away
        self.query_one("#input_text", expect_type=TextArea).focus()

    @on(Button.Pressed, "#translate_button")
    def translate(self) -> None:
        from langchain.chains.llm import LLMChain
        from langchain.prompts import PromptTemplate
        from langchain_openai.llms import OpenAI

        input_text = self.query_one("#input_text", expect_type=TextArea).text
        if input_text.strip():
            language = self.query_one("#language_selector", expect_type=Select).value

            prompt = PromptTemplate(
                input_variables=["language", "input_text"],
                template="Could you translate in the language {language} the following text: {input_text}",
            )
            chain = LLMChain(llm=OpenAI(), prompt=prompt)

            output_textarea = self.query_one("#output_text", expect_type=TextArea)
            output_textarea.clear()
            output_textarea.insert("Translating ...")
            response = chain.invoke(
                input={"language": language, "input_text": input_text}
            )
            output_textarea.clear()
            output_textarea.insert(response["text"].lstrip("\n"))

    @on(Button.Pressed, "#copy_button")
    def copy(self) -> None:
        cb.copy(self.query_one("#output_text", expect_type=TextArea).text)

    @on(Button.Pressed, "#paste_button")
    def paste(self) -> None:
        input_textarea = self.query_one("#input_text", expect_type=TextArea)
        input_textarea.clear()
        input_textarea.insert(cb.paste())


if __name__ == "__main__":
    app = TranslatorApp()
    app.run()
