# -*- coding: UTF-8 -*-

'''
Module
    task_test.py
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
    Unit tests for ReceptionTask FIFO byte buffering and error handling.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.exceptions.connection_error import BotConnectionError
from botracked.core.model.exceptions.queue_empty_error import QueueEmptyError
from botracked.core.service.connection.buffer.iqueue import IByteQueue
from botracked.core.service.connection.receiver.protocol.ireader import IByteReader
from botracked.core.service.connection.receiver.task import ReceptionTask

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReceptionTaskTest(TestCase):
    '''
        Verifies ReceptionTask execute_step, read_bytes, and cleanup.
    '''

    def test_step_enqueues_data_and_read_bytes_dequeues(self) -> None:
        '''
            Verifies execute_step buffers non-empty chunks and read_bytes dequeues.

            :exceptions: None.
        '''
        reader = Mock(spec=IByteReader)
        reader.read_bytes.side_effect = [b'\xaa\xbb', b'', BotConnectionError('err')]
        queue = Mock(spec=IByteQueue)
        queue.dequeue.side_effect = [b'\xaa\xbb', QueueEmptyError('empty')]
        queue.is_empty.return_value = False
        task = ReceptionTask(reader=reader, queue=queue, buffer_size=256)

        self.assertTrue(task.has_pending())
        self.assertTrue(task.execute_step())
        queue.enqueue.assert_called_once_with(b'\xaa\xbb')

        self.assertTrue(task.execute_step())
        self.assertEqual(queue.enqueue.call_count, 1)

        self.assertFalse(task.execute_step())
        self.assertEqual(task.read_bytes(0.05), b'\xaa\xbb')
        with self.assertRaises(QueueEmptyError):
            task.read_bytes(0.05)

        task.cleanup()
        queue.clear.assert_called_once()


if __name__ == '__main__':
    main()
