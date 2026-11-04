# -*- coding: UTF-8 -*-

'''
Module
    iraw_queue_test.py
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
    Unit tests for IRawByteQueue structural protocol contract.
'''

from __future__ import annotations

from queue import Queue
from unittest import TestCase, main

from botracked.infrastructure.connection.buffer.iraw_queue import IRawByteQueue

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RawByteQueueProtocolTest(TestCase):
    '''
        Verifies runtime structural subtyping of IRawByteQueue over Queue.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies stdlib Queue satisfies IRawByteQueue and object does not.

            :exceptions: None.
        '''
        raw_q: Queue[bytes] = Queue()
        self.assertIsInstance(raw_q, IRawByteQueue)
        self.assertNotIsInstance(object(), IRawByteQueue)


if __name__ == '__main__':
    main()
