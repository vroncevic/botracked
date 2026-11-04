# -*- coding: UTF-8 -*-

'''
Module
    protocol_opcode_test.py
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
    Unit tests for ProtocolOpcode IntEnum.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.model.protocol_opcode import ProtocolOpcode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProtocolOpcodeTest(TestCase):
    '''
        Tests ProtocolOpcode integer enumeration values and message opcodes.
    '''

    def test_command_opcodes(self) -> None:
        '''
            Verifies host-to-robot command opcode byte values.

            :exceptions: None.
        '''
        self.assertEqual(int(ProtocolOpcode.CMD_MOTION), 0x01)
        self.assertEqual(int(ProtocolOpcode.CMD_SET_SPEED), 0x02)
        self.assertEqual(int(ProtocolOpcode.CMD_STOP), 0x03)
        self.assertEqual(int(ProtocolOpcode.CMD_PING), 0x04)
        self.assertEqual(int(ProtocolOpcode.CMD_GET_STATUS), 0x10)
        self.assertEqual(int(ProtocolOpcode.CMD_GET_DIAG), 0x11)
        self.assertEqual(int(ProtocolOpcode.CMD_ERR_CLEAR), 0x12)

    def test_response_opcodes(self) -> None:
        '''
            Verifies robot-to-host response opcode byte values.

            :exceptions: None.
        '''
        self.assertEqual(int(ProtocolOpcode.RESP_ACK), 0x80)
        self.assertEqual(int(ProtocolOpcode.RESP_NACK), 0x81)
        self.assertEqual(int(ProtocolOpcode.RESP_PONG), 0x84)
        self.assertEqual(int(ProtocolOpcode.RESP_STATUS), 0x90)
        self.assertEqual(int(ProtocolOpcode.RESP_DIAG), 0x91)


if __name__ == '__main__':
    main()
