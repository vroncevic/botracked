# -*- coding: UTF-8 -*-

'''
Module
    pacer.py
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
    Defines MissionPacer managing step timing, pauses, and interruptions.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.service.concurrency.iclock import IClock
from botracked.core.service.concurrency.iflag import ISignalFlag

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionPacer:
    '''
        Defines class MissionPacer implementing IMissionPacer structurally.
        Encapsulates step duration delays and responsive pause flag handling.

        It defines:

            :attributes:
                | ZERO_DURATION - Lower clamp bound for non-negative durations.
                | _clock - Monotonic clock port tracking step deadlines.
                | _pause_flag - Signal flag indicating paused progression.
                | _stop_flag - Signal flag indicating mission abort.
                | _tick_interval_sec - Wait slice interval in seconds.
            :methods:
                | __init__ - Initializes mission pacer with clock, flags, and tick.
                | wait_paused - Waits while pause flag is active unless aborted.
                | sleep_step - Waits for step duration while observing stop flag.
    '''

    ZERO_DURATION: ClassVar[float] = 0.0

    _clock: IClock
    _pause_flag: ISignalFlag
    _stop_flag: ISignalFlag
    _tick_interval_sec: float

    def __init__(
        self,
        *,
        clock: IClock,
        pause_flag: ISignalFlag,
        stop_flag: ISignalFlag,
        tick_interval_sec: float,
    ) -> None:
        '''
            Initializes mission pacer with clock, synchronization flags, and tick.

            :param clock: Monotonic clock port tracking step deadlines.
            :param pause_flag: Signal flag indicating paused progression.
            :param stop_flag: Signal flag indicating mission cancellation.
            :param tick_interval_sec: Wait slice interval in seconds.
            :exceptions: None.
        '''
        self._clock = clock
        self._pause_flag = pause_flag
        self._stop_flag = stop_flag
        self._tick_interval_sec = tick_interval_sec

    def wait_paused(self) -> bool:
        '''
            Waits while pause flag is active unless cancellation occurs.

            :return: True if resumed normally, False if stopped.
            :exceptions: None.
        '''
        while self._pause_flag.is_set() and not self._stop_flag.is_set():
            self._stop_flag.wait(self._tick_interval_sec)

        return not self._stop_flag.is_set()

    def sleep_step(self, duration_s: float) -> bool:
        '''
            Waits for step duration while observing cancellation signal.

            :param duration_s: Step duration to wait in seconds.
            :return: True if full duration elapsed, False if stopped.
            :exceptions: None.
        '''
        end_time: float = self._clock.monotonic() + max(
            self.ZERO_DURATION, duration_s
        )

        while not self._stop_flag.is_set():
            remaining: float = end_time - self._clock.monotonic()

            if remaining <= self.ZERO_DURATION:
                break

            self._stop_flag.wait(min(self._tick_interval_sec, remaining))

        return not self._stop_flag.is_set()
