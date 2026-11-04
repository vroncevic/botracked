# -*- coding: UTF-8 -*-

'''
Module
    panel.py
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
    Provides ConnectionPanel composite UI component managing serial links.
'''

from __future__ import annotations

from tkinter import LEFT
from tkinter.ttk import Frame
from typing import ClassVar

from botracked.core.model.connection_params import ConnectionParams
from botracked.core.model.connection_preference import ConnectionPreference
from botracked.core.model.exceptions.preferences_error import PreferencesError
from botracked.core.service.connection.preferences.irepository import IConnectionPreferencesRepository
from botracked.infrastructure.gui.connection.dependencies import ConnectionPanelDependencies
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

class ConnectionPanel:
    '''
        Defines class ConnectionPanel implementing IConnectionPanel.
        Composite toolbar panel coordinating serial section and status badge.

        It defines:

            :attributes:
                | DEFAULT_TIMEOUT - Serial link connection timeout in seconds.
                | SECTION_PADX - Horizontal padding around child sections.
                | MSG_DISCONNECTED - Status caption displayed on disconnect.
                | _frame - Main container Frame widget.
                | _delegate - Strongly-typed connection action delegate port.
                | _preferences_repo - Repository port for connection persistence.
                | _serial_section - Injected serial port leaf section port.
                | _status_section - Injected status badge leaf section port.
            :methods:
                | __init__ - Initializes connection panel with dependencies.
                | get_widget - Returns root container Frame widget.
                | set_connection_state - Updates connection state and controls.
                | refresh_ports - Scans available serial ports.
                | on_toggle_connection - Handles connect or disconnect click.
                | on_refresh_ports - Handles request to refresh serial ports.
    '''

    DEFAULT_TIMEOUT: ClassVar[float] = 2.0
    SECTION_PADX: ClassVar[int] = 4
    MSG_DISCONNECTED: ClassVar[str] = 'Disconnected'

    _frame: Frame
    _delegate: IConnectionActionDelegate
    _preferences_repo: IConnectionPreferencesRepository
    _serial_section: ISerialSection
    _status_section: IConnectionStatusSection

    def __init__(self, dependencies: ConnectionPanelDependencies) -> None:
        '''
            Initializes connection panel and mounts injected child sections.

            :param dependencies: Connection panel collaborator ports bundle.
            :exceptions: None.
        '''
        self._frame = dependencies.frame
        self._delegate = dependencies.delegate
        self._preferences_repo = dependencies.preferences_repo
        self._serial_section = dependencies.serial_section
        self._status_section = dependencies.status_section

        self._serial_section.get_widget().pack(
            in_=self._frame, side=LEFT, padx=self.SECTION_PADX
        )
        self._status_section.bind_listener(self)
        self._status_section.get_widget().pack(
            in_=self._frame, side=LEFT, padx=self.SECTION_PADX
        )

    def get_widget(self) -> Frame:
        '''
            Returns root container Frame widget.

            :return: Main Frame widget.
            :exceptions: None.
        '''
        return self._frame

    def set_connection_state(self, is_connected: bool, message: str) -> None:
        '''
            Updates connection state and controls.

            :param is_connected: True if link is active, False otherwise.
            :param message: Text description of connection state.
            :exceptions: None.
        '''
        self._status_section.set_state(is_connected, message)
        self._serial_section.set_enabled(not is_connected)

    def refresh_ports(self) -> None:
        '''
            Scans available serial ports.

            :exceptions: None.
        '''
        self._serial_section.refresh_ports()

    def on_toggle_connection(self) -> None:
        '''
            Handles connect or disconnect click and updates UI state.

            :exceptions: None.
        '''
        if self._status_section.is_connected():
            self._delegate.handle_disconnect()
            self.set_connection_state(False, self.MSG_DISCONNECTED)
            return

        port: str = self._serial_section.get_port()
        baud: int = self._serial_section.get_baud()
        try:
            self._preferences_repo.save_preference(
                ConnectionPreference(port=port, baud=baud)
            )
        except PreferencesError:
            pass

        params = ConnectionParams(
            serial_port=port,
            baud_rate=baud,
            timeout=self.DEFAULT_TIMEOUT,
        )
        connected, message = self._delegate.handle_connect(params)
        self.set_connection_state(connected, message)

    def on_refresh_ports(self) -> None:
        '''
            Handles request to refresh available serial ports.

            :exceptions: None.
        '''
        self.refresh_ports()
