# -*- coding: UTF-8 -*-

'''
Module
    service_test.py
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
    Unit tests for BotMotionService.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.core.service.connection.dispatcher.idispatcher import IFrameDispatcher
from botracked.core.service.motion.service import BotMotionService

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotMotionServiceTestCase(TestCase):
    '''
        Verifies BotMotionService motion, speed, command, and step dispatch.
    '''

    def setUp(self) -> None:
        '''
            Prepares test fixtures.

            :exceptions: None.
        '''
        self.mock_dispatcher = Mock(spec=IFrameDispatcher)
        self.service = BotMotionService(dispatcher=self.mock_dispatcher)

    def test_motion_speed_stop_and_command(self) -> None:
        '''
            Verifies send_motion, clamped set_speed, stop_motors, send_command.

            :exceptions: None.
        '''
        self.mock_dispatcher.dispatch_frame.return_value = True
        self.assertTrue(self.service.send_motion(MotionCommand.FORWARD))
        self.mock_dispatcher.dispatch_frame.assert_called_with(
            ProtocolOpcode.CMD_MOTION,
            bytes([MotionCommand.FORWARD.value]),
            'CMD_MOTION(FORWARD)',
        )

        self.assertTrue(self.service.set_speed(300))
        self.mock_dispatcher.dispatch_frame.assert_called_with(
            ProtocolOpcode.CMD_SET_SPEED, bytes([255]), 'CMD_SET_SPEED(300)'
        )
        self.assertTrue(self.service.set_speed(-5))
        self.mock_dispatcher.dispatch_frame.assert_called_with(
            ProtocolOpcode.CMD_SET_SPEED, bytes([0]), 'CMD_SET_SPEED(-5)'
        )

        self.assertTrue(self.service.stop_motors())
        self.mock_dispatcher.dispatch_frame.assert_called_with(
            ProtocolOpcode.CMD_STOP, b'', 'CMD_STOP'
        )
        self.assertTrue(self.service.send_command(ProtocolOpcode.CMD_PING))
        self.mock_dispatcher.dispatch_frame.assert_called_with(
            ProtocolOpcode.CMD_PING, b'', 'CMD_PING'
        )

    def test_execute_step_outcomes(self) -> None:
        '''
            Verifies execute_step returns True on full success and False on drop.

            :exceptions: None.
        '''
        step = CompiledStep(
            frames=(b'\x01', b'\x02'),
            duration_sec=0.5,
            auto_stop_after=False,
            description='MOVE',
            line_number=3,
        )
        self.mock_dispatcher.dispatch_raw.return_value = True
        self.assertTrue(self.service.execute_step(step))

        self.mock_dispatcher.dispatch_raw.side_effect = [True, False]
        self.assertFalse(self.service.execute_step(step))


if __name__ == '__main__':
    main()
