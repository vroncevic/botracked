# -*- coding: UTF-8 -*-

'''
Module
    executor_test.py
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
    Unit tests for StudioCommandExecutor.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.model.exceptions.botracked_error import BotrackedError
from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.infrastructure.command.definition import StudioCommandDefinition
from botracked.infrastructure.command.executor import StudioCommandExecutor
from botracked.infrastructure.command.ipreloader import IScriptPreloader
from botracked.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class StudioCommandExecutorTest(TestCase):
    '''
        Tests StudioCommandExecutor preloading, launch, and error reporting.
    '''

    def test_execute_success_and_error(self) -> None:
        '''
            Verifies GUI launch return dict and error handling path.

            :exceptions: None.
        '''
        gui = MagicMock(spec=IGUI)
        gui.is_initialized.return_value = True
        srv = MagicMock(spec=BotRuntimeBundle)
        srv.is_initialized.return_value = True
        preloader = MagicMock(spec=IScriptPreloader)
        executor = StudioCommandExecutor(
            definition=StudioCommandDefinition(),
            gui=gui,
            preloader=preloader,
        )
        res = executor.execute(params={'script': ''}, service=srv)
        self.assertEqual(res['returncode'], 0)
        self.assertIsNotNone(executor.get_definition())
        gui.start.assert_called_once()
        self.assertTrue(str(executor))

        gui.is_initialized.return_value = False
        uninit_res = executor.execute(params={}, service=srv)
        self.assertEqual(uninit_res['returncode'], 1)
        self.assertIn('not initialized', str(uninit_res['stderr']))
        gui.is_initialized.return_value = True

        gui.start.side_effect = BotrackedError('gui failure')
        err_res = executor.execute(params={}, service=srv)
        self.assertEqual(err_res['returncode'], 1)
        self.assertIn('gui failure', str(err_res['stderr']))


if __name__ == '__main__':
    main()
