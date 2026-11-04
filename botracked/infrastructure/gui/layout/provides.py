# -*- coding: UTF-8 -*-

'''
Module
    provides.py
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
    Defines LayoutProvides bundle exposing ILayoutBuilder port.
'''

from __future__ import annotations

from dataclasses import dataclass

from botracked.infrastructure.gui.layout.ibuilder import ILayoutBuilder
from botracked.infrastructure.gui.layout.slots import LayoutSlots

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@dataclass(frozen=True, slots=True)
class LayoutProvides:
    '''
        Immutable output bundle exposing assembled layout builder contract.

        It defines:

            :attributes:
                | builder - Window split-pane layout builder port.
                | slots - Native split-pane container frames bundle.
    '''

    builder: ILayoutBuilder
    slots: LayoutSlots
