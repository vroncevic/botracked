# -*- coding: UTF-8 -*-

'''
Module
    iconfigurator.py
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
    Defines IWindowConfigurator protocol for root window setup.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.infrastructure.gui.lifecycle.irunner import IGuiLifecycleRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@runtime_checkable
class IWindowConfigurator(Protocol):
    '''
        Defines structural contract IWindowConfigurator for Tk window setup.

        It defines:

            :methods:
                | configure - Applies title, geometry, background, and theme.
                | bind_close_handler - Binds shutdown handler to WM_DELETE_WINDOW.
    '''

    def configure(self) -> None:
        '''
            Applies title, geometry, minimum size, background, and theme.
        '''

    def bind_close_handler(self, runner: IGuiLifecycleRunner) -> None:
        '''
            Binds shutdown handler to WM_DELETE_WINDOW protocol.

            :param runner: Strongly-typed GUI lifecycle runner.
        '''
