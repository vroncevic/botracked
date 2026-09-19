# -*- coding: UTF-8 -*-

'''
Module
    token_type.py
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
    Defines TokenType enumeration for tracked_bot mission scripting language.
'''

from __future__ import annotations

from enum import Enum, auto

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TokenType(Enum):
    '''
        Lexical token types recognized in .track mission scripts.

        It defines:

            :attributes:
                | SPEED - Speed configuration keyword.
                | FORWARD - Forward motion keyword.
                | BACKWARD - Backward motion keyword.
                | TURN_LEFT - Turn left keyword.
                | TURN_RIGHT - Turn right keyword.
                | SPIN_LEFT - Spin left keyword.
                | SPIN_RIGHT - Spin right keyword.
                | WAIT - Wait pause keyword.
                | STOP - Stop motion keyword.
                | PING - Ping communication keyword.
                | CLEAR_ERRORS - Clear errors keyword.
                | REPEAT - Loop repeat keyword.
                | END - Loop end keyword.
                | NUMBER - Integer or floating point literal.
                | IDENTIFIER - Generic identifier or unknown token.
                | COLON - Colon punctuation separator.
                | NEWLINE - Statement newline delimiter.
                | COMMENT - Comment line starting with hash.
                | EOF - End of script stream marker.
    '''

    # Instructions
    SPEED = auto()
    FORWARD = auto()
    BACKWARD = auto()
    TURN_LEFT = auto()
    TURN_RIGHT = auto()
    SPIN_LEFT = auto()
    SPIN_RIGHT = auto()
    WAIT = auto()
    STOP = auto()
    PING = auto()
    CLEAR_ERRORS = auto()

    # Control Flow
    REPEAT = auto()
    END = auto()

    # Literals and punctuation
    NUMBER = auto()
    IDENTIFIER = auto()
    COLON = auto()
    NEWLINE = auto()
    COMMENT = auto()
    EOF = auto()
