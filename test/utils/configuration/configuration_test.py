from os.path import abspath, join, dirname
from unittest import TestCase

from app.model.errors.invalid_configuration_key_error import InvalidConfigurationKeyError
from app.utils.configuration.configuration import Configuration


class ConfigurationTest(TestCase):

    def setUp(self):
        Configuration.ENV_CONF_FOLDER_PATH = \
            f'{abspath(join(dirname(__file__), "../../"))}/resources/config/env/'
        Configuration.SENSITIVE_CONF_PATH = \
            f'{abspath(join(dirname(__file__), "../../"))}/resources/config/sensitive.conf'
        self.config = Configuration(env='test')

    def test_read_value(self):
        self.assertEqual('test_db', self.config.get('database.name'))

    def test_env_file_not_present(self):
        self.config = Configuration('missing')
        # The empty value is the default value in the global config
        self.assertEqual('', self.config.get('database.name'))

    def test_read_with_default(self):
        self.assertEqual('Hello World!', self.config.get('invalidKey', 'Hello World!'))

    def test_read_value_not_present(self):
        with self.assertRaises(InvalidConfigurationKeyError) as context:
            self.config.get('invalid_key')
        self.assertTrue('Failed to read' in context.exception.message)

    def test_sensitive_conf(self):
        config = Configuration(env='test')
        self.assertEqual('fakeSecret', config.get('app.secret'))
