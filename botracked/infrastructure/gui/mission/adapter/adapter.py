# -*- coding: UTF-8 -*-

'''
Module
    adapter.py
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
    Provides MissionActionAdapter bridging GUI mission events to DSL and runner.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.service.dsl.iservice import ITbotDslService
from botracked.core.service.motion.runner.irunner import IMissionRunner
from botracked.infrastructure.gui.console.observer.ilistener import ILogListener

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionActionAdapter:
    '''
        Defines class MissionActionAdapter implementing IMissionActionDelegate.
        Adapts GUI mission events to core mission runner and DSL service.

        It defines:

            :attributes:
                | LEVEL_INFO - Informational console log severity tag.
                | LEVEL_WARN - Warning console log severity tag.
                | _mission_runner - Asynchronous mission execution runner port.
                | _dsl_service - DSL parsing, validation, and compilation port.
                | _log_listener - Diagnostic console log listener port.
            :methods:
                | __init__ - Initializes adapter with runner, DSL, and logger.
                | handle_run - Compiles and starts mission script execution.
                | handle_pause - Pauses running mission execution.
                | handle_resume - Resumes paused mission execution.
                | handle_abort - Aborts active mission execution.
                | handle_validate - Validates script syntax without executing.
    '''

    LEVEL_INFO: ClassVar[str] = 'INFO'
    LEVEL_WARN: ClassVar[str] = 'WARN'

    _mission_runner: IMissionRunner
    _dsl_service: ITbotDslService
    _log_listener: ILogListener

    def __init__(
        self,
        mission_runner: IMissionRunner,
        dsl_service: ITbotDslService,
        log_listener: ILogListener,
    ) -> None:
        '''
            Initializes adapter with mission runner, DSL service, and logger.

            :param mission_runner: Asynchronous mission runner instance.
            :param dsl_service: DSL compiler service instance.
            :param log_listener: Diagnostic console log listener.
            :exceptions: None.
        '''
        self._mission_runner = mission_runner
        self._dsl_service = dsl_service
        self._log_listener = log_listener

    def handle_run(self, script: str) -> None:
        '''
            Compiles and starts mission script execution.

            :param script: DSL script source text.
            :exceptions:
                | DslError: If script compilation fails.
        '''
        steps = self._dsl_service.compile(script)
        self._mission_runner.start(steps)
        self._log_listener.write_entry(
            self.LEVEL_INFO, f'Started mission ({len(steps)} compiled steps)'
        )

    def handle_pause(self) -> None:
        '''
            Pauses running mission execution.

            :exceptions: None.
        '''
        self._mission_runner.pause()
        self._log_listener.write_entry(self.LEVEL_WARN, 'Mission paused')

    def handle_resume(self) -> None:
        '''
            Resumes paused mission execution.

            :exceptions: None.
        '''
        self._mission_runner.resume()
        self._log_listener.write_entry(self.LEVEL_INFO, 'Mission resumed')

    def handle_abort(self) -> None:
        '''
            Aborts active mission execution.

            :exceptions: None.
        '''
        self._mission_runner.abort()
        self._log_listener.write_entry(self.LEVEL_WARN, 'Mission aborted')

    def handle_validate(self, script: str) -> tuple[bool, str]:
        '''
            Validates script syntax without executing.

            :param script: DSL script source text.
            :return: Tuple of validation success boolean and message string.
            :exceptions: None.
        '''
        return self._dsl_service.validate(script)
