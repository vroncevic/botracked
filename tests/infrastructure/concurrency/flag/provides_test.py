# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for SignalFlagProvides immutable output bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.infrastructure.concurrency.flag.provides import SignalFlagProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SignalFlagProvidesTest(TestCase):
    '''
        Verifies SignalFlagProvides attribute storage and immutability.
    '''

    def test_provides_storage_and_frozen(self) -> None:
        '''
            Verifies flag field preservation and FrozenInstanceError on write.

            :exceptions: None.
        '''
        flag = Mock(spec=ISignalFlag)
        prov = SignalFlagProvides(flag=flag)
        self.assertIs(prov.flag, flag)
        with self.assertRaises(FrozenInstanceError):
            setattr(prov, 'flag', flag)


if __name__ == '__main__':
    main()
