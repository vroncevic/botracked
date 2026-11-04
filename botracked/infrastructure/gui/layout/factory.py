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
    Defines LayoutFactory assembling LayoutBuilder subsystem.
'''

from __future__ import annotations

from botracked.infrastructure.gui.layout.builder import LayoutBuilder
from botracked.infrastructure.gui.layout.dependencies import LayoutDependencies
from botracked.infrastructure.gui.layout.provides import LayoutProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class LayoutFactory:
    '''
        Defines class LayoutFactory assembling split-pane layout builder.

        It defines:

            :methods:
                | create - Creates LayoutProvides from LayoutDependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: LayoutDependencies) -> LayoutProvides:
        '''
            Creates LayoutProvides from LayoutDependencies.

            :param dependencies: Layout collaborators bundle.
            :return: Wired LayoutProvides bundle.
            :exceptions: None.
        '''
        builder = LayoutBuilder(root=dependencies.root)

        return LayoutProvides(builder=builder, slots=builder.create_slots())

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
