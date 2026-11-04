# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Provides GuiPanelsBundle parameter bundle holding top-level panel ports.
'''

from __future__ import annotations

from dataclasses import dataclass

from botracked.infrastructure.gui.connection.ipanel import IConnectionPanel
from botracked.infrastructure.gui.console.ipanel import IConsolePanel
from botracked.infrastructure.gui.mission.ipanel import IMissionPanel
from botracked.infrastructure.gui.motion.ipanel import IMotionPanel
from botracked.infrastructure.gui.telemetry.ipanel import ITelemetryPanel

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@dataclass(frozen=True, slots=True)
class GuiPanelsBundle:
    '''
        Immutable parameter bundle grouping primary GUI panel contracts.

        It defines:

            :attributes:
                | connection - Serial connection configuration panel port.
                | mission - Mission routine editor and controls panel port.
                | motion - Manual steering and speed control panel port.
                | telemetry - Live telemetry dashboard panel port.
                | console - Packet stream and diagnostic console panel port.
    '''

    connection: IConnectionPanel
    mission: IMissionPanel
    motion: IMotionPanel
    telemetry: ITelemetryPanel
    console: IConsolePanel
