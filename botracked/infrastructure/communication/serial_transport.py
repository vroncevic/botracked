# -*- coding: UTF-8 -*-

'''
Module
    serial_transport.py
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
    Provides SerialTransport adapter using pySerial for USB communication.
'''

from __future__ import annotations

from serial import Serial, SerialException
from serial.tools.list_ports import comports

from botracked.core.model.connection_params import ConnectionParams

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialTransport:
    '''
        Defines class SerialTransport with attribute(s) and method(s).
        Hardware serial port transport adapter for ATmega328P via USB-UART bridge.

        It defines:

            :attributes:
                | _serial - Active pySerial Serial instance or None.
            :methods:
                | __init__ - Initializes serial transport in disconnected state.
                | list_available_ports - Scans system for available serial ports.
                | connect - Opens serial port according to parameters.
                | disconnect - Closes active serial connection.
                | is_connected - Checks if serial port is open and active.
                | send - Transmits raw bytes over serial interface.
                | write - Transmits raw bytes over serial interface (alias).
                | receive - Reads incoming bytes from serial buffer.
    '''

    _serial: Serial | None

    def __init__(self) -> None:
        '''
            Initializes serial transport in disconnected state.

            :exceptions: None.
        '''
        self._serial = None

    @classmethod
    def list_available_ports(cls) -> list[str]:
        '''
            Scans system for available serial ports.

            :return: List of device port paths (e.g. ['/dev/ttyUSB0']).
            :exceptions: None.
        '''
        return [port.device for port in comports()]

    def connect(self, params: ConnectionParams) -> bool:
        '''
            Opens serial port according to connection parameters.

            :param params: Connection configuration.
            :return: True if successfully connected, False otherwise.
            :exceptions: None.
        '''
        self.disconnect()
        try:
            self._serial = Serial(
                port=params.serial_port,
                baudrate=params.baud_rate,
                timeout=params.timeout,
                write_timeout=params.timeout,
            )
            return self._serial.is_open
        except (SerialException, OSError):
            self._serial = None
            return False

    def disconnect(self) -> None:
        '''
            Closes active serial connection.

            :exceptions: None.
        '''
        if self._serial is not None:
            try:
                if self._serial.is_open:
                    self._serial.close()
            except (SerialException, OSError):
                pass
            finally:
                self._serial = None

    def is_connected(self) -> bool:
        '''
            Checks if serial port is open and active.

            :return: True if connected, False otherwise.
            :exceptions: None.
        '''
        return self._serial is not None and self._serial.is_open

    def send(self, data: bytes) -> bool:
        '''
            Transmits raw bytes over serial interface.

            :param data: Byte sequence to write.
            :return: True if all bytes written, False on error.
            :exceptions: None.
        '''
        if not self.is_connected() or self._serial is None:
            return False
        try:
            written: int = self._serial.write(data)
            self._serial.flush()
            return written == len(data)
        except (SerialException, OSError):
            self.disconnect()
            return False

    def write(self, data: bytes) -> bool:
        '''
            Transmits raw bytes over serial interface (alias for send).

            :param data: Byte sequence to write.
            :return: True if all bytes written, False on error.
            :exceptions: None.
        '''
        return self.send(data)

    def receive(self, max_bytes: int = 1024) -> bytes:
        '''
            Reads incoming bytes from serial buffer.

            :param max_bytes: Maximum byte count to read.
            :return: Bytes read from port.
            :exceptions: None.
        '''
        if not self.is_connected() or self._serial is None:
            return b''
        try:
            waiting: int = self._serial.in_waiting
            if waiting > 0:
                count: int = min(waiting, max_bytes)
                return self._serial.read(count)
            return b''
        except (SerialException, OSError):
            self.disconnect()
            return b''
