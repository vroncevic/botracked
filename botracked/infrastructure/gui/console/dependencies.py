# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Defines ConsolePanelDependencies bundle for ConsolePanelFactory.
'''

from __future__ import annotations

from dataclasses import dataclass
from tkinter.ttk import Frame

from botracked.infrastructure.gui.console.stream.isection import IConsoleStreamSection
from botracked.infrastructure.gui.console.toolbar.isection import IConsoleToolbarSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@dataclass(frozen=True, slots=True)
class ConsolePanelDependencies:
    '''
        Immutable collaborator bundle injected into ConsolePanelFactory.

        It defines:

            :attributes:
                | frame - Root container Frame widget.
                | stream_section - Injected console stream leaf section port.
                | toolbar_section - Injected console toolbar leaf section port.
    '''

    frame: Frame
    stream_section: IConsoleStreamSection
    toolbar_section: IConsoleToolbarSection
