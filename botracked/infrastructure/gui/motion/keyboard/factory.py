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
    Defines MotionKeyboardFactory assembling MotionKeyboardController.
'''

from __future__ import annotations

from botracked.infrastructure.gui.motion.keyboard.controller.controller import (
    MotionKeyboardController,
)
from botracked.infrastructure.gui.motion.keyboard.dependencies import MotionKeyboardDependencies
from botracked.infrastructure.gui.motion.keyboard.provides import MotionKeyboardProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MotionKeyboardFactory:
    '''
        Defines class MotionKeyboardFactory assembling keyboard controller.

        It defines:

            :methods:
                | create - Creates MotionKeyboardProvides from dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls, dependencies: MotionKeyboardDependencies
    ) -> MotionKeyboardProvides:
        '''
            Creates MotionKeyboardProvides from MotionKeyboardDependencies.

            :param dependencies: Keyboard controller collaborators bundle.
            :return: Wired MotionKeyboardProvides bundle.
            :exceptions: None.
        '''
        return MotionKeyboardProvides(
            controller=MotionKeyboardController(delegate=dependencies.delegate)
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
