# -*- coding: UTF-8 -*-

'''
Module
    byte_queue_test.py
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
    Unit tests for ByteQueue FIFO adapter over IRawByteQueue.
'''

from __future__ import annotations

from queue import Empty, Queue
from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.exceptions.queue_empty_error import QueueEmptyError
from botracked.infrastructure.connection.buffer.byte_queue import ByteQueue
from botracked.infrastructure.connection.buffer.iraw_queue import IRawByteQueue

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ByteQueueTest(TestCase):
    '''
        Verifies ByteQueue enqueue, dequeue timeout, clear, and is_empty.
    '''

    def test_enqueue_dequeue_clear_and_str(self) -> None:
        '''
            Verifies full FIFO cycle and timeout behavior over stdlib Queue.

            :exceptions: None.
        '''
        raw_q: Queue[bytes] = Queue()
        adapter = ByteQueue(raw_queue=raw_q)

        self.assertTrue(adapter.is_empty())
        with self.assertRaises(QueueEmptyError):
            adapter.dequeue(0.001)

        adapter.enqueue(b'\x01')
        adapter.enqueue(b'\x02')
        self.assertFalse(adapter.is_empty())
        self.assertEqual(adapter.dequeue(0.01), b'\x01')

        adapter.clear()
        self.assertTrue(adapter.is_empty())
        self.assertIn('ByteQueue', str(adapter))

    def test_clear_handles_concurrent_empty_race(self) -> None:
        '''
            Verifies clear exits gracefully if get_nowait raises Empty.

            :exceptions: None.
        '''
        mock_q = Mock(spec=IRawByteQueue)
        mock_q.empty.return_value = False
        mock_q.get_nowait.side_effect = Empty()
        adapter = ByteQueue(raw_queue=mock_q)
        adapter.clear()
        mock_q.get_nowait.assert_called_once()


if __name__ == '__main__':
    main()
