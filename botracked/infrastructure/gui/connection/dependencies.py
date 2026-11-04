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
    Defines ConnectionPanelDependencies bundle for ConnectionPanelFactory.
'''

from __future__ import annotations

from dataclasses import dataclass
from tkinter.ttk import Frame

from botracked.core.service.connection.preferences.irepository import IConnectionPreferencesRepository
from botracked.infrastructure.gui.connection.idelegate import IConnectionActionDelegate
from botracked.infrastructure.gui.connection.serial.isection import ISerialSection
from botracked.infrastructure.gui.connection.status.isection import IConnectionStatusSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@dataclass(frozen=True, slots=True)
class ConnectionPanelDependencies:
    '''
        Immutable collaborator bundle injected into ConnectionPanelFactory.

        It defines:

            :attributes:
                | frame - Container Frame widget for connection panel.
                | delegate - Connection action delegate port.
                | preferences_repo - Connection preferences repository port.
                | serial_section - Injected serial input leaf section port.
                | status_section - Injected status badge leaf section port.
    '''

    frame: Frame
    delegate: IConnectionActionDelegate
    preferences_repo: IConnectionPreferencesRepository
    serial_section: ISerialSection
    status_section: IConnectionStatusSection
