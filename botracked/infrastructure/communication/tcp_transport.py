# -*- coding: UTF-8 -*-

'''
Module
    tcp_transport.py
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
    Provides TcpTransport adapter for wireless socket communication via ESP8266.
'''

from __future__ import annotations

from socket import (
    AF_INET,
    SHUT_RDWR,
    SOCK_STREAM,
    error as SocketError,
    socket,
)

from botracked.core.model.connection_params import ConnectionParams

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TcpTransport:
    '''
        Defines class TcpTransport with attribute(s) and method(s).
        Wireless TCP client transport adapter connecting to ESP8266 WiFi bridge.

        It defines:

            :attributes:
                | _socket - Active TCP socket instance or None.
                | _is_connected - Boolean flag tracking connected state.
            :methods:
                | __init__ - Initializes TCP transport in disconnected state.
                | connect - Connects TCP socket to remote robot IP and port.
                | disconnect - Shuts down and closes active TCP socket.
                | is_connected - Checks if TCP connection is active.
                | send - Sends bytes through TCP socket.
                | write - Sends bytes through TCP socket (alias).
                | receive - Reads incoming bytes from TCP socket.
    '''

    _socket: socket | None
    _is_connected: bool

    def __init__(self) -> None:
        '''
            Initializes TCP transport in disconnected state.

            :exceptions: None.
        '''
        self._socket = None
        self._is_connected = False

    def connect(self, params: ConnectionParams) -> bool:
        '''
            Connects TCP socket to remote robot IP and port.

            :param params: Connection parameters.
            :return: True if connected successfully, False otherwise.
            :exceptions: None.
        '''
        self.disconnect()
        try:
            sock: socket = socket(AF_INET, SOCK_STREAM)
            sock.settimeout(params.timeout)
            sock.connect((params.tcp_host, params.tcp_port))
            # Set non-blocking/short timeout for asynchronous polling
            sock.settimeout(0.05)
            self._socket = sock
            self._is_connected = True
            return True
        except (SocketError, OSError):
            self.disconnect()
            return False

    def disconnect(self) -> None:
        '''
            Shuts down and closes active TCP socket.

            :exceptions: None.
        '''
        if self._socket is not None:
            try:
                self._socket.shutdown(SHUT_RDWR)
            except (SocketError, OSError):
                pass
            try:
                self._socket.close()
            except (SocketError, OSError):
                pass
            finally:
                self._socket = None
        self._is_connected = False

    def is_connected(self) -> bool:
        '''
            Checks if TCP connection is currently active.

            :return: True if connected, False otherwise.
            :exceptions: None.
        '''
        return self._is_connected and self._socket is not None

    def send(self, data: bytes) -> bool:
        '''
            Sends bytes through TCP socket.

            :param data: Byte sequence to transmit.
            :return: True if all bytes sent, False on error.
            :exceptions: None.
        '''
        if not self.is_connected() or self._socket is None:
            return False
        try:
            self._socket.sendall(data)
            return True
        except (SocketError, OSError):
            self.disconnect()
            return False

    def write(self, data: bytes) -> bool:
        '''
            Sends bytes through TCP socket (alias for send).

            :param data: Byte sequence to transmit.
            :return: True if all bytes sent, False on error.
            :exceptions: None.
        '''
        return self.send(data)

    def receive(self, max_bytes: int = 1024) -> bytes:
        '''
            Reads incoming bytes from TCP socket.

            :param max_bytes: Maximum byte count to receive.
            :return: Bytes received, or empty bytes on timeout.
            :exceptions: None.
        '''
        if not self.is_connected() or self._socket is None:
            return b''
        try:
            return self._socket.recv(max_bytes)
        except TimeoutError:
            return b''
        except (SocketError, OSError):
            self.disconnect()
            return b''
