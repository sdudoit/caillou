import json
from unittest.mock import MagicMock

import pytest

from caillou.translate import Translator

CONFIG_SAMPLE_CONTENT = """
{
    "llms": {
        "openai-gpt-3.5-turbo": {
            "type": "langchain_openai.llms.OpenAI",
            "config": {
                "api_key": "MY_OPENAI_API_KEY",
                "model": "gpt-3.5-turbo-instruct",
                "temperature": 0.0
            }
        },
        "ollama-llama2": {
            "type": "langchain_community.llms.ollama.Ollama",
            "config": {
                "model": "llama2",
                "temperature": 0.0
            }
        },
        "ollama-llama3": {
            "type": "langchain_community.llms.ollama.Ollama",
            "config": {
                "model": "llama3",
                "temperature": 0.0
            }
        }
    },
    "services": {
        "translate": {
            "llm": "openai-gpt-3.5-turbo"
        }
    }
}
"""


@pytest.fixture
def translator():
    config = json.loads(CONFIG_SAMPLE_CONTENT)
    return Translator(config)


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
