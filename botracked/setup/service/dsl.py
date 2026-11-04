# -*- coding: UTF-8 -*-

'''
Module
    dsl.py
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
    Defines DslAssembler wiring mission routine DSL compilation pipeline.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.dsl.compiler.dependencies import CompilerDependencies
from botracked.core.service.dsl.compiler.factory import CompilerFactory
from botracked.core.service.dsl.dependencies import DslDependencies
from botracked.core.service.dsl.factory import DslFactory
from botracked.core.service.dsl.iservice import ITbotDslService
from botracked.core.service.dsl.lexer.factory import LexerFactory
from botracked.core.service.dsl.parser.factory import ParserFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslAssembler:
    '''
        Defines class DslAssembler wiring mission routine DSL pipeline.

        It defines:

            :attributes:
                | DEFAULT_DSL_SPEED - Baseline mission locomotion speed byte.
            :methods:
                | assemble - Wires lexer, parser, compiler, returns DSL service.
                | get_version - Returns assembler version string.
    '''

    DEFAULT_DSL_SPEED: ClassVar[int] = 180

    @classmethod
    def assemble(cls, codec: IBinaryCodec) -> ITbotDslService:
        '''
            Wires lexer, parser, compiler, and returns DSL service port.

            :param codec: Binary packet codec port.
            :return: Fully configured ITbotDslService instance.
            :exceptions: None.
        '''
        return DslFactory.create(
            DslDependencies(
                lexer=LexerFactory.create().lexer,
                parser=ParserFactory.create().parser,
                compiler=CompilerFactory.create(
                    CompilerDependencies(
                        codec=codec,
                        default_speed=cls.DEFAULT_DSL_SPEED,
                    )
                ).compiler,
            )
        ).service

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns assembler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
