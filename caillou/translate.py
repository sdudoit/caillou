from abc import ABC

from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLLM
from langchain_openai.llms import OpenAI


class BaseTranslator(ABC):

    def __init__(self, llm: BaseLLM, prompt_template: str) -> None:
        self.llm = llm
        self.chain = LLMChain(
            llm=OpenAI(),
            prompt=PromptTemplate(
                input_variables=["language", "input_text"],
                template=prompt_template,
            ),
        )

    def translate(self, language: str, input_text: str) -> str:
        """Translate into the given language the given input text"""
        return self.chain.invoke(input={"language": language, "input_text": input_text})


class OpenAITranslator(BaseTranslator):

    def __init__(self, api_key: str) -> None:
        super().__init__(
            OpenAI(api_key=api_key),
            prompt_template="Could you translate in the language {language} the following text: {input_text}",
        )
