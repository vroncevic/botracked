# -*- coding: UTF-8 -*-

'''
Module
    section.py
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
    Defines ConnectionStatusSection leaf UI component for status badge and button.
'''

from __future__ import annotations

from tkinter import LEFT, StringVar, Tk
from tkinter.ttk import Button, Frame, Label
from typing import ClassVar

from botracked.infrastructure.gui.connection.status.ilistener import IConnectionControlListener
from botracked.infrastructure.gui.theme.colors import UIColors

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class ConnectionStatusSection:
    '''
        Defines class ConnectionStatusSection implementing IConnectionStatusSection.
        Leaf UI section presenting connection status badge and toggle button.

        It defines:

            :attributes:
                | INITIAL_STATUS - Initial offline badge caption.
                | BTN_CONNECT - Button caption when link is disconnected.
                | BTN_DISCONNECT - Button caption when link is connected.
                | WIDGET_PADX - Horizontal padding around status widgets.
                | _frame - Sub-container Frame widget.
                | _status_var - Bound StringVar for status display.
                | _status_lbl - Label widget for status badge.
                | _toggle_btn - Button widget for toggling connection.
                | _is_connected - Boolean flag tracking link status.
            :methods:
                | __init__ - Initializes status section and mounts widgets.
                | get_widget - Returns section container Frame widget.
                | bind_listener - Binds toggle button command to listener.
                | set_state - Updates badge label and toggle button state.
                | is_connected - Returns boolean indicating connection state.
    '''

    INITIAL_STATUS: ClassVar[str] = 'Disconnected'
    BTN_CONNECT: ClassVar[str] = 'Connect'
    BTN_DISCONNECT: ClassVar[str] = 'Disconnect'
    WIDGET_PADX: ClassVar[int] = 6

    _frame: Frame
    _status_var: StringVar
    _status_lbl: Label
    _toggle_btn: Button
    _is_connected: bool

    def __init__(self, parent: Frame | Tk) -> None:
        '''
            Initializes status section and mounts widgets.

            :param parent: Parent container widget.
            :exceptions: None.
        '''
        self._frame = Frame(parent, style='Surface.TFrame')
        self._is_connected = False
        self._status_var = StringVar(value=self.INITIAL_STATUS)
        self._status_lbl = Label(
            self._frame,
            textvariable=self._status_var,
            style='Surface.TLabel',
            foreground=UIColors.RED,
        )
        self._status_lbl.pack(side=LEFT, padx=self.WIDGET_PADX)
        self._toggle_btn = Button(self._frame, text=self.BTN_CONNECT)
        self._toggle_btn.pack(side=LEFT, padx=self.WIDGET_PADX)

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
            :exceptions: None.
        '''
        return self._frame

    def bind_listener(self, listener: IConnectionControlListener) -> None:
        '''
            Binds toggle button command to control listener.

            :param listener: Strongly-typed connection control listener.
            :exceptions: None.
        '''
        self._toggle_btn.configure(command=listener.on_toggle_connection)

    def set_state(self, is_connected: bool, text: str) -> None:
        '''
            Updates badge label and toggle button state.

            :param is_connected: True if connected, False otherwise.
            :param text: Text description of connection state.
            :exceptions: None.
        '''
        self._is_connected = is_connected
        self._status_var.set(text)
        color: str = str(UIColors.GREEN if is_connected else UIColors.RED)
        self._status_lbl.configure(foreground=color)
        btn_text: str = (
            self.BTN_DISCONNECT if is_connected else self.BTN_CONNECT
        )
        self._toggle_btn.configure(text=btn_text)

    def is_connected(self) -> bool:
        '''
            Returns boolean indicating current connection state.

            :return: True if connected, False otherwise.
            :exceptions: None.
        '''
        return self._is_connected
