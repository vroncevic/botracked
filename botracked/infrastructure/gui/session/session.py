# -*- coding: UTF-8 -*-

'''
Module
    session.py
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
    Provides GuiSession coordinating mounted mission panel and lifecycle runner.
'''

from __future__ import annotations

from botracked.infrastructure.gui.lifecycle.irunner import IGuiLifecycleRunner
from botracked.infrastructure.gui.mission.ipanel import IMissionPanel

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class GuiSession:
    '''
        Defines class GuiSession implementing IGuiSession contract.
        Encapsulates an active mounted Tk session without exposing Tkinter types.

        It defines:

            :attributes:
                | _mission_panel - Mission routine panel contract.
                | _lifecycle_runner - Lifecycle event loop runner contract.
            :methods:
                | __init__ - Initializes session with mission panel and runner.
                | set_script - Loads mission script into active mission editor.
                | start - Starts Tkinter mainloop via lifecycle runner.
                | stop - Stops lifecycle runner and closes window.
    '''

    _mission_panel: IMissionPanel
    _lifecycle_runner: IGuiLifecycleRunner

    def __init__(
        self,
        mission_panel: IMissionPanel,
        lifecycle_runner: IGuiLifecycleRunner,
    ) -> None:
        '''
            Initializes session with mission panel and lifecycle runner.

            :param mission_panel: Mounted mission routine panel port.
            :param lifecycle_runner: Mounted GUI lifecycle runner port.
            :exceptions: None.
        '''
        self._mission_panel = mission_panel
        self._lifecycle_runner = lifecycle_runner

    def set_script(self, script_text: str) -> None:
        '''
            Loads mission script into active mission editor.

            :param script_text: Raw .track script text.
            :exceptions: None.
        '''
        self._mission_panel.set_script(script_text)

    def start(self) -> None:
        '''
            Starts Tkinter mainloop via lifecycle runner.

            :exceptions: None.
        '''
        self._lifecycle_runner.start()

    def stop(self) -> None:
        '''
            Stops lifecycle runner and closes window.

            :exceptions: None.
        '''
        self._lifecycle_runner.stop()
