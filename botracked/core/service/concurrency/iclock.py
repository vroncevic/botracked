# -*- coding: UTF-8 -*-

'''
Module
    iclock.py
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
    Defines IClock driven port for monotonic and wall-clock time queries.
'''

from __future__ import annotations

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
class IClock(Protocol):
    '''
        Defines structural protocol IClock abstracting time measurements.

        It defines:

            :methods:
                | monotonic - Returns current monotonic clock timestamp in seconds.
                | now - Returns current epoch wall-clock timestamp in seconds.
    '''

    def monotonic(self) -> float:
        '''
            Returns current monotonic clock timestamp in seconds.

            :return: Monotonic timestamp in seconds.
        '''

    def now(self) -> float:
        '''
            Returns current epoch wall-clock timestamp in seconds.

            :return: Wall-clock timestamp in seconds.
        '''
