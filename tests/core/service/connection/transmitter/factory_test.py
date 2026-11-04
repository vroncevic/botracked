# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for service TransmitterFactory subsystem assembly.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.connection.buffer.iqueue import IByteQueue
from botracked.core.service.connection.transmitter.dependencies import TransmitterDependencies
from botracked.core.service.connection.transmitter.factory import TransmitterFactory
from botracked.core.service.connection.transmitter.protocol.itransmitter import IByteTransmitter
from botracked.core.service.connection.transmitter.protocol.iwriter import IByteWriter
from botracked.core.service.connection.worker.task.itask import IWorkerTask

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TransmitterServiceFactoryTest(TestCase):
    '''
        Verifies TransmitterFactory assembly and version reporting.
    '''

    def test_factory_assembly_and_version(self) -> None:
        '''
            Verifies TransmitterFactory exposes transmitter, task, and worker_task.

            :exceptions: None.
        '''
        tx_provisions = TransmitterFactory.create(
            TransmitterDependencies(
                writer=Mock(spec=IByteWriter),
                queue=Mock(spec=IByteQueue),
                timeout=0.05,
            )
        )
        self.assertIsInstance(tx_provisions.transmitter, IByteTransmitter)
        self.assertIsInstance(tx_provisions.worker_task, IWorkerTask)
        self.assertIs(tx_provisions.transmitter, tx_provisions.worker_task)
        self.assertEqual(TransmitterFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
