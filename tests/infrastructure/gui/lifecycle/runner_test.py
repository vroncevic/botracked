# -*- coding: UTF-8 -*-

'''
Module
    runner_test.py
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
    Unit tests for GuiLifecycleRunner.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.model.exceptions.botracked_error import BotrackedError
from botracked.core.service.connection.iservice import IBotConnectionService
from botracked.core.service.motion.runner.irunner import IMissionRunner
from botracked.core.service.telemetry.listener.ilistener import ITelemetryListener
from botracked.core.service.telemetry.poller.ipoller import ITelemetryPoller
from botracked.infrastructure.gui.lifecycle.dependencies import GuiLifecycleDependencies
from botracked.infrastructure.gui.lifecycle.runner import GuiLifecycleRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiLifecycleRunnerTest(TestCase):
    '''
        Tests GuiLifecycleRunner mainloop launch and resilient shutdown.
    '''

    def test_start_and_stop_resilience(self) -> None:
        '''
            Verifies mainloop start and clean teardown even when errors occur.

            :exceptions: None.
        '''
        root = MagicMock(spec=Tk)
        conn = MagicMock(spec=IBotConnectionService)
        listener = MagicMock(spec=ITelemetryListener)
        poller = MagicMock(spec=ITelemetryPoller)
        mission = MagicMock(spec=IMissionRunner)
        runner = GuiLifecycleRunner(
            GuiLifecycleDependencies(
                root=root,
                connection_service=conn,
                listener=listener,
                poller=poller,
                mission_runner=mission,
            )
        )
        self.assertFalse(runner.is_closing())
        runner.start()
        root.mainloop.assert_called_once()

        poller.stop.side_effect = BotrackedError('poller err')
        listener.stop.side_effect = BotrackedError('listener err')
        mission.abort.side_effect = BotrackedError('mission abort err')
        conn.disconnect.side_effect = BotrackedError('disconnect err')
        root.destroy.side_effect = TclError('destroyed')
        runner.stop()
        self.assertTrue(runner.is_closing())
        poller.stop.assert_called_once()
        listener.stop.assert_called_once()
        mission.abort.assert_called_once()
        conn.disconnect.assert_called_once()


if __name__ == '__main__':
    main()
