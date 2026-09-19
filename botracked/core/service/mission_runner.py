# -*- coding: UTF-8 -*-

'''
Module
    mission_runner.py
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
    Provides MissionRunner handling asynchronous timed execution of mission steps.
'''

from __future__ import annotations

from collections.abc import Callable
from threading import Event, Thread
from time import sleep

from botracked.core.model.dsl.compiled_step import CompiledStep

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionRunner:
    '''
        Defines class MissionRunner with attribute(s) and method(s).
        Background worker orchestrating timed mission execution with pause and abort.

        It defines:

            :attributes:
                | _stop_event - Cancellation event flag for thread termination.
                | _pause_event - Pause event flag for freezing mission progression.
                | _thread - Worker thread running the sequence or None.
                | _execute_fn - Callback executing a single step.
                | _stop_fn - Callback commanding robot to stop motors.
            :methods:
                | __init__ - Initializes mission runner with execution callbacks.
                | start - Starts mission execution thread.
                | pause - Pauses mission execution.
                | resume - Resumes mission execution.
                | abort - Aborts mission execution immediately.
                | is_running - Checks if mission is currently active.
                | _worker - Worker thread loop executing steps.
    '''

    _stop_event: Event
    _pause_event: Event
    _thread: Thread | None
    _execute_fn: Callable[[CompiledStep], bool]
    _stop_fn: Callable[[], bool]

    def __init__(
        self,
        execute_fn: Callable[[CompiledStep], bool],
        stop_fn: Callable[[], bool],
    ) -> None:
        '''
            Initializes mission runner with execution callbacks.

            :param execute_fn: Function executing a single step.
            :param stop_fn: Function commanding robot to stop motors.
            :exceptions: None.
        '''
        self._stop_event = Event()
        self._pause_event = Event()
        self._thread = None
        self._execute_fn = execute_fn
        self._stop_fn = stop_fn

    def start(self, steps: list[CompiledStep]) -> None:
        '''
            Starts mission execution thread.

            :param steps: Ordered list of mission steps.
            :exceptions: None.
        '''
        self.abort()
        self._stop_event.clear()
        self._pause_event.clear()
        self._thread = Thread(target=self._worker, args=(steps,), daemon=True)
        self._thread.start()

    def pause(self) -> None:
        '''
            Pauses mission execution.

            :exceptions: None.
        '''
        self._pause_event.set()
        self._stop_fn()

    def resume(self) -> None:
        '''
            Resumes mission execution.

            :exceptions: None.
        '''
        self._pause_event.clear()

    def abort(self) -> None:
        '''
            Aborts mission execution immediately.

            :exceptions: None.
        '''
        self._stop_event.set()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=0.2)
        self._thread = None
        self._stop_fn()

    def is_running(self) -> bool:
        '''
            Checks if mission is currently active.

            :return: True if active, False otherwise.
            :exceptions: None.
        '''
        return self._thread is not None and self._thread.is_alive()

    def _wait_while_paused(self) -> bool:
        '''
            Blocks execution while paused until resumed or stopped.

            :return: True if resumed, False if stopped.
            :rtype: bool

            :exceptions: None.
        '''
        while self._pause_event.is_set():
            if self._stop_event.is_set():
                return False
            sleep(0.05)
        return not self._stop_event.is_set()

    def _sleep_step_duration(self, step: CompiledStep) -> None:
        '''
            Dwells for step duration while handling pause and stop interruptions.

            :param step: Active compiled step.
            :type step: CompiledStep

            :return: None.
            :rtype: None

            :exceptions: None.
        '''
        elapsed: float = 0.0
        while elapsed < step.duration_sec:
            if self._stop_event.is_set():
                break
            if self._pause_event.is_set():
                if not self._wait_while_paused():
                    break
                self._execute_fn(step)
            sleep(0.05)
            elapsed += 0.05

    def _worker(self, steps: list[CompiledStep]) -> None:
        '''
            Worker thread loop executing steps with pause and stop handling.

            :param steps: Ordered list of compiled mission steps.
            :type steps: list[CompiledStep]

            :return: None.
            :rtype: None

            :exceptions: None.
        '''
        for step in steps:
            if self._stop_event.is_set():
                break
            if not self._wait_while_paused():
                break
            self._execute_fn(step)
            if step.duration_sec > 0:
                self._sleep_step_duration(step)
            if step.auto_stop_after and not self._stop_event.is_set():
                self._stop_fn()
        if not self._stop_event.is_set():
            self._stop_fn()
