import os

from app.utils.configuration.configuration import Configuration


class ConfigHolder:
    """
    Having configuration wrapped like this allows us to reload configuration on runtime if
    we change the configuration files on the server.
    Nevertheless, it's not recommended to change the configuration files themselves but
    create some override file and make the configuration smart enough to also read those;
    it's not a big change but it's out of scope here.
    """

    __config: Configuration = None
    __DEFAULT_ENV = 'dev'

    @classmethod
    def set_for_env(cls, env: str):
        cls.__config = Configuration(env)

    @classmethod
    def config(cls) -> Configuration:
        if not cls.__config:
            cls.set_for_env(os.environ.get('ENV', cls.__DEFAULT_ENV))
        return cls.__config
