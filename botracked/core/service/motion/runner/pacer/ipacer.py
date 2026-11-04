# -*- coding: UTF-8 -*-

'''
Module
    ipacer.py
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
    Defines structural contract IMissionPacer for step timing and pause control.
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
class IMissionPacer(Protocol):
    '''
        Defines structural contract IMissionPacer for step delays and pauses.

        It defines:

            :methods:
                | wait_paused - Waits while pause flag is active unless stopped.
                | sleep_step - Waits for step duration while observing stop flag.
    '''

    def wait_paused(self) -> bool:
        '''
            Waits while pause flag is active unless cancellation occurs.

            :return: True if resumed normally, False if stopped.
        '''

    def sleep_step(self, duration_s: float) -> bool:
        '''
            Waits for step duration while observing cancellation signal.

            :param duration_s: Step duration to wait in seconds.
            :return: True if full duration elapsed, False if stopped.
        '''
