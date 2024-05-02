from abc import ABC, abstractmethod

from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai.llms import OpenAI
from pydantic import BaseModel


class BaseTranslator(ABC):
    """Abstract class representing a translator"""

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


class OpenAITranslatorConfig(BaseModel):
    api_key: str

    model: str

    temperature: float


class OpenAITranslator(BaseTranslator):
    """Translator using the OpenAI API"""

    INPUTS = ["language", "input_text"]

    PROMPT_TEMPLATE = "Could you translate in the language {language} the following text: {input_text}"

    def __init__(self, config: OpenAITranslatorConfig) -> None:
        self.config = config
        super().__init__()

    def _create_chain(self) -> None:
        return LLMChain(
            llm=OpenAI(**self.config.model_dump()),
            prompt=PromptTemplate(
                input_variables=OpenAITranslator.INPUTS,
                template=OpenAITranslator.PROMPT_TEMPLATE,
            ),
        )


class TranslatorFactory:
    """Factory to create the appropriate Translator based on the provided configuration"""

    @classmethod
    def create(cls, config: BaseModel) -> BaseTranslator:
        match config:
            case OpenAITranslatorConfig():
                return OpenAITranslator(config)
            case _:
                raise Exception("Unknown configuration type provided")
