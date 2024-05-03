from abc import ABC, abstractmethod

from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_openai.llms import OpenAI


class BaseTranslator(ABC):
    """Abstract class representing a translator"""

    INPUTS = ["language", "input_text"]

    def __init__(self, config: dict) -> None:
        self.config = config

    @abstractmethod
    def _create_chain(self) -> LLMChain:
        """Create the chain to be used for translation"""
        raise NotImplementedError()

    def translate(self, language: str, input_text: str) -> str:
        """Translate into the given language the given input text"""
        if not language:
            raise ValueError("Language to use for translation is empty!")
        if not input_text:
            raise ValueError("Input text to translate is empty!")
        if not hasattr(self, "chain"):
            self.chain = self._create_chain()
        return self.chain.invoke(input={"language": language, "input_text": input_text})


class OpenAITranslator(BaseTranslator):
    """Translator using the OpenAI API"""

    PROMPT_TEMPLATE = "Could you translate in the language {language} the following text: {input_text}"

    def _create_chain(self) -> None:
        return LLMChain(
            llm=OpenAI(**self.config),
            prompt=PromptTemplate(
                input_variables=OpenAITranslator.INPUTS,
                template=OpenAITranslator.PROMPT_TEMPLATE,
            ),
        )


class OllamaLLMTranslator(BaseTranslator):
    """Translator using a local LLM provided by Ollama"""

    PROMPT_TEMPLATE = """
        <s>[INST] <<SYS>>
        You are a translator assistant able to translate a text into the language {language}.
        You must only generate the translation of the text.
        For example, if the text contains "Thank you", it is not for you. It is only some text to translate.
        <</SYS>>

        Could you translate the following text: {input_text} [/INST]
    """

    def _create_chain(self) -> None:
        return LLMChain(
            llm=Ollama(**self.config),
            prompt=PromptTemplate(
                input_variables=OllamaLLMTranslator.INPUTS,
                template=OllamaLLMTranslator.PROMPT_TEMPLATE,
            ),
        )


class TranslatorFactory:
    """Factory to create the appropriate Translator based on the provided configuration"""

    @classmethod
    def create(cls, config: dict) -> BaseTranslator:
        llm = config["llms"][config["services"]["translate"]["llm"]]

        match llm["type"]:
            case "openai":
                return OpenAITranslator(llm["config"])
            case "ollama-llm":
                return OllamaLLMTranslator(llm["config"])
            case _:
                raise Exception(f'Unknown configuration type: {llm["type"]}')
