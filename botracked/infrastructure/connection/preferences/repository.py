# -*- coding: UTF-8 -*-

'''
Module
    repository.py
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
    Provides ConnectionPreferencesRepository over injected IPreferencesStorage.
'''

from __future__ import annotations

from typing import ClassVar

from ats_utilities.utils.reflection import to_str

from botracked.core.model.connection_preference import ConnectionPreference
from botracked.core.model.exceptions.preferences_error import PreferencesError
from botracked.infrastructure.connection.preferences.istorage import IPreferencesStorage

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionPreferencesRepository:
    '''
        Defines class ConnectionPreferencesRepository implementing repository port.
        Validates and maps ConnectionPreference records over IPreferencesStorage.

        It defines:

            :attributes:
                | KEY_PORT - Dictionary key storing serial port device string.
                | KEY_BAUD - Dictionary key storing integer baud rate.
                | MIN_BAUD - Minimum valid positive baud rate threshold.
                | _storage - Low-level key-value JSON storage port.
            :methods:
                | __init__ - Initializes repository with injected storage port.
                | has_preference - Checks if saved connection preference exists.
                | load_preference - Loads persisted connection preference record.
                | save_preference - Persists connection preference to storage.
                | __str__ - Returns string representation of repository.
    '''

    KEY_PORT: ClassVar[str] = 'port'
    KEY_BAUD: ClassVar[str] = 'baud'
    MIN_BAUD: ClassVar[int] = 1
    _storage: IPreferencesStorage

    def __init__(self, storage: IPreferencesStorage) -> None:
        '''
            Initializes repository with injected storage port.

            :param storage: Storage adapter satisfying IPreferencesStorage.
            :exceptions: None.
        '''
        self._storage = storage

    def has_preference(self) -> bool:
        '''
            Checks if a persisted connection preference exists.

            :return: True if preference storage exists, False otherwise.
            :exceptions: None.
        '''
        return self._storage.exists()

    def load_preference(self) -> ConnectionPreference:
        '''
            Loads previously saved connection preference from storage.

            :return: Persisted ConnectionPreference value object.
            :exceptions:
                | PreferencesError: If storage is missing or payload is malformed.
        '''
        payload = self._storage.read_payload()
        if self.KEY_PORT not in payload or self.KEY_BAUD not in payload:
            raise PreferencesError(
                'Persisted preferences payload lacks required keys.'
            )

        raw_port = payload[self.KEY_PORT]
        raw_baud = payload[self.KEY_BAUD]

        if not isinstance(raw_port, str) or not raw_port.strip():
            raise PreferencesError(
                'Persisted serial port identifier must be a non-empty string.'
            )

        if (
            isinstance(raw_baud, bool)
            or not isinstance(raw_baud, int)
            or raw_baud < self.MIN_BAUD
        ):
            raise PreferencesError(
                'Persisted baud rate must be a positive integer.'
            )

        return ConnectionPreference(port=raw_port, baud=raw_baud)

    def save_preference(self, preference: ConnectionPreference) -> bool:
        '''
            Persists connection preference to storage.

            :param preference: Connection preference value object.
            :return: True if persisted successfully, False otherwise.
            :exceptions: None.
        '''
        if not preference.port.strip() or preference.baud < self.MIN_BAUD:
            return False

        try:
            self._storage.write_payload(
                {self.KEY_PORT: preference.port, self.KEY_BAUD: preference.baud}
            )
            return True

        except PreferencesError:
            return False

    def __str__(self) -> str:
        '''
            Returns string representation of repository.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
