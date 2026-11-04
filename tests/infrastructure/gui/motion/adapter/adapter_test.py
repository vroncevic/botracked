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
    Unit tests for MotionActionAdapter.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.model.exceptions.botracked_error import BotrackedError
from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.core.service.motion.iservice import IBotMotionService
from botracked.infrastructure.gui.console.observer.ilistener import ILogListener
from botracked.infrastructure.gui.motion.adapter.adapter import MotionActionAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MotionActionAdapterTest(TestCase):
    '''
        Tests MotionActionAdapter manual motion, speed, stop, ping, and clear.
    '''

    def test_actions_and_error_logging(self) -> None:
        '''
            Verifies forwarding to motion service and error log capture.

            :exceptions: None.
        '''
        srv = MagicMock(spec=IBotMotionService)
        log = MagicMock(spec=ILogListener)
        adapter = MotionActionAdapter(motion_service=srv, log_listener=log)

        adapter.handle_motion(MotionCommand.FORWARD)
        srv.send_motion.assert_called_once_with(MotionCommand.FORWARD)
        adapter.handle_speed(200)
        srv.set_speed.assert_called_once_with(200)
        adapter.handle_stop()
        srv.stop_motors.assert_called_once()
        adapter.handle_ping()
        srv.send_command.assert_called_with(ProtocolOpcode.CMD_PING)
        adapter.handle_clear_errors()
        srv.send_command.assert_called_with(ProtocolOpcode.CMD_ERR_CLEAR)

        srv.stop_motors.side_effect = BotrackedError('offline')
        adapter.handle_stop()
        log.write_entry.assert_called_once()

        srv.send_motion.side_effect = BotrackedError('motion err')
        adapter.handle_motion(MotionCommand.FORWARD)

        srv.set_speed.side_effect = BotrackedError('speed err')
        adapter.handle_speed(200)

        srv.send_command.side_effect = BotrackedError('cmd err')
        adapter.handle_ping()
        adapter.handle_clear_errors()


if __name__ == '__main__':
    main()
