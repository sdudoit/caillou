from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai.llms import OpenAI


class OpenAITranslator:
    """Translator using the OpenAI API"""

    def __init__(self, api_key: str) -> None:
        self.chain = LLMChain(
            llm=OpenAI(api_key=api_key),
            prompt=PromptTemplate(
                input_variables=["language", "input_text"],
                template="Could you translate in the language {language} the following text: {input_text}",
            ),
        )

    def translate(self, language: str, input_text: str) -> str:
        """Translate into the given language the given input text"""
        if not language:
            raise ValueError("Language to use for translation is empty!")
        if not input_text:
            raise ValueError("Input text to translate is empty!")
        return self.chain.invoke(input={"language": language, "input_text": input_text})
