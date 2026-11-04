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
    Defines factory creating binary codec adapter provisions.
'''

from __future__ import annotations

from botracked.infrastructure.codec.codec import BinaryCodec
from botracked.infrastructure.codec.dependencies import CodecDependencies
from botracked.infrastructure.codec.provides import CodecProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CodecFactory:
    '''
        Defines class CodecFactory with classmethod(s).
        Factory creating binary codec adapter provisions.

        It defines:

            :methods:
                | create - Instantiates and encapsulates binary codec adapter.
                | get_version - Returns factory component version string.
    '''

    @classmethod
    def create(cls, dependencies: CodecDependencies) -> CodecProvides:
        '''
            Instantiates and encapsulates binary codec adapter.

            :param dependencies: Parameter bundle with CRC calculator port.
            :return: Provisions container with binary codec interface.
            :exceptions: None.
        '''
        codec: BinaryCodec = BinaryCodec(dependencies.crc_calculator)

        return CodecProvides(codec=codec)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
