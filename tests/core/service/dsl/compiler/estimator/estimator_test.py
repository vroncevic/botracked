# -*- coding: UTF-8 -*-

'''
Module
    estimator_test.py
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
    Unit tests for AstDurationEstimator.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.token_type import TokenType
from botracked.core.model.exceptions.dsl_syntax_error import DslSyntaxError
from botracked.core.service.dsl.compiler.estimator.estimator import AstDurationEstimator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AstDurationEstimatorTest(TestCase):
    '''
        Tests AstDurationEstimator execution timing estimates.
    '''

    _estimator: AstDurationEstimator

    def setUp(self) -> None:
        '''
            Sets up test fixture before each test method.

            :exceptions: None.
        '''
        self._estimator = AstDurationEstimator()

    def test_estimate_motion_and_wait(self) -> None:
        '''
            Verifies duration estimation for motion and wait instructions.

            :exceptions: None.
        '''
        fwd = AstInstruction(
            token_type=TokenType.FORWARD,
            line_number=1,
            parameters=(2.5,),
            children=(),
        )
        wait = AstInstruction(
            token_type=TokenType.WAIT,
            line_number=2,
            parameters=(1.0,),
            children=(),
        )
        stop = AstInstruction(
            token_type=TokenType.STOP,
            line_number=3,
            parameters=(),
            children=(),
        )
        total = self._estimator.estimate_duration((fwd, wait, stop))
        self.assertAlmostEqual(total, 3.5)

    def test_estimate_defaults_and_repeat(self) -> None:
        '''
            Verifies fallback default durations and repeat loop multiplier.

            :exceptions: None.
        '''
        fwd_default = AstInstruction(
            token_type=TokenType.FORWARD,
            line_number=1,
            parameters=(),
            children=(),
        )
        wait_default = AstInstruction(
            token_type=TokenType.WAIT,
            line_number=2,
            parameters=(),
            children=(),
        )
        self.assertEqual(self._estimator.estimate_node(fwd_default), 0.0)
        self.assertEqual(self._estimator.estimate_node(wait_default), 0.5)

        repeat = AstInstruction(
            token_type=TokenType.REPEAT,
            line_number=3,
            parameters=(3,),
            children=(
                AstInstruction(
                    token_type=TokenType.TURN_LEFT,
                    line_number=4,
                    parameters=(1.0,),
                    children=(),
                ),
            ),
        )
        self.assertAlmostEqual(self._estimator.estimate_node(repeat), 3.0)

    def test_estimate_unsupported_node(self) -> None:
        '''
            Verifies DslSyntaxError when evaluating an unsupported token type.

            :exceptions: None.
        '''
        node = AstInstruction(
            token_type=TokenType.IDENTIFIER,
            line_number=9,
            parameters=(),
            children=(),
        )
        with self.assertRaises(DslSyntaxError):
            self._estimator.estimate_node(node)


if __name__ == '__main__':
    main()
