import json

from platformdirs import user_config_path

USE_OPENAI_API_KEY_ENV = "os.environ['OPENAI_API_KEY']"

CONFIG_FILE_NAME = "config.json"

CONFIG_INITIAL_CONTENT = """
{
    "llms": {
        "openai-gpt-3.5-turbo": {
            "type": "openai",
            "config": {
                "api_key": "os.environ['OPENAI_API_KEY']",
                "model": "gpt-3.5-turbo-instruct",
                "temperature": 0.0
            }
        },
        "ollama-llama2": {
            "type": "ollama-llm",
            "config": {
                "model": "llama2"
            }
        },
        "ollama-llama3": {
            "type": "ollama-llm",
            "config": {
                "model": "llama3"
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


def load_config() -> dict:
    """Load an existing configuration or create one if not exists"""
    config_dir = user_config_path(__package__)
    if not config_dir.exists():
        print(f"Creating config in: {config_dir}")
        config_dir.mkdir(parents=True)
    config_file = config_dir / CONFIG_FILE_NAME
    if not config_file.exists():
        print(f"Initializing config in: {config_file}")
        with open(config_file, "wt") as f:
            f.write(CONFIG_INITIAL_CONTENT)
    with open(config_file) as f:
        content = f.read()
        # If using environment variable in config, replace it with actual value
        if USE_OPENAI_API_KEY_ENV in content:
            import os

            content = content.replace(USE_OPENAI_API_KEY_ENV, os.environ["OPENAI_API_KEY"])
        return json.loads(content)
