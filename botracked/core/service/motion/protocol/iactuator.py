# -*- coding: UTF-8 -*-

'''
Module
    iactuator.py
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
    Defines narrow ISP protocol IMissionActuator for mission step execution.
'''

from __future__ import annotations

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
class IMissionActuator(Protocol):
    '''
        Defines narrow ISP protocol IMissionActuator for automated routines.

        It defines:

            :methods:
                | execute_step - Dispatches frames for a compiled mission step.
                | stop_motors - Sends immediate motor halt command.
    '''

    def execute_step(self, step: CompiledStep) -> bool:
        '''
            Executes a single compiled mission step.

            :param step: CompiledStep instance with binary frames.
            :return: True if all frames dispatched, False otherwise.
        '''

    def stop_motors(self) -> bool:
        '''
            Sends emergency or post-step motor stop command.

            :return: True if sent, False otherwise.
        '''
