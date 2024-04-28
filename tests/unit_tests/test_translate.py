from unittest.mock import MagicMock

import pytest

from caillou.translate import BaseTranslator, OpenAITranslator


@pytest.fixture
def base_translator():
    llm = MagicMock()
    return BaseTranslator(llm, "Template")


def test_base_translator_init(base_translator):
    assert base_translator.llm == MagicMock()
    assert base_translator.prompt_template == "Template"


def test_translate_raises_on_empty_language(base_translator):
    with pytest.raises(ValueError):
        base_translator.translate("", "text")


def test_translate_raises_on_empty_text(base_translator):
    with pytest.raises(ValueError):
        base_translator.translate("en", "")


def test_translate_calls_chain_invoke(base_translator):
    base_translator.translate("en", "Hello")
    base_translator.chain.invoke.assert_called_with({"language": "en", "input_text": "Hello"})


def test_openai_translator_init():
    translator = OpenAITranslator("key")
    assert (
        translator.prompt_template == "Could you translate in the language {language} the following text: {input_text}"
    )


if __name__ == "__main__":
    pytest.main()
