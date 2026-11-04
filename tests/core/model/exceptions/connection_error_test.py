# -*- coding: UTF-8 -*-

'''
Module
    connection_error_test.py
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
    Unit tests for BotConnectionError domain exception.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.model.exceptions.botracked_error import BotrackedError
from botracked.core.model.exceptions.connection_error import BotConnectionError

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotConnectionErrorTest(TestCase):
    '''
        Tests BotConnectionError exception hierarchy and message formatting.
    '''

    def test_raise_and_hierarchy(self) -> None:
        '''
            Verifies BotConnectionError subclasses BotrackedError and preserves message.

            :exceptions: None.
        '''
        err = BotConnectionError('connection_error failure')
        self.assertIsInstance(err, BotrackedError)
        self.assertEqual(str(err), 'connection_error failure')


if __name__ == '__main__':
    main()
