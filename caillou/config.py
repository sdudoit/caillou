from dotenv import load_dotenv
from platformdirs import user_config_path


def load_config() -> None:
    """Load an existing configuration or create one if not exists"""
    config_dir = user_config_path(__package__)
    if not config_dir.exists():
        print(f"Creating config in: {config_dir}")
        config_dir.mkdir(parents=True)
    config_file = config_dir / "config"
    if not config_file.exists():
        openai_api_key = input("Please provide an OPENAI_API_KEY: ")
        with open(config_file, "wt") as f:
            f.write(f"OPENAI_API_KEY={openai_api_key}")
    if not load_dotenv(dotenv_path=config_file):
        raise Exception(f"Could not load config from: {config_file}")
