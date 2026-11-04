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
    Defines SerialSection leaf UI component for serial port configuration.
'''

from __future__ import annotations

from tkinter import LEFT, StringVar, Tk
from tkinter.ttk import Button, Combobox, Frame, Label
from typing import ClassVar

from botracked.infrastructure.gui.connection.iport_delegate import IPortRefreshDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class SerialSection:
    '''
        Defines class SerialSection implementing ISerialSection contract.
        Leaf UI section presenting serial port combobox, refresh button, and baud.

        It defines:

            :attributes:
                | BAUD_VALUES - Standard supported UART baud rates.
                | FALLBACK_BAUD - Fallback baud rate when input text is invalid.
                | PORT_WIDTH - Character width of port combobox.
                | BAUD_WIDTH - Character width of baud combobox.
                | REFRESH_WIDTH - Character width of refresh button.
                | WIDGET_PADX - Horizontal padding around child controls.
                | STATE_NORMAL - Interactive ttk widget state string.
                | STATE_READONLY - Read-only combobox state string.
                | STATE_DISABLED - Disabled ttk widget state string.
                | _frame - Sub-container Frame widget.
                | _delegate - Narrow port refresh delegate port.
                | _port_var - Bound StringVar for selected serial port.
                | _baud_var - Bound StringVar for selected baud rate.
                | _port_combo - Combobox widget for port selection.
                | _baud_combo - Combobox widget for baud rate selection.
                | _refresh_btn - Button widget for refreshing port list.
            :methods:
                | __init__ - Initializes serial section and mounts widgets.
                | get_widget - Returns section container Frame widget.
                | get_port - Returns selected serial port string.
                | get_baud - Returns selected baud rate integer.
                | refresh_ports - Scans serial ports and refreshes combobox items.
                | set_enabled - Enables or disables input controls.
    '''

    BAUD_VALUES: ClassVar[tuple[str, ...]] = (
        '9600', '19200', '38400', '57600', '115200'
    )
    FALLBACK_BAUD: ClassVar[int] = 9600
    PORT_WIDTH: ClassVar[int] = 14
    BAUD_WIDTH: ClassVar[int] = 8
    REFRESH_WIDTH: ClassVar[int] = 3
    WIDGET_PADX: ClassVar[int] = 3
    STATE_NORMAL: ClassVar[str] = 'normal'
    STATE_READONLY: ClassVar[str] = 'readonly'
    STATE_DISABLED: ClassVar[str] = 'disabled'

    _frame: Frame
    _delegate: IPortRefreshDelegate
    _port_var: StringVar
    _baud_var: StringVar
    _port_combo: Combobox
    _baud_combo: Combobox
    _refresh_btn: Button

    def __init__(
        self,
        parent: Frame | Tk,
        delegate: IPortRefreshDelegate,
        default_port: str,
        default_baud: int,
    ) -> None:
        '''
            Initializes serial section and mounts widgets.

            :param parent: Parent container widget.
            :param delegate: Narrow delegate providing port scanning.
            :param default_port: Initial port string value.
            :param default_baud: Initial baud rate integer value.
            :exceptions: None.
        '''
        self._frame = Frame(parent, style='Surface.TFrame')
        self._delegate = delegate
        self._port_var = StringVar(value=default_port)
        self._baud_var = StringVar(value=str(default_baud))

        port_lbl = Label(self._frame, text='Port:', style='Surface.TLabel')
        port_lbl.pack(side=LEFT, padx=self.WIDGET_PADX)
        self._port_combo = Combobox(
            self._frame,
            textvariable=self._port_var,
            width=self.PORT_WIDTH,
        )
        self._port_combo.pack(side=LEFT, padx=self.WIDGET_PADX)

        self._refresh_btn = Button(
            self._frame,
            text='⟳',
            width=self.REFRESH_WIDTH,
            command=self.refresh_ports,
        )
        self._refresh_btn.pack(side=LEFT, padx=self.WIDGET_PADX)

        baud_lbl = Label(self._frame, text='Baud:', style='Surface.TLabel')
        baud_lbl.pack(side=LEFT, padx=self.WIDGET_PADX)
        self._baud_combo = Combobox(
            self._frame,
            textvariable=self._baud_var,
            values=self.BAUD_VALUES,
            width=self.BAUD_WIDTH,
            state=self.STATE_READONLY,
        )
        self._baud_combo.pack(side=LEFT, padx=self.WIDGET_PADX)

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
            :exceptions: None.
        '''
        return self._frame

    def get_port(self) -> str:
        '''
            Returns selected serial port string.

            :return: Serial port path string.
            :exceptions: None.
        '''
        return self._port_var.get()

    def get_baud(self) -> int:
        '''
            Returns selected baud rate integer.

            :return: Baud rate integer value.
            :exceptions: None.
        '''
        try:
            return int(self._baud_var.get())
        except ValueError:
            return self.FALLBACK_BAUD

    def refresh_ports(self) -> None:
        '''
            Scans serial ports and refreshes combobox items.

            :exceptions: None.
        '''
        ports: tuple[str, ...] = self._delegate.handle_refresh_ports()
        self._port_combo['values'] = ports
        if ports and self._port_var.get() not in ports:
            self._port_var.set(ports[0])

    def set_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables input controls.

            :param enabled: True if controls should be interactive, False otherwise.
            :exceptions: None.
        '''
        state_str: str = self.STATE_NORMAL if enabled else self.STATE_DISABLED
        baud_state: str = (
            self.STATE_READONLY if enabled else self.STATE_DISABLED
        )
        self._port_combo.configure(state=state_str)
        self._refresh_btn.configure(state=state_str)
        self._baud_combo.configure(state=baud_state)
