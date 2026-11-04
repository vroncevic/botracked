# -*- coding: UTF-8 -*-

'''
Module
    queue_empty_error_test.py
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
    Unit tests for QueueEmptyError domain exception.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.model.exceptions.connection_error import BotConnectionError
from botracked.core.model.exceptions.queue_empty_error import QueueEmptyError

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class QueueEmptyErrorTest(TestCase):
    '''
        Tests QueueEmptyError exception hierarchy and message formatting.
    '''

    def test_raise_and_hierarchy(self) -> None:
        '''
            Verifies QueueEmptyError subclasses BotConnectionError and preserves message.

            :exceptions: None.
        '''
        err = QueueEmptyError('queue is empty')
        self.assertIsInstance(err, BotConnectionError)
        self.assertEqual(str(err), 'queue is empty')


if __name__ == '__main__':
    main()
