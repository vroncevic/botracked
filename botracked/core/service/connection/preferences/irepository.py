# -*- coding: UTF-8 -*-

'''
Module
    irepository.py
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
    Defines IConnectionPreferencesRepository driven port for link persistence.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.connection_preference import ConnectionPreference

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IConnectionPreferencesRepository(Protocol):
    '''
        Defines protocol IConnectionPreferencesRepository with method(s).
        Structural port interface for persisting serial connection preferences.

        It defines:

            :methods:
                | has_preference - Checks if saved connection preference exists.
                | load_preference - Loads persisted connection preference record.
                | save_preference - Persists connection preference to storage.
    '''

    def has_preference(self) -> bool:
        '''
            Checks if a persisted connection preference exists.

            :return: True if valid preference storage exists, False otherwise.
        '''

    def load_preference(self) -> ConnectionPreference:
        '''
            Loads previously saved connection preference from storage.

            :return: Persisted ConnectionPreference value object.
        '''

    def save_preference(self, preference: ConnectionPreference) -> bool:
        '''
            Persists connection preference to storage.

            :param preference: Connection preference value object.
            :return: True if persisted successfully, False otherwise.
        '''
