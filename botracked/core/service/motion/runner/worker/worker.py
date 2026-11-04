# -*- coding: UTF-8 -*-

'''
Module
    worker.py
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
    Defines MissionExecutionWorker executing compiled steps over IMissionActuator.
'''

from __future__ import annotations

from collections.abc import Sequence

from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.motion.protocol.iactuator import IMissionActuator
from botracked.core.service.motion.runner.pacer.ipacer import IMissionPacer

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionExecutionWorker:
    '''
        Defines class MissionExecutionWorker implementing IMissionExecutionWorker.
        Executes sequence of compiled mission steps with timed delays and stop control.

        It defines:

            :attributes:
                | _pacer - Pacer port handling step duration delay and pauses.
                | _actuator - Narrow actuator port for step frames and stop.
                | _stop_flag - Signal flag indicating mission abort.
                | _steps - Immutable tuple of loaded mission steps for run cycle.
            :methods:
                | __init__ - Initializes worker with pacer, actuator, and stop flag.
                | load_steps - Stores ordered mission steps for next run cycle.
                | execute - Executes sequence of mission steps sequentially.
                | run - Executes loaded mission steps on background runner.
                | is_stopped - Checks if cancellation signal flag is set.
    '''

    _pacer: IMissionPacer
    _actuator: IMissionActuator
    _stop_flag: ISignalFlag
    _steps: tuple[CompiledStep, ...]

    def __init__(
        self,
        *,
        pacer: IMissionPacer,
        actuator: IMissionActuator,
        stop_flag: ISignalFlag,
    ) -> None:
        '''
            Initializes worker with pacer, mission actuator, and stop flag.

            :param pacer: Pacer handling step duration delay and pauses.
            :param actuator: Narrow actuator executing step frames and motor stop.
            :param stop_flag: Signal flag indicating mission cancellation.
            :exceptions: None.
        '''
        self._pacer = pacer
        self._actuator = actuator
        self._stop_flag = stop_flag
        self._steps = ()

    def load_steps(self, steps: Sequence[CompiledStep]) -> None:
        '''
            Stores ordered mission steps for next run cycle.

            :param steps: Ordered sequence of compiled mission steps.
            :exceptions: None.
        '''
        self._steps = tuple(steps)

    def execute(self, steps: Sequence[CompiledStep]) -> bool:
        '''
            Executes sequence of mission steps sequentially.

            :param steps: Ordered sequence of compiled mission steps.
            :return: True if all steps executed successfully, False if aborted.
            :exceptions: None.
        '''
        for step in steps:
            if self._stop_flag.is_set() or not self._pacer.wait_paused():
                self._actuator.stop_motors()
                return False

            self._actuator.execute_step(step)

            if not self._pacer.sleep_step(step.duration_sec):
                self._actuator.stop_motors()
                return False

            if step.auto_stop_after:
                self._actuator.stop_motors()

        self._actuator.stop_motors()
        return True

    def run(self) -> None:
        '''
            Executes loaded mission steps on background runner.

            :exceptions: None.
        '''
        self.execute(self._steps)

    def is_stopped(self) -> bool:
        '''
            Checks if cancellation signal flag is active.

            :return: True if stop flag is set, False otherwise.
            :exceptions: None.
        '''
        return self._stop_flag.is_set()
