# -*- coding: UTF-8 -*-

'''
Module
    runner.py
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
    Provides GuiLifecycleRunner managing Tkinter mainloop and graceful shutdown.
'''

from __future__ import annotations

from tkinter import TclError, Tk

from botracked.core.model.exceptions.botracked_error import BotrackedError
from botracked.core.service.connection.iservice import IBotConnectionService
from botracked.core.service.motion.runner.irunner import IMissionRunner
from botracked.core.service.telemetry.listener.ilistener import ITelemetryListener
from botracked.core.service.telemetry.poller.ipoller import ITelemetryPoller
from botracked.infrastructure.gui.lifecycle.dependencies import GuiLifecycleDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiLifecycleRunner:
    '''
        Defines class GuiLifecycleRunner implementing IGuiLifecycleRunner
        contract structurally.

        It defines:

            :attributes:
                | _root - Root Tk window instance.
                | _connection_service - Link connection service port.
                | _listener - Background telemetry listener port.
                | _poller - Background telemetry poller port.
                | _mission_runner - Asynchronous mission runner port.
                | _closing - Flag indicating shutdown has been initiated.
            :methods:
                | __init__ - Initializes lifecycle runner with dependency bundle.
                | start - Launches the Tkinter event loop.
                | stop - Stops telemetry, aborts missions, closes link, destroys UI.
                | is_closing - Returns True if shutdown was initiated.
    '''

    _root: Tk
    _connection_service: IBotConnectionService
    _listener: ITelemetryListener
    _poller: ITelemetryPoller
    _mission_runner: IMissionRunner
    _closing: bool

    def __init__(self, dependencies: GuiLifecycleDependencies) -> None:
        '''
            Initializes lifecycle runner with window and service contracts.

            :param dependencies: Lifecycle collaborator ports bundle.
            :exceptions: None.
        '''
        self._root = dependencies.root
        self._connection_service = dependencies.connection_service
        self._listener = dependencies.listener
        self._poller = dependencies.poller
        self._mission_runner = dependencies.mission_runner
        self._closing = False

    def start(self) -> None:
        '''
            Launches the Tkinter event loop.

            :exceptions: None.
        '''
        self._closing = False
        self._root.mainloop()

    def stop(self) -> None:
        '''
            Stops telemetry, aborts missions, disconnects hardware, destroys UI.

            :exceptions: None.
        '''
        self._closing = True
        try:
            self._poller.stop()
        except (BotrackedError, RuntimeError):
            pass
        try:
            self._listener.stop()
        except (BotrackedError, RuntimeError):
            pass
        try:
            self._mission_runner.abort()
        except (BotrackedError, RuntimeError):
            pass
        try:
            self._connection_service.disconnect()
        except (BotrackedError, RuntimeError):
            pass
        try:
            self._root.destroy()
        except (TclError, RuntimeError):
            pass

    def is_closing(self) -> bool:
        '''
            Returns True if shutdown has been initiated.

            :return: Boolean shutdown state.
            :exceptions: None.
        '''
        return self._closing
