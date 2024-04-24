from __future__ import annotations

import clipboard as cb
from textual.app import App, ComposeResult, on
from textual.binding import Binding
from textual.widgets import Button, Select, Static, TextArea

LANGUAGES = """
Dutch
English
French
German
Italian
""".splitlines()


class CustomTextArea(TextArea):

    BINDINGS = [
        Binding("ctrl+a", "select_all", "Select All", show=False, priority=True)
    ]


class TranslatorApp(App):
    """Translate a text into a target language"""

    TITLE = "Caillou Translate"

    CSS_PATH = "translate.tcss"

    def compose(self) -> ComposeResult:
        yield CustomTextArea(id="input_text")
        yield Button(id="paste_button", label="<< Paste", variant="default")
        yield Button(id="translate_button", label="Translate to", variant="primary")
        yield Select.from_values(
            id="language_selector",
            values=LANGUAGES,
            prompt="Select target language",
            value="French",
        )
        yield Static()
        yield CustomTextArea(id="output_text", read_only=True)
        yield Button(id="copy_button", label="Copy >>", variant="default")

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
        language = self.query_one("#language_selector", expect_type=Select).value

        prompt = PromptTemplate(
            input_variables=["language", "input_text"],
            template="Could you translate in the language {language} the following text: {input_text}",
        )
        chain = LLMChain(llm=OpenAI(), prompt=prompt)

        output_textarea = self.query_one("#output_text", expect_type=TextArea)
        output_textarea.clear()
        output_textarea.insert("Translating ...")
        response = chain.invoke(input={"language": language, "input_text": input_text})
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
