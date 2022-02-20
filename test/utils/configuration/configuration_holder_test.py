import os
from os.path import abspath, join, dirname
from unittest import TestCase, mock

from app.utils.configuration.configuration import Configuration
from app.utils.configuration.config_holder import ConfigHolder


class ConfigurationHolderTest(TestCase):

    def setUp(self):
        Configuration.ENV_CONF_FOLDER_PATH = \
            f'{abspath(join(dirname(__file__), "../../"))}/resources/config/env/'
        Configuration.SENSITIVE_CONF_PATH = \
            f'{abspath(join(dirname(__file__), "../../"))}/resources/config/sensitive.conf'

    def test_set_for_env(self):
        ConfigHolder.set_for_env('test')
        self.assertEqual('test_db', ConfigHolder.config().get('database.name'))

    @mock.patch.dict(os.environ, {'ENV': 'test'}, clear=True)
    def test_use_default_env(self):
        self.assertEqual('test_db', ConfigHolder.config().get('database.name'))
