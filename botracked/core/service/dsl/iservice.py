# -*- coding: UTF-8 -*-

'''
Module
    iservice.py
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
    Defines ITbotDslService structural protocol for mission script compilation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.dsl.compiled_step import CompiledStep

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITbotDslService(Protocol):
    '''
        Defines structural protocol ITbotDslService for mission script pipeline.

        It defines:

            :methods:
                | compile - Parses and compiles mission source into binary steps.
                | validate - Validates source script syntax without raising.
                | estimate_duration - Estimates execution duration in seconds.
                | count_tokens - Counts lexical tokens in script text.
    '''

    def compile(self, source: str) -> list[CompiledStep]:
        '''
            Parses and compiles mission source into executable steps.

            :param source: Raw script text.
            :return: List of CompiledStep instances.
        '''

    def validate(self, source: str) -> tuple[bool, str]:
        '''
            Validates source script syntax without raising exceptions.

            :param source: Raw script text.
            :return: Tuple of (is_valid, report_message).
        '''

    def estimate_duration(self, source: str) -> float:
        '''
            Estimates execution duration in seconds.

            :param source: Raw script text.
            :return: Total estimated duration in seconds.
        '''

    def count_tokens(self, source: str) -> int:
        '''
            Counts lexical tokens in script text.

            :param source: Raw script text.
            :return: Integer token count.
        '''
