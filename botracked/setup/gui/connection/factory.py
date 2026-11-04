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
    Defines ConnectionFactory assembling the connection GUI toolbar.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from typing import ClassVar

from botracked.core.model.exceptions.preferences_error import PreferencesError
from botracked.infrastructure.gui.connection.adapter.dependencies import ConnectionAdapterDependencies
from botracked.infrastructure.gui.connection.adapter.factory import ConnectionAdapterFactory
from botracked.infrastructure.gui.connection.dependencies import ConnectionPanelDependencies
from botracked.infrastructure.gui.connection.factory import ConnectionPanelFactory
from botracked.infrastructure.gui.connection.ipanel import IConnectionPanel
from botracked.infrastructure.gui.connection.serial.dependencies import SerialSectionDependencies
from botracked.infrastructure.gui.connection.serial.factory import SerialSectionFactory
from botracked.infrastructure.gui.connection.status.dependencies import ConnectionStatusDependencies
from botracked.infrastructure.gui.connection.status.factory import ConnectionStatusFactory
from botracked.setup.gui.connection.dependencies import ConnectionDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionFactory:
    '''
        Defines class ConnectionFactory assembling connection GUI toolbar.

        It defines:

            :attributes:
                | DEFAULT_PORT - Fallback serial port path when none persisted.
                | DEFAULT_BAUD - Fallback baud rate when none persisted.
                | PANEL_STYLE - Surface ttk Frame style identifier.
                | PANEL_PADDING - Horizontal and vertical toolbar padding.
            :methods:
                | create - Wires and returns mounted IConnectionPanel.
                | get_version - Returns factory version string.
    '''

    DEFAULT_PORT: ClassVar[str] = '/dev/ttyACM0'
    DEFAULT_BAUD: ClassVar[int] = 9600
    PANEL_STYLE: ClassVar[str] = 'Surface.TFrame'
    PANEL_PADDING: ClassVar[tuple[int, int]] = (8, 6)

    @classmethod
    def create(
        cls, dependencies: ConnectionDependencies
    ) -> IConnectionPanel:
        '''
            Wires connection adapter, leaf sections, and ConnectionPanel.

            :param dependencies: Connection GUI composition collaborators.
            :return: Assembled IConnectionPanel instance.
            :exceptions: None.
        '''
        default_port: str = cls.DEFAULT_PORT
        default_baud: int = cls.DEFAULT_BAUD
        if dependencies.preferences_repository.has_preference():
            try:
                pref = dependencies.preferences_repository.load_preference()
                default_port = pref.port
                default_baud = pref.baud
            except PreferencesError:
                pass

        adapter_prov = ConnectionAdapterFactory.create(
            ConnectionAdapterDependencies(
                connection_service=dependencies.connection_service,
                listener=dependencies.runners.listener,
                poller=dependencies.runners.poller,
                mission_runner=dependencies.runners.mission,
                port_scanner=dependencies.port_scanner,
                log_listener=dependencies.log_listener,
            )
        )
        conn_frame = Frame(
            dependencies.root,
            style=cls.PANEL_STYLE,
            padding=cls.PANEL_PADDING,
        )
        serial_prov = SerialSectionFactory.create(
            SerialSectionDependencies(
                parent=conn_frame,
                delegate=adapter_prov.port_delegate,
                default_port=default_port,
                default_baud=default_baud,
            )
        )
        status_prov = ConnectionStatusFactory.create(
            ConnectionStatusDependencies(parent=conn_frame)
        )
        panel = ConnectionPanelFactory.create(
            ConnectionPanelDependencies(
                frame=conn_frame,
                delegate=adapter_prov.delegate,
                preferences_repo=dependencies.preferences_repository,
                serial_section=serial_prov.section,
                status_section=status_prov.section,
            )
        ).panel
        panel.refresh_ports()
        return panel

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
