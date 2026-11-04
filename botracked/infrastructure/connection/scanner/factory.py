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
    Defines ScannerFactory assembling PortScanner infrastructure adapter.
'''

from __future__ import annotations

from botracked.infrastructure.connection.scanner.dependencies import ScannerDependencies
from botracked.infrastructure.connection.scanner.provides import ScannerProvides
from botracked.infrastructure.connection.scanner.scanner import PortScanner

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScannerFactory:
    '''
        Defines class ScannerFactory assembling PortScanner subsystem.

        It defines:

            :methods:
                | create - Creates ScannerProvides from ScannerDependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: ScannerDependencies) -> ScannerProvides:
        '''
            Creates ScannerProvides from ScannerDependencies.

            :param dependencies: Configuration bundle specifying symlink enumeration.
            :return: Assembled ScannerProvides bundle.
            :exceptions: None.
        '''
        scanner = PortScanner(include_links=dependencies.include_links)

        return ScannerProvides(scanner=scanner)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
