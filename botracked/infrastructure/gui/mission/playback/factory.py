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
    Defines MissionPlaybackFactory assembling MissionPlaybackSection.
'''

from __future__ import annotations

from botracked.infrastructure.gui.mission.playback.dependencies import MissionPlaybackDependencies
from botracked.infrastructure.gui.mission.playback.provides import MissionPlaybackProvides
from botracked.infrastructure.gui.mission.playback.section import MissionPlaybackSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionPlaybackFactory:
    '''
        Defines class MissionPlaybackFactory assembling MissionPlaybackSection.

        It defines:

            :methods:
                | create - Creates MissionPlaybackProvides from dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls, dependencies: MissionPlaybackDependencies
    ) -> MissionPlaybackProvides:
        '''
            Creates MissionPlaybackProvides from MissionPlaybackDependencies.

            :param dependencies: Playback section collaborators bundle.
            :return: Wired MissionPlaybackProvides bundle.
            :exceptions: None.
        '''
        return MissionPlaybackProvides(
            section=MissionPlaybackSection(dependencies=dependencies)
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
