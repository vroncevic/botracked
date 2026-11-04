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
    Unit tests for TransmissionTask FIFO outbound byte draining and error handling.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.exceptions.connection_error import BotConnectionError
from botracked.core.model.exceptions.queue_empty_error import QueueEmptyError
from botracked.core.service.connection.buffer.iqueue import IByteQueue
from botracked.core.service.connection.transmitter.protocol.iwriter import IByteWriter
from botracked.core.service.connection.transmitter.task import TransmissionTask

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TransmissionTaskTest(TestCase):
    '''
        Verifies TransmissionTask write_bytes, execute_step, and cleanup.
    '''

    def test_enqueue_drain_and_connection_error(self) -> None:
        '''
            Verifies write_bytes enqueues and execute_step drains onto writer safely.

            :exceptions: None.
        '''
        writer = Mock(spec=IByteWriter)
        writer.write_bytes.side_effect = [True, BotConnectionError('write failed')]
        out_queue = Mock(spec=IByteQueue)
        out_queue.dequeue.side_effect = [
            QueueEmptyError('queue empty'),
            b'\x01\x02',
            b'\x03\x04',
        ]
        out_queue.is_empty.return_value = False
        tx_task = TransmissionTask(writer=writer, queue=out_queue, timeout=0.04)

        self.assertTrue(tx_task.has_pending())
        self.assertTrue(tx_task.write_bytes(b'\x01\x02'))
        out_queue.enqueue.assert_called_once_with(b'\x01\x02')

        self.assertTrue(tx_task.execute_step())
        writer.write_bytes.assert_not_called()

        self.assertTrue(tx_task.execute_step())
        writer.write_bytes.assert_called_once_with(b'\x01\x02')

        self.assertFalse(tx_task.execute_step())
        tx_task.cleanup()
        out_queue.clear.assert_called_once()


if __name__ == '__main__':
    main()
