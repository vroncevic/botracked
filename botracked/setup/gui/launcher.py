# -*- coding: UTF-8 -*-

'''
Module
    launcher.py
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
    Provides GuiSessionLauncher lazily creating Tk sessions at launch time.
'''

from __future__ import annotations

from typing import ClassVar

from ats_utilities.utils.reflection import to_str

from botracked.infrastructure.gui.session.isession import IGuiSession
from botracked.setup.gui.dependencies import BotGuiSessionDependencies
from botracked.setup.gui.factory import BotGuiSessionFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiSessionLauncher:
    '''
        Defines class GuiSessionLauncher implementing IGUI contract structurally.
        Defers X11/Tk display initialization until studio command execution.

        It defines:

            :attributes:
                | EMPTY_SCRIPT - Default empty initial script constant.
                | _dependencies - Stored GUI session collaborator ports bundle.
                | _sessions - Active mounted GUI sessions collection.
                | _initial_script - Buffered .track script text prior to launch.
                | _is_initialized - Readiness flag for engine validation.
            :methods:
                | __init__ - Initializes launcher with GUI session dependencies.
                | is_initialized - Checks if GUI adapter is ready.
                | load_script - Buffers and forwards mission script text.
                | start - Creates Tk session, applies script, starts loop.
                | stop - Stops and removes all active GUI sessions cleanly.
                | __str__ - Returns string representation of session launcher.
    '''

    EMPTY_SCRIPT: ClassVar[str] = ''

    _dependencies: BotGuiSessionDependencies
    _sessions: list[IGuiSession]
    _initial_script: str
    _is_initialized: bool

    def __init__(self, dependencies: BotGuiSessionDependencies) -> None:
        '''
            Initializes launcher with GUI session collaborator ports bundle.

            :param dependencies: GUI session collaborator ports bundle.
            :exceptions: None.
        '''
        self._dependencies = dependencies
        self._sessions = []
        self._initial_script = self.EMPTY_SCRIPT
        self._is_initialized = True

    def is_initialized(self) -> bool:
        '''
            Checks if GUI adapter is ready.

            :return: True if ready, False otherwise.
            :exceptions: None.
        '''
        return self._is_initialized

    def load_script(self, script_text: str) -> None:
        '''
            Buffers and forwards mission routine script into studio.

            :param script_text: Raw .track script text.
            :exceptions: None.
        '''
        self._initial_script = script_text
        for session in self._sessions:
            session.set_script(script_text)

    def start(self) -> None:
        '''
            Creates Tk session, applies optional script, and runs event loop.

            :exceptions: None.
        '''
        session: IGuiSession = BotGuiSessionFactory.create(self._dependencies)
        self._sessions.append(session)
        if self._initial_script:
            session.set_script(self._initial_script)
        session.start()

    def stop(self) -> None:
        '''
            Stops and clears all active GUI sessions cleanly.

            :exceptions: None.
        '''
        while self._sessions:
            self._sessions.pop().stop()

    def __str__(self) -> str:
        '''
            Returns string representation of session launcher.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
