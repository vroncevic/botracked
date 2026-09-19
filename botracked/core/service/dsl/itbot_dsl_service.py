# -*- coding: UTF-8 -*-

'''
Module
    itbot_dsl_service.py
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
    Defines ITbotDslService interface for script compilation and validation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.dsl.compiled_step import CompiledStep

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITbotDslService(Protocol):
    '''
        Defines protocol ITbotDslService with method(s).
        Protocol for DSL lifecycle operations including validation and compilation.

        It defines:

            :methods:
                | validate - Validates mission script syntax and parameter ranges.
                | compile - Compiles source script into executable binary steps.
    '''

    def validate(self, source: str) -> tuple[bool, str]:
        '''
            Validates .track mission script syntax and parameter ranges.

            :param source: Raw script text.
            :return: Tuple of (is_valid, status_or_error_message).
        '''

    def compile(self, source: str) -> list[CompiledStep]:
        '''
            Compiles source script into executable binary steps.

            :param source: Raw script text.
            :return: List of CompiledStep instances.
        '''
