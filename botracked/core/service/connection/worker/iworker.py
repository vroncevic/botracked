# -*- coding: UTF-8 -*-

'''
Module
    iworker.py
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
    Defines structural interface for lifecycle-managed background workers.
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
class IConnectionWorker(Protocol):
    '''
        Defines structural protocol for background worker lifecycle control.

        It defines:

            :methods:
                | start - Activates background worker execution.
                | stop - Signals worker termination and waits for completion.
                | is_running - Checks if worker loop is currently active.
    '''

    def start(self) -> None:
        '''
            Activates background worker execution.
        '''

    def stop(self) -> None:
        '''
            Signals worker termination and waits for completion.
        '''

    def is_running(self) -> bool:
        '''
            Checks if worker loop is currently active.

            :return: True if active, False otherwise.
        '''
