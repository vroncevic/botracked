# -*- coding: UTF-8 -*-

'''
Module
    irunner.py
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
    Defines IGuiLifecycleRunner protocol for Tkinter mainloop and shutdown.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@runtime_checkable
class IGuiLifecycleRunner(Protocol):
    '''
        Defines structural contract IGuiLifecycleRunner for GUI event loop.

        It defines:

            :methods:
                | start - Launches the Tkinter main event loop.
                | stop - Stops background workers, disconnects link, destroys UI.
                | is_closing - Checks whether shutdown has been initiated.
    '''

    def start(self) -> None:
        '''
            Launches the Tkinter main event loop.
        '''

    def stop(self) -> None:
        '''
            Stops background workers, disconnects serial link, destroys window.
        '''

    def is_closing(self) -> bool:
        '''
            Checks whether shutdown has been initiated.

            :return: True if closing or closed, False otherwise.
        '''
