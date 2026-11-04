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
    Defines DriverFactory assembling synchronized serial driver provisions.
'''

from __future__ import annotations

from threading import RLock
from serial import Serial

from botracked.infrastructure.connection.driver.control import RawSerialControl
from botracked.infrastructure.connection.driver.dependencies import DriverDependencies
from botracked.infrastructure.connection.driver.driver import SerialDriver
from botracked.infrastructure.connection.driver.provides import DriverProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DriverFactory:
    '''
        Defines class DriverFactory with classmethod(s).
        Factory creating synchronized serial driver provisions.

        It defines:

            :methods:
                | create - Instantiates and encapsulates serial driver adapter.
                | get_version - Returns factory component version string.
    '''

    @classmethod
    def create(cls, dependencies: DriverDependencies) -> DriverProvides:
        '''
            Instantiates and encapsulates synchronized serial driver adapter.

            :param dependencies: Parameter bundle with port timeout settings.
            :return: Provisions container with synchronized driver interface.
            :exceptions: None.
        '''
        raw_serial: Serial = Serial(
            timeout=dependencies.timeout,
            write_timeout=dependencies.timeout,
            inter_byte_timeout=dependencies.inter_byte_timeout,
        )
        lock: RLock = RLock()
        control: RawSerialControl = RawSerialControl(raw_serial)
        driver: SerialDriver = SerialDriver(
            control=control,
            io=raw_serial,
            lock=lock,
        )
        return DriverProvides(driver=driver)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
