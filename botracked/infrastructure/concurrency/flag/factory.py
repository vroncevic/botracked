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
    Defines SignalFlagFactory instantiating stdlib Event behind ISignalFlag.
'''

from __future__ import annotations

from threading import Event

from botracked.infrastructure.concurrency.flag.provides import SignalFlagProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SignalFlagFactory:
    '''
        Defines class SignalFlagFactory assembling SignalFlagProvides subsystem.

        It defines:

            :attributes: None.
            :methods:
                | create - Creates SignalFlagProvides wrapping threading.Event.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> SignalFlagProvides:
        '''
            Creates SignalFlagProvides wrapping stdlib threading Event.

            :return: Assembled SignalFlagProvides bundle.
            :exceptions: None.
        '''
        return SignalFlagProvides(flag=Event())

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
