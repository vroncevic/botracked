# -*- coding: UTF-8 -*-

'''
Module
    inode_test.py
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
    Unit tests for INodeCompiler protocol.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.dsl.compiler.motion.imotion import IMotionStepCompiler
from botracked.core.service.dsl.compiler.node.inode import INodeCompiler
from botracked.core.service.dsl.compiler.node.node import NodeCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NodeCompilerProtocolTest(TestCase):
    '''
        Verifies runtime structural subtyping of INodeCompiler.
    '''

    def test_conformance(self) -> None:
        '''
            Verifies NodeCompiler and Mock satisfy INodeCompiler.

            :exceptions: None.
        '''
        node_compiler = NodeCompiler(
            motion_compiler=Mock(spec=IMotionStepCompiler),
            codec=Mock(spec=IBinaryCodec),
            default_speed=180,
        )
        self.assertIsInstance(node_compiler, INodeCompiler)
        self.assertIsInstance(Mock(spec=INodeCompiler), INodeCompiler)
        self.assertNotIsInstance(object(), INodeCompiler)


if __name__ == '__main__':
    main()
