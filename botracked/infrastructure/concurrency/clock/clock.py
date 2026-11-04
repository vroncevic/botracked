# -*- coding: UTF-8 -*-

'''
Module
    clock.py
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
    Defines Clock adapter wrapping stdlib monotonic and epoch time sources.
'''

from __future__ import annotations

from time import monotonic as stdlib_monotonic, time as stdlib_time

from ats_utilities.utils.reflection import to_str

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Clock:
    '''
        Defines class Clock implementing IClock contract structurally.
        Provides monotonic and wall-clock timestamps via Python stdlib time.

        It defines:

            :attributes: None.
            :methods:
                | __init__ - Initializes system clock adapter instance.
                | monotonic - Returns current monotonic timestamp in seconds.
                | now - Returns current epoch wall-clock timestamp in seconds.
                | __str__ - Returns string representation of adapter.
    '''

    def __init__(self) -> None:
        '''
            Initializes system clock adapter instance.

            :exceptions: None.
        '''

    def monotonic(self) -> float:
        '''
            Returns current monotonic timestamp in seconds.

            :return: Monotonic timestamp in seconds.
            :exceptions: None.
        '''
        return stdlib_monotonic()

    def now(self) -> float:
        '''
            Returns current epoch wall-clock timestamp in seconds.

            :return: Wall-clock timestamp in seconds.
            :exceptions: None.
        '''
        return stdlib_time()

    def __str__(self) -> str:
        '''
            Returns string representation of Clock adapter.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
