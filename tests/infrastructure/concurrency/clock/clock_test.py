# -*- coding: UTF-8 -*-

'''
Module
    clock_test.py
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
    Unit tests for Clock system time adapter.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.infrastructure.concurrency.clock.clock import Clock

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ClockTest(TestCase):
    '''
        Verifies Clock monotonic, wall-clock now, and string formatting.
    '''

    def test_monotonic_now_and_str(self) -> None:
        '''
            Verifies monotonic non-decreasing behavior and positive epoch time.

            :exceptions: None.
        '''
        clock = Clock()
        first = clock.monotonic()
        second = clock.monotonic()
        self.assertGreaterEqual(second, first)
        self.assertGreater(clock.now(), 0.0)
        self.assertIn('Clock', str(clock))


if __name__ == '__main__':
    main()
