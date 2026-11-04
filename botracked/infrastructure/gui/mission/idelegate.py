# -*- coding: UTF-8 -*-

'''
Module
    idelegate.py
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
    Defines IMissionActionDelegate protocol for mission studio actions.
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
class IMissionActionDelegate(Protocol):
    '''
        Defines structural contract IMissionActionDelegate for mission studio.

        It defines:

            :methods:
                | handle_run - Compiles and starts mission script execution.
                | handle_pause - Pauses running mission execution.
                | handle_resume - Resumes paused mission execution.
                | handle_abort - Aborts active mission execution.
                | handle_validate - Validates DSL script syntax.
    '''

    def handle_run(self, script: str) -> None:
        '''
            Compiles and starts mission script execution.

            :param script: DSL script source text.
        '''

    def handle_pause(self) -> None:
        '''
            Pauses running mission execution.
        '''

    def handle_resume(self) -> None:
        '''
            Resumes paused mission execution.
        '''

    def handle_abort(self) -> None:
        '''
            Aborts active mission execution.
        '''

    def handle_validate(self, script: str) -> tuple[bool, str]:
        '''
            Validates DSL script syntax without executing.

            :param script: DSL script source text.
            :return: Tuple of validation boolean and status message.
        '''
