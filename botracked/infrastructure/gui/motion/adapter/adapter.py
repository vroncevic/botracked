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
    Provides MotionActionAdapter bridging GUI motion controls to motion service.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.model.exceptions.botracked_error import BotrackedError
from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.core.service.motion.iservice import IBotMotionService
from botracked.infrastructure.gui.console.observer.ilistener import ILogListener

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MotionActionAdapter:
    '''
        Defines class MotionActionAdapter implementing IMotionActionDelegate.
        Adapts GUI manual motion and diagnostic actions to IBotMotionService.

        It defines:

            :attributes:
                | LEVEL_ERROR - Error severity tag for console stream.
                | _motion_service - Kinematic actuation and motion service port.
                | _log_listener - Diagnostic console log listener port.
            :methods:
                | __init__ - Initializes adapter with motion service and logger.
                | handle_motion - Transmits motion direction command.
                | handle_speed - Sets active locomotion PWM speed value.
                | handle_stop - Immediately stops tracked bot locomotion.
                | handle_ping - Sends link health verification ping.
                | handle_clear_errors - Dispatches error reset sequence.
    '''

    LEVEL_ERROR: ClassVar[str] = 'ERROR'

    _motion_service: IBotMotionService
    _log_listener: ILogListener

    def __init__(
        self,
        motion_service: IBotMotionService,
        log_listener: ILogListener,
    ) -> None:
        '''
            Initializes adapter with core motion service and log listener.

            :param motion_service: Kinematic actuation and motion service.
            :param log_listener: Diagnostic console log listener.
            :exceptions: None.
        '''
        self._motion_service = motion_service
        self._log_listener = log_listener

    def handle_motion(self, cmd: MotionCommand) -> None:
        '''
            Transmits motion direction command safely.

            :param cmd: MotionCommand direction value.
            :exceptions: None.
        '''
        try:
            self._motion_service.send_motion(cmd)
        except BotrackedError as exc:
            self._log_listener.write_entry(
                self.LEVEL_ERROR, f'Motion {cmd.name} failed: {exc}'
            )

    def handle_speed(self, speed: int) -> None:
        '''
            Sets active locomotion PWM speed value safely.

            :param speed: PWM speed value (0-255).
            :exceptions: None.
        '''
        try:
            self._motion_service.set_speed(speed)
        except BotrackedError as exc:
            self._log_listener.write_entry(
                self.LEVEL_ERROR, f'Speed update failed: {exc}'
            )

    def handle_stop(self) -> None:
        '''
            Immediately stops tracked bot locomotion safely.

            :exceptions: None.
        '''
        try:
            self._motion_service.stop_motors()
        except BotrackedError as exc:
            self._log_listener.write_entry(
                self.LEVEL_ERROR, f'Stop motors failed: {exc}'
            )

    def handle_ping(self) -> None:
        '''
            Sends link health verification ping safely.

            :exceptions: None.
        '''
        try:
            self._motion_service.send_command(ProtocolOpcode.CMD_PING)
        except BotrackedError as exc:
            self._log_listener.write_entry(
                self.LEVEL_ERROR, f'Ping command failed: {exc}'
            )

    def handle_clear_errors(self) -> None:
        '''
            Dispatches error reset sequence safely.

            :exceptions: None.
        '''
        try:
            self._motion_service.send_command(ProtocolOpcode.CMD_ERR_CLEAR)
        except BotrackedError as exc:
            self._log_listener.write_entry(
                self.LEVEL_ERROR, f'Clear errors failed: {exc}'
            )
