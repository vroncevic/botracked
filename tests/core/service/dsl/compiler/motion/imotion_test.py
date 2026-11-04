# -*- coding: UTF-8 -*-

'''
Module
    imotion_test.py
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
    Unit tests for IMotionStepCompiler protocol.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, Mock

from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.dsl.compiler.motion.imotion import IMotionStepCompiler
from botracked.core.service.dsl.compiler.motion.motion import MotionStepCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionStepCompilerProtocolTest(TestCase):
    '''
        Verifies runtime structural subtyping of IMotionStepCompiler.
    '''

    def test_protocol_satisfaction(self) -> None:
        '''
            Verifies MotionStepCompiler and Mock satisfy IMotionStepCompiler.

            :exceptions: None.
        '''
        codec = MagicMock(spec=IBinaryCodec)
        compiler = MotionStepCompiler(codec=codec)
        self.assertIsInstance(compiler, IMotionStepCompiler)
        self.assertIsInstance(Mock(spec=IMotionStepCompiler), IMotionStepCompiler)
        self.assertNotIsInstance(object(), IMotionStepCompiler)


if __name__ == '__main__':
    main()
