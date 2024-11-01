from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str
    
    LANG: str = 'EN'

    AUTO_TASKS: bool = True
    TASKS_JOIN_TO_CHANNEL: bool = False
    DELAY_GET_TASKS: list[int] = [5, 10]
    DELAY_TASK_COMPLETE: list[int] = [10, 15]
    DELAY_TASK_CLAIM: list[int] = [10, 15]
    BLACKLIST_TASK: list[str] = []
    
    USE_RANDOM_DELAY_IN_RUN: bool = True
    DELAY_ACCOUNT: list[int] = [5, 10]
    DELAY_RELOGIN: list[int] = [5, 10]
    DELAY_RESTARTING: list[int] = [21600, 43200]

    USE_REF: bool = True
    REF_LINK: str = 'https://t.me/PAWSOG_bot/PAWS?startapp=8ppTr9Ft'

    USE_PROXY_FROM_FILE: bool = False


settings = Settings()


