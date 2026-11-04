# -*- coding: UTF-8 -*-

'''
Module
    iidentifier.py
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
    Defines IIdentifierScanner structural protocol for keyword/identifier scanning.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.dsl.token import Token

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IIdentifierScanner(Protocol):
    '''
        Defines protocol IIdentifierScanner with method(s).
        Structural protocol for scanning keywords and identifier tokens.

        It defines:

            :methods:
                | is_identifier_start - Checks if character starts an identifier.
                | scan - Scans identifier or keyword and returns token with column.
    '''

    def is_identifier_start(self, ch: str) -> bool:
        '''
            Checks if character starts an identifier or keyword.

            :param ch: Character under current column.
            :return: True if alphabetical or underscore, False otherwise.
        '''

    def scan(self, line: str, col: int, line_idx: int) -> tuple[Token, int]:
        '''
            Scans an identifier or keyword and returns token with advanced column.

            :param line: Source text line.
            :param col: Starting column index (1-based).
            :param line_idx: Line number (1-based).
            :return: Tuple of generated Token and updated column index.
        '''
