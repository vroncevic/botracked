# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Defines MissionWorkerDependencies immutable collaborator bundle.
'''

from __future__ import annotations

from dataclasses import dataclass

from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.motion.protocol.iactuator import IMissionActuator
from botracked.core.service.motion.runner.pacer.ipacer import IMissionPacer

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class MissionWorkerDependencies:
    '''
        Immutable collaborator bundle injected into MissionWorkerFactory.

        It defines:

            :attributes:
                | pacer - Mission pacer port handling step delays and pauses.
                | actuator - Narrow actuator port executing steps and stop.
                | stop_flag - Signal flag indicating mission cancellation.
    '''

    pacer: IMissionPacer
    actuator: IMissionActuator
    stop_flag: ISignalFlag
