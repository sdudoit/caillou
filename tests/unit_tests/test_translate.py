from unittest.mock import MagicMock

import pytest

from caillou.translate import OpenAITranslator


@pytest.fixture
def translator():
    return OpenAITranslator("API_KEY")


def test_init(translator):
    assert translator.chain is not None


def test_translate_no_language(translator):
    with pytest.raises(ValueError) as exc_info:
        translator.translate("", "hello")
    assert str(exc_info.value) == "Language to use for translation is empty!"


def test_translate_no_text(translator):
    with pytest.raises(ValueError) as exc_info:
        translator.translate("en", "")
    assert str(exc_info.value) == "Input text to translate is empty!"


def test_translate(translator):
    translator.chain = MagicMock()
    translator.chain.invoke = MagicMock(return_value="bonjour")
    result = translator.translate("fr", "hello")
    assert result == "bonjour"


if __name__ == "__main__":
    pytest.main()
