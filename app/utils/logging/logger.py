import logging

from app.utils.configuration.config_holder import ConfigHolder


class Logger:

    @classmethod
    def set_up(cls):
        handlers = []

        """ 
        If we wanted to do something like UDP logging for prod (or a different env), this would 
        be the place to set the handler by adding it to the list of handlers. 
        For this exercise it feels a bit out of scope, so we're sticking to the console logger. 
        See https://docs.python.org/3/library/logging.handlers.html#datagramhandler.
        """

        handlers.append(logging.StreamHandler())
        # Configure
        logging.basicConfig(
            format=ConfigHolder.config().get('logging.format_string'),
            level=logging.getLevelName(ConfigHolder.config().get('logging.min_logging_level')),
            handlers=handlers)

    def __init__(self, class_name):
        self._logger = logging.getLogger(class_name)

    def info(self, message):
        self._logger.info(message)

    def error(self, message, exc_info=True):
        self._logger.exception(message, exc_info=exc_info)

    def debug(self, message):
        self._logger.debug(message)

    def warning(self, message):
        self._logger.warning(message)