# -*- coding: UTF-8 -*-

'''
Module
    ireceiver_test.py
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
    Unit tests for IByteReceiver structural protocol contract.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.connection.buffer.iqueue import IByteQueue
from botracked.core.service.connection.receiver.protocol.ireader import IByteReader
from botracked.core.service.connection.receiver.protocol.ireceiver import IByteReceiver
from botracked.core.service.connection.receiver.task import ReceptionTask

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ByteReceiverProtocolTest(TestCase):
    '''
        Verifies runtime structural subtyping of IByteReceiver.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies ReceptionTask satisfies IByteReceiver and object does not.

            :exceptions: None.
        '''
        task = ReceptionTask(
            reader=Mock(spec=IByteReader),
            queue=Mock(spec=IByteQueue),
            buffer_size=1024,
        )
        self.assertIsInstance(task, IByteReceiver)
        self.assertNotIsInstance(object(), IByteReceiver)


if __name__ == '__main__':
    main()
