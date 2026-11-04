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
    Defines MissionStatusFactory assembling MissionStatusSection.
'''

from __future__ import annotations

from botracked.infrastructure.gui.mission.status.dependencies import MissionStatusDependencies
from botracked.infrastructure.gui.mission.status.provides import MissionStatusProvides
from botracked.infrastructure.gui.mission.status.section import MissionStatusSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionStatusFactory:
    '''
        Defines class MissionStatusFactory assembling MissionStatusSection.

        It defines:

            :methods:
                | create - Creates MissionStatusProvides from dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls, dependencies: MissionStatusDependencies
    ) -> MissionStatusProvides:
        '''
            Creates MissionStatusProvides from MissionStatusDependencies.

            :param dependencies: Status section collaborators bundle.
            :return: Wired MissionStatusProvides bundle.
            :exceptions: None.
        '''
        section = MissionStatusSection(parent=dependencies.parent)

        return MissionStatusProvides(section=section)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
