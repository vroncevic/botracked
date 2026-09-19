# -*- coding: UTF-8 -*-

'''
Module
    connection_panel.py
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
    Provides ConnectionPanel for configuring and managing transport links.
'''

from __future__ import annotations

from os.path import exists
from tkinter import LEFT, StringVar
from tkinter.ttk import Button, Combobox, Frame, Label

from botracked.core.model.connection_params import ConnectionParams
from botracked.infrastructure.communication.preferences.connection_preferences_repository import (
    ConnectionPreferencesRepository,
)
from botracked.infrastructure.communication.serial_transport import (
    SerialTransport,
)
from botracked.infrastructure.gui.connection.connection_callbacks import (
    ConnectionCallbacks,
)
from botracked.infrastructure.gui.connection.connection_panel_config import (
    ConnectionPanelConfig,
)
from botracked.infrastructure.gui.theme.colors import UIColors

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionPanel:
    '''
        Defines class ConnectionPanel with attribute(s) and method(s).
        Toolbar panel for hardware serial port and wireless connection.

        It defines:

            :attributes:
                | _frame - Main container Frame widget.
                | _callbacks - ConnectionCallbacks bundle.
                | _preferences_repo - Repository for saved preferences.
                | _config - Configuration parameters holding UI literals.
                | _port_var - String variable binding selected port.
                | _baud_var - String variable binding selected baud rate.
                | _status_var - String variable binding status text.
                | _port_combo - Dropdown combobox for port selection.
                | _status_lbl - Label widget displaying status badge.
                | _toggle_btn - Connect/Disconnect toggle button widget.
                | _is_connected - Boolean flag tracking connected state.
            :methods:
                | __init__ - Initializes connection panel components.
                | get_widget - Returns root Frame widget.
                | refresh_ports - Scans OS for serial devices and populates list.
                | set_connection_state - Updates UI indicators on state change.
                | _build_ui - Constructs internal widget hierarchy.
                | _handle_toggle - Handles connect/disconnect button click event.
    '''

    _frame: Frame
    _callbacks: ConnectionCallbacks
    _preferences_repo: ConnectionPreferencesRepository
    _config: ConnectionPanelConfig
    _port_var: StringVar
    _baud_var: StringVar
    _status_var: StringVar
    _port_combo: Combobox
    _status_lbl: Label
    _toggle_btn: Button
    _is_connected: bool

    def __init__(
        self,
        parent: Frame,
        callbacks: ConnectionCallbacks,
        preferences_repo: ConnectionPreferencesRepository | None = None,
        config: ConnectionPanelConfig | None = None,
    ) -> None:
        '''
            Initializes connection panel components.

            :param parent: Parent Tk widget.
            :param callbacks: ConnectionCallbacks bundle.
            :param preferences_repo: Optional preferences repository.
            :param config: Optional ConnectionPanelConfig instance.
            :exceptions: None.
        '''
        self._callbacks = callbacks
        self._preferences_repo = (
            preferences_repo
            if preferences_repo is not None
            else ConnectionPreferencesRepository()
        )
        self._config = config if config is not None else ConnectionPanelConfig()
        self._is_connected = False
        self._frame = Frame(
            parent, style='Panel.TFrame', padding=self._config.padding_main
        )
        self._build_ui()

    def get_widget(self) -> Frame:
        '''
            Returns root Frame widget.

            :return: Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def refresh_ports(self) -> None:
        '''
            Scans OS for serial devices and populates dropdown.

            :exceptions: None.
        '''
        cfg: ConnectionPanelConfig = self._config
        ports: list[str] = SerialTransport.list_available_ports()
        if exists(cfg.device_alias) and cfg.device_alias not in ports:
            ports.insert(0, cfg.device_alias)
        if not ports:
            ports = list(cfg.fallback_ports)
        self._port_combo['values'] = ports
        if ports and self._port_var.get() not in ports:
            self._port_var.set(ports[0])

    def set_connection_state(self, is_connected: bool, message: str) -> None:
        '''
            Updates UI indicators based on connection state.

            :param is_connected: True if link is up.
            :param message: Diagnostic description.
            :exceptions: None.
        '''
        cfg: ConnectionPanelConfig = self._config
        self._is_connected = is_connected
        status_text: str = message if message else (
            cfg.status_connected if is_connected else cfg.status_disconnected
        )
        self._status_var.set(status_text)
        if is_connected:
            self._status_lbl.configure(foreground=UIColors.GREEN)
            self._toggle_btn.configure(text=cfg.btn_disconnect, style='Danger.TButton')
            self._port_combo.configure(state='disabled')
        else:
            self._status_lbl.configure(foreground=UIColors.RED)
            self._toggle_btn.configure(text=cfg.btn_connect, style='Success.TButton')
            self._port_combo.configure(state='normal')

    def _init_variables(self) -> None:
        '''
            Initializes bound UI variables from preferences and defaults.

            :exceptions: None.
        '''
        cfg: ConnectionPanelConfig = self._config
        pref_port, pref_baud = self._preferences_repo.load_preference()
        initial_port: str = pref_port or cfg.default_port
        initial_baud: str = str(pref_baud) if pref_baud else cfg.default_baud

        self._port_var = StringVar(value=initial_port)
        self._baud_var = StringVar(value=initial_baud)
        self._status_var = StringVar(value=cfg.status_disconnected)

    def _build_port_selector(self) -> None:
        '''
            Builds dropdown combobox and refresh button for port selection.

            :exceptions: None.
        '''
        cfg: ConnectionPanelConfig = self._config
        Label(self._frame, text=cfg.label_port, style='Panel.TLabel').pack(side=LEFT, padx=(4, 2))
        self._port_combo = Combobox(self._frame, textvariable=self._port_var, width=14)
        self._port_combo.pack(side=LEFT, padx=2)
        self.refresh_ports()

        refresh_btn: Button = Button(
            self._frame, text=cfg.btn_refresh, width=2, command=self.refresh_ports
        )
        refresh_btn.pack(side=LEFT, padx=2)

    def _build_baud_and_actions(self) -> None:
        '''
            Builds baud rate selector, connect toggle button, and status label.

            :exceptions: None.
        '''
        cfg: ConnectionPanelConfig = self._config
        Label(self._frame, text=cfg.label_baud, style='Panel.TLabel').pack(side=LEFT, padx=(6, 2))
        baud_combo: Combobox = Combobox(
            self._frame,
            textvariable=self._baud_var,
            values=list(cfg.baud_rates),
            width=8,
        )
        baud_combo.pack(side=LEFT, padx=2)

        self._toggle_btn = Button(
            self._frame,
            text=cfg.btn_connect,
            style='Success.TButton',
            command=self._handle_toggle,
            width=11,
        )
        self._toggle_btn.pack(side=LEFT, padx=(10, 4))

        self._status_lbl = Label(
            self._frame,
            textvariable=self._status_var,
            style='Panel.TLabel',
            foreground=UIColors.RED,
            font=('Helvetica', 9, 'bold'),
        )
        self._status_lbl.pack(side=LEFT, padx=(12, 4))

    def _build_ui(self) -> None:
        '''
            Constructs internal widget hierarchy and layout.

            :exceptions: None.
        '''
        self._init_variables()
        self._build_port_selector()
        self._build_baud_and_actions()

    def _handle_toggle(self) -> None:
        '''
            Handles connect or disconnect button click events.

            :exceptions: None.
        '''
        if self._is_connected:
            self._callbacks.on_disconnect()
            self.set_connection_state(False, 'Disconnected')
            return

        baud: int = 9600
        try:
            baud = int(self._baud_var.get())
        except ValueError:
            pass
        port: str = self._port_var.get()
        params = ConnectionParams(
            connection_type='SERIAL',
            serial_port=port,
            baud_rate=baud,
        )
        success = self._callbacks.on_connect(params)
        if success:
            self._preferences_repo.save_preference(port=port, baud=baud)
            self.set_connection_state(True, 'Connected')
        else:
            self.set_connection_state(False, 'Connection failed')
