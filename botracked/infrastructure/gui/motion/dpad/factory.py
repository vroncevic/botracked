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
    Defines MotionDpadFactory assembling MotionTrigger instances and section.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.model.motion_command import MotionCommand
from botracked.infrastructure.gui.motion.dpad.dependencies import MotionDpadDependencies
from botracked.infrastructure.gui.motion.dpad.provides import MotionDpadProvides
from botracked.infrastructure.gui.motion.dpad.section import MotionDpadSection
from botracked.infrastructure.gui.motion.dpad.trigger.itrigger import IMotionTrigger
from botracked.infrastructure.gui.motion.dpad.trigger.trigger import MotionTrigger

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MotionDpadFactory:
    '''
        Defines class MotionDpadFactory assembling D-pad triggers and section.

        It defines:

            :attributes:
                | DIRECTIONAL_COMMANDS - Six directional commands bound on grid.
            :methods:
                | create - Creates MotionDpadProvides from dependencies.
                | get_version - Returns factory version string.
    '''

    DIRECTIONAL_COMMANDS: ClassVar[tuple[MotionCommand, ...]] = (
        MotionCommand.SPIN_LEFT,
        MotionCommand.FORWARD,
        MotionCommand.SPIN_RIGHT,
        MotionCommand.TURN_LEFT,
        MotionCommand.TURN_RIGHT,
        MotionCommand.BACKWARD,
    )

    @classmethod
    def create(cls, dependencies: MotionDpadDependencies) -> MotionDpadProvides:
        '''
            Creates MotionDpadProvides from MotionDpadDependencies.

            :param dependencies: D-pad section collaborators bundle.
            :return: Wired MotionDpadProvides bundle.
            :exceptions: None.
        '''
        triggers: dict[MotionCommand, IMotionTrigger] = {
            cmd: MotionTrigger(delegate=dependencies.delegate, command=cmd)
            for cmd in cls.DIRECTIONAL_COMMANDS
        }
        return MotionDpadProvides(
            section=MotionDpadSection(
                parent=dependencies.parent,
                delegate=dependencies.delegate,
                triggers=triggers,
            )
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
