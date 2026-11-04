# -*- coding: UTF-8 -*-

'''
Module
    istorage.py
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
    Defines structural protocol IPreferencesStorage for JSON persistence I/O.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IPreferencesStorage(Protocol):
    '''
        Defines structural contract IPreferencesStorage for key-value JSON files.

        It defines:

            :methods:
                | exists - Checks if persistent storage file currently exists.
                | read_payload - Reads and parses dictionary payload from storage.
                | write_payload - Serializes and writes dictionary payload to storage.
    '''

    def exists(self) -> bool:
        '''
            Checks if persistent storage file currently exists.

            :return: True if storage file exists, False otherwise.
        '''

    def read_payload(self) -> dict[str, object]:
        '''
            Reads and parses dictionary payload from storage.

            :return: Parsed key-value dictionary payload.
        '''

    def write_payload(self, payload: Mapping[str, object]) -> None:
        '''
            Serializes and writes dictionary payload to storage.

            :param payload: Mapping of preference keys to primitive values.
        '''
