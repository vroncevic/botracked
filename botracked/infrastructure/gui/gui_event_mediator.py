# -*- coding: UTF-8 -*-

'''
Module
    gui_event_mediator.py
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
    Provides GuiEventMediator routing events from background threads to GUI widgets.
'''

from __future__ import annotations

from tkinter import Tk

from botracked.core.model.telemetry_data import TelemetryData
from botracked.infrastructure.gui.connection.connection_panel import (
    ConnectionPanel,
)
from botracked.infrastructure.gui.stream.log_panel import LogPanel
from botracked.infrastructure.gui.telemetry.telemetry_panel import (
    TelemetryPanel,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiEventMediator:
    '''
        Defines class GuiEventMediator with attribute(s) and method(s).
        Thread-safe event bridge between BotService worker threads and Tkinter UI widgets.

        It defines:

            :attributes:
                | _root - Root Tkinter application window instance.
                | _conn_panel - Connection panel widget component.
                | _telem_panel - Live telemetry panel widget component.
                | _log_panel - Packet stream log panel widget component.
            :methods:
                | __init__ - Initializes event mediator with UI components.
                | on_telemetry_updated - Schedules telemetry UI updates.
                | on_connection_state_changed - Schedules connection state updates.
                | on_packet_logged - Schedules packet stream log displays.
    '''

    _root: Tk
    _conn_panel: ConnectionPanel
    _telem_panel: TelemetryPanel
    _log_panel: LogPanel

    def __init__(
        self,
        root: Tk,
        conn_panel: ConnectionPanel,
        telem_panel: TelemetryPanel,
        log_panel: LogPanel,
    ) -> None:
        '''
            Initializes event mediator with UI components.

            :param root: Root Tkinter application window instance.
            :param conn_panel: Connection panel component.
            :param telem_panel: Telemetry display component.
            :param log_panel: Packet stream log component.
            :exceptions: None.
        '''
        self._root = root
        self._conn_panel = conn_panel
        self._telem_panel = telem_panel
        self._log_panel = log_panel

    def on_telemetry_updated(self, telemetry: TelemetryData) -> None:
        '''
            Receives telemetry update from background thread and schedules UI update.

            :param telemetry: Updated TelemetryData record.
            :exceptions: None.
        '''
        try:
            self._root.after(0, lambda: self._telem_panel.update_telemetry(telemetry))
        except Exception:
            pass

    def on_connection_state_changed(self, is_connected: bool, message: str) -> None:
        '''
            Receives connection state change and schedules UI update.

            :param is_connected: True if connected.
            :param message: Status description.
            :exceptions: None.
        '''
        try:
            self._root.after(
                0, lambda: self._conn_panel.set_connection_state(is_connected, message)
            )
        except Exception:
            pass

    def on_packet_logged(self, direction: str, opcode_name: str, raw_hex: str) -> None:
        '''
            Receives packet trace and schedules log display.

            :param direction: Direction indicator (TX or RX).
            :param opcode_name: Opcode name string.
            :param raw_hex: Hex data representation.
            :exceptions: None.
        '''
        try:
            self._root.after(
                0, lambda: self._log_panel.append_packet(direction, opcode_name, raw_hex)
            )
        except Exception:
            pass
