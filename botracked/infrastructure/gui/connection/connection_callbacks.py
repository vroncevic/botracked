# -*- coding: UTF-8 -*-

'''
Module
    connection_callbacks.py
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
    Parameter bundle encapsulating callbacks for communication link connection.
'''

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from botracked.core.model.connection_params import ConnectionParams

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class ConnectionCallbacks:
    '''
        Defines class ConnectionCallbacks with attribute(s) and method(s).
        Parameter bundle encapsulating event callbacks for transport link management.

        It defines:

            :attributes:
                | on_connect - Callback invoked to establish hardware connection.
                | on_disconnect - Callback invoked to terminate hardware connection.
            :methods: None.
    '''

    on_connect: Callable[[ConnectionParams], bool]
    on_disconnect: Callable[[], None]
