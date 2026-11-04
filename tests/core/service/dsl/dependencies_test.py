# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for DslDependencies bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.dsl.compiler.icompiler import ITbotCompiler
from botracked.core.service.dsl.dependencies import DslDependencies
from botracked.core.service.dsl.lexer.ilexer import ITbotLexer
from botracked.core.service.dsl.parser.iparser import ITbotParser

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslDependenciesTest(TestCase):
    '''
        Verifies DslDependencies field storage and immutability.
    '''

    def test_bundle_immutability(self) -> None:
        '''
            Verifies stored lexer, parser, compiler ports and frozen protection.

            :exceptions: None.
        '''
        lexer = Mock(spec=ITbotLexer)
        parser = Mock(spec=ITbotParser)
        compiler = Mock(spec=ITbotCompiler)
        deps = DslDependencies(lexer=lexer, parser=parser, compiler=compiler)
        self.assertIs(deps.lexer, lexer)
        self.assertIs(deps.parser, parser)
        self.assertIs(deps.compiler, compiler)
        with self.assertRaises(FrozenInstanceError):
            setattr(deps, 'lexer', lexer)


if __name__ == '__main__':
    main()
