# -*- coding: UTF-8 -*-

'''
Module
    driver.py
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
    Provides SerialDriver synchronized hardware adapter implementing ISerialDriver.
'''

from __future__ import annotations

from botracked.infrastructure.connection.driver.ilock import IPortLock
from botracked.infrastructure.connection.driver.iraw_control import IRawSerialControl
from botracked.infrastructure.connection.driver.iraw_io import IRawSerialIO

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialDriver:
    '''
        Defines class SerialDriver implementing ISerialDriver structurally.
        Synchronizes low-level serial access across control and I/O operations.

        It defines:

            :attributes:
                | _control - Raw serial lifecycle control port.
                | _io - Raw serial byte I/O port.
                | _lock - Shared reentrant lock port.
            :methods:
                | __init__ - Initializes driver with control, I/O, and lock ports.
                | open_port - Configures and opens physical serial port under lock.
                | close_port - Closes active physical serial port under lock.
                | is_open - Checks whether serial port is currently open.
                | read_chunk - Reads raw byte chunk from open serial port.
                | write_chunk - Writes and flushes raw byte chunk under lock.
    '''

    _control: IRawSerialControl
    _io: IRawSerialIO
    _lock: IPortLock

    def __init__(
        self,
        *,
        control: IRawSerialControl,
        io: IRawSerialIO,
        lock: IPortLock,
    ) -> None:
        '''
            Initializes driver with control, I/O, and shared lock interfaces.

            :param control: Raw serial lifecycle control interface.
            :param io: Raw serial byte I/O interface.
            :param lock: Shared reentrant lock interface.
            :exceptions: None.
        '''
        self._control = control
        self._io = io
        self._lock = lock

    def open_port(self, port_name: str, baudrate: int) -> bool:
        '''
            Configures and opens physical serial port under lock.

            :param port_name: System serial port identifier.
            :param baudrate: Communication speed in bauds.
            :return: True if port opened successfully, False otherwise.
            :exceptions: None.
        '''
        self._lock.acquire()
        try:
            return self._control.open(port_name, baudrate)
        finally:
            self._lock.release()

    def close_port(self) -> None:
        '''
            Closes active physical serial port under lock.

            :exceptions: None.
        '''
        self._lock.acquire()
        try:
            self._control.close()
        finally:
            self._lock.release()

    def is_open(self) -> bool:
        '''
            Checks whether serial port is currently open.

            :return: True if open, False otherwise.
            :exceptions: None.
        '''
        return self._control.is_open()

    def read_chunk(self, max_size: int) -> bytes:
        '''
            Reads raw byte chunk from open serial port.

            :param max_size: Maximum number of bytes to read.
            :return: Received byte sequence.
            :exceptions: None.
        '''
        return self._io.read(max_size)

    def write_chunk(self, data: bytes) -> int:
        '''
            Writes and flushes raw byte chunk under lock.

            :param data: Raw byte chunk to transmit.
            :return: Number of bytes written.
            :exceptions: None.
        '''
        self._lock.acquire()
        try:
            written: int = self._io.write(data)
            self._io.flush()
            return written
        finally:
            self._lock.release()
