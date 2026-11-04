# -*- coding: UTF-8 -*-

'''
Module
    main_test.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    botracked is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    botracked is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Unit tests for main bootstrap entrypoint.
'''

from __future__ import annotations

from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock, patch

from main import main as run_app

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MainTest(TestCase):
    '''
        Tests tool entrypoint bootstrap flow.
    '''

    @patch('main.BotrackedBundleFactory.create_bundle')
    @patch('main.Botracked')
    def test_main_execution(
        self, mock_engine_cls: MagicMock, mock_factory: MagicMock
    ) -> None:
        '''
            Verifies main bootstraps engine and processes operation.

            :param mock_engine_cls: Mocked engine class.
            :param mock_factory: Mocked bundle factory.
            :exceptions: None.
        '''
        mock_bundle = MagicMock()
        mock_factory.return_value = mock_bundle
        mock_engine = MagicMock()
        mock_engine.process.return_value = True
        mock_engine_cls.return_value = mock_engine

        self.assertTrue(run_app())
        mock_factory.assert_called_once()
        mock_engine_cls.assert_called_once_with(mock_bundle)


if __name__ == '__main__':
    unittest_main()
