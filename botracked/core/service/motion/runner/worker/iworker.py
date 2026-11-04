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
    Defines structural contract IMissionExecutionWorker for step execution.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from botracked.core.model.dsl.compiled_step import CompiledStep

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMissionExecutionWorker(Protocol):
    '''
        Defines structural contract IMissionExecutionWorker for step execution.

        It defines:

            :methods:
                | load_steps - Stores ordered mission steps for next run cycle.
                | execute - Executes sequence of mission steps synchronously.
                | run - Executes loaded mission steps on background runner.
                | is_stopped - Checks if cancellation signal flag is set.
    '''

    def load_steps(self, steps: Sequence[CompiledStep]) -> None:
        '''
            Stores ordered mission steps for next run cycle.

            :param steps: Ordered sequence of compiled mission steps.
        '''

    def execute(self, steps: Sequence[CompiledStep]) -> bool:
        '''
            Executes sequence of mission steps synchronously.

            :param steps: Ordered sequence of compiled mission steps.
            :return: True if all steps completed, False if aborted.
        '''

    def run(self) -> None:
        '''
            Executes loaded mission steps on background runner.
        '''

    def is_stopped(self) -> bool:
        '''
            Checks if cancellation signal flag is set.

            :return: True if stop flag is set, False otherwise.
        '''
