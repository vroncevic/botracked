# -*- coding: UTF-8 -*-

'''
Module
    ilistener.py
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
    Defines ILogListener protocol for GUI console diagnostic log entries.
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
class ILogListener(Protocol):
    '''
        Defines structural contract ILogListener for console diagnostic logging.

        It defines:

            :methods:
                | write_entry - Appends severity-tagged message to console.
                | clear - Clears accumulated diagnostic stream entries.
    '''

    def write_entry(self, level: str, message: str) -> None:
        '''
            Appends severity-tagged message to console log stream.

            :param level: Severity tag string (INFO, WARN, ERROR).
            :param message: Human-readable diagnostic message.
        '''

    def clear(self) -> None:
        '''
            Clears accumulated diagnostic stream entries.
        '''
