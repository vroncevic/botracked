# -*- coding: UTF-8 -*-

'''
Module
    adapter_test.py
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
    Unit tests for MissionActionAdapter.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.service.dsl.iservice import ITbotDslService
from botracked.core.service.motion.runner.irunner import IMissionRunner
from botracked.infrastructure.gui.console.observer.ilistener import ILogListener
from botracked.infrastructure.gui.mission.adapter.adapter import MissionActionAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionActionAdapterTest(TestCase):
    '''
        Tests MissionActionAdapter run, pause, resume, abort, and validate.
    '''

    def test_mission_actions(self) -> None:
        '''
            Verifies DSL compile/validate and runner lifecycle delegation.

            :exceptions: None.
        '''
        runner = MagicMock(spec=IMissionRunner)
        dsl = MagicMock(spec=ITbotDslService)
        dsl.compile.return_value = ()
        dsl.validate.return_value = (True, 'Valid')
        log = MagicMock(spec=ILogListener)

        adapter = MissionActionAdapter(
            mission_runner=runner, dsl_service=dsl, log_listener=log
        )
        adapter.handle_run('PING\n')
        runner.start.assert_called_once()
        adapter.handle_pause()
        runner.pause.assert_called_once()
        adapter.handle_resume()
        runner.resume.assert_called_once()
        adapter.handle_abort()
        runner.abort.assert_called_once()
        self.assertEqual(adapter.handle_validate('PING\n'), (True, 'Valid'))


if __name__ == '__main__':
    main()
