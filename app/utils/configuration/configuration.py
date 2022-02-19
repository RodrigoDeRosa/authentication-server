from dataclasses import dataclass
from os.path import abspath, join, dirname
from typing import ClassVar

from pyhocon import ConfigFactory, ConfigTree, ConfigException, UndefinedKey

from app.model.errors.invalid_configuration_key_error import InvalidConfigurationKeyError


@dataclass
class Configuration:
    env: str
    __config: ConfigTree = None
    BASE_CONF_FOLDER_PATH: ClassVar[str] = f'{abspath(join(dirname(__file__), "../../../"))}/resources/config/app/'
    ENV_CONF_FOLDER_PATH: ClassVar[str] = f'{abspath(join(dirname(__file__), "../../../"))}/resources/config/env/'
    FILE_NAME: ClassVar[str] = 'application.conf'
    SENSITIVE_CONF_PATH: ClassVar[str] = f'{abspath(join(dirname(__file__), "../../../"))}/sensitive.conf'

    def __post_init__(self):
        config: ConfigTree = ConfigFactory.parse_file(f'{self.BASE_CONF_FOLDER_PATH}{self.FILE_NAME}')

        try:
            env_config: ConfigTree = ConfigFactory.parse_file(f'{self.ENV_CONF_FOLDER_PATH}{self.env}/{self.FILE_NAME}')
            # The environment config has priority over the general config
            config = env_config.with_fallback(config)
        except FileNotFoundError:
            pass

        sensitive_conf: ConfigTree = ConfigFactory.parse_file(self.SENSITIVE_CONF_PATH)
        config = sensitive_conf.with_fallback(config)

        self.__config = config

    def get(self, key: str, default=UndefinedKey) -> object:
        try:
            return self.__config.get(key, default=default)
        except ConfigException:
            raise InvalidConfigurationKeyError(key)
