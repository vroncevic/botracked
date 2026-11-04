# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Engine orchestrating the initialization and execution of botracked.
'''

from __future__ import annotations

from collections.abc import Mapping
from logging import ERROR, INFO
from sys import stdout

from ats_utilities.base.engine import Base
from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.logger.ilogger import ILogger

from botracked.infrastructure.cli.icli import ICLI
from botracked.setup.bundle import BotrackedBundle
from botracked.setup.validator import BotrackedBundleValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Botracked(Base):
    '''
        Engine orchestrating the initialization and execution of botracked.

        It defines:

            :attributes:
                | _is_initialized - Boolean flag tracking initialization state.
                | _has_logger - Boolean flag tracking logger availability.
                | _logger - Logger interface instance from base context.
                | _cli - CLI adapter contract instance.
            :methods:
                | __init__ - Initializes engine with adapters and services.
                | process - Processes botracked CLI or GUI operations.
    '''

    _is_initialized: bool
    _logger: ILogger
    _cli: ICLI

    def __init__(self, bundle: BotrackedBundle) -> None:
        '''
            Initializes the botracked engine with adapters and services.

            :param bundle: BotrackedBundle containing adapters and services.
            :exceptions: None.
        '''
        self._is_initialized = False

        try:
            BotrackedBundleValidator.validate(bundle)
            super().__init__(bundle.base)

            self._logger = self.get_context().logger
            self._is_initialized = False
            self._cli = bundle.cli

            self._is_initialized = (
                bundle.base.option_manager.is_initialized()
                and bundle.service.is_initialized()
                and bundle.gui.is_initialized()
                and self._cli.is_initialized()
            )

            self._logger.write_log(
                INFO, '✅ botracked: engine initialized successfully!'
            )

        except (ATSValueError, ATSTypeError) as exc:
            stdout.write(f'❌ botracked: {exc}!\n')

        except Exception as exc:
            stdout.write(f'❌ botracked unexpected exception: {exc}!\n')

    def process(self, verbose: bool = False) -> bool:
        '''
            Processes botracked CLI or GUI operations.

            :param verbose: Enable verbose output.
            :return: True if successful, False otherwise.
            :exceptions: None.
        '''
        result: Mapping[str, object] = {}

        try:
            if self.is_initialized():
                self._logger.write_log(INFO, '🔥 Starting botracked execution...')
                result: Mapping[str, object] = self._cli.run()
                self._logger.write_log(INFO, '✅ Execution finished!')

                if result.get('returncode') != 0:
                    stderr_msg = result.get('stderr') or 'failed!'
                    self._logger.write_log(ERROR, f'❌ botracked: {stderr_msg}')
                    return False

                self._logger.write_log(INFO, '✅ bottracked: done!')
                self._logger.write_log(INFO, '✅ bottracked: exiting successfully!')
                return True

            stdout.write('❌ bottracked: engine not initialized!\n')
            return False

        except (ATSValueError, ATSTypeError) as exc:
            stdout.write(f'❌ bottracked: {exc}!\n')
            return False

        except Exception as exc:
            stdout.write(f'❌ bottracked unexpected exception: {exc}!\n')
            return False
