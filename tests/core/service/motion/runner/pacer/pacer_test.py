# -*- coding: UTF-8 -*-

'''
Module
    pacer_test.py
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
    Unit tests for MissionPacer.
'''

from __future__ import annotations

from threading import Event, Thread
from time import sleep
from unittest import TestCase, main

from botracked.core.service.motion.runner.pacer.pacer import MissionPacer
from botracked.infrastructure.concurrency.clock.clock import Clock

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionPacerTestCase(TestCase):
    '''
        Verifies MissionPacer pause waiting and cancellable step delays.
    '''

    def setUp(self) -> None:
        '''
            Prepares test fixtures.

            :exceptions: None.
        '''
        self.pause_flag = Event()
        self.stop_flag = Event()
        self.pacer = MissionPacer(
            pause_flag=self.pause_flag,
            stop_flag=self.stop_flag,
            clock=Clock(),
            tick_interval_sec=0.01,
        )

    def test_wait_paused_resume_and_abort(self) -> None:
        '''
            Verifies wait_paused unblocks on resume and returns False on stop.

            :exceptions: None.
        '''
        self.assertTrue(self.pacer.wait_paused())

        self.pause_flag.set()

        def resume_soon() -> None:
            sleep(0.015)
            self.pause_flag.clear()

        resumer = Thread(target=resume_soon)
        resumer.start()
        self.assertTrue(self.pacer.wait_paused())
        resumer.join()

        self.pause_flag.set()
        self.stop_flag.set()
        self.assertFalse(self.pacer.wait_paused())

    def test_sleep_step_complete_and_stopped(self) -> None:
        '''
            Verifies sleep_step completes duration or exits immediately on stop.

            :exceptions: None.
        '''
        self.assertTrue(self.pacer.sleep_step(0.015))
        self.stop_flag.set()
        self.assertFalse(self.pacer.sleep_step(0.5))


if __name__ == '__main__':
    main()
