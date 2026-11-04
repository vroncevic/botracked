# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Defines CompilerFactory assembling DSL AST binary compiler subsystem.
'''

from __future__ import annotations

from botracked.core.service.dsl.compiler.compiler import TbotCompiler
from botracked.core.service.dsl.compiler.dependencies import CompilerDependencies
from botracked.core.service.dsl.compiler.estimator.estimator import AstDurationEstimator
from botracked.core.service.dsl.compiler.motion.motion import MotionStepCompiler
from botracked.core.service.dsl.compiler.node.node import NodeCompiler
from botracked.core.service.dsl.compiler.provides import CompilerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CompilerFactory:
    '''
        Defines class CompilerFactory assembling TbotCompiler and collaborators.

        It defines:

            :methods:
                | create - Creates CompilerProvides bundle from dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: CompilerDependencies) -> CompilerProvides:
        '''
            Creates CompilerProvides bundle from injected dependencies.

            :param dependencies: External codec and baseline speed configuration.
            :return: Assembled CompilerProvides bundle.
            :exceptions: None.
        '''
        estimator: AstDurationEstimator = AstDurationEstimator()
        motion_compiler: MotionStepCompiler = MotionStepCompiler(
            codec=dependencies.codec
        )
        node_compiler: NodeCompiler = NodeCompiler(
            motion_compiler=motion_compiler,
            codec=dependencies.codec,
            default_speed=dependencies.default_speed,
        )
        compiler: TbotCompiler = TbotCompiler(
            node_compiler=node_compiler,
            estimator=estimator,
        )

        return CompilerProvides(compiler=compiler)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
