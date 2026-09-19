# -*- coding: UTF-8 -*-

'''
Module
    compiled_step.py
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
    Defines CompiledStep representing a single executable mission plan step.
'''

from __future__ import annotations

from dataclasses import dataclass, field

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class CompiledStep:
    '''
        Defines executable step produced by the mission script compiler.
        Encapsulates payload frames, timing delay, and execution flags.

        It defines:

            :attributes:
                | frames - Tuple of raw encoded command frame byte sequences.
                | duration_sec - Delay duration in seconds to wait after sending.
                | auto_stop_after - Indicates if a STOP frame should follow.
                | description - Human-readable description of this step.
                | line_number - Source line number that generated this step.
            :methods:
                | frame_count - Returns the number of frames in this step.
                | has_delay - Checks whether this step requires a timing delay.
    '''

    frames: tuple[bytes, ...] = field(default_factory=tuple)
    duration_sec: float = 0.0
    auto_stop_after: bool = False
    description: str = ''
    line_number: int = 1

    @property
    def frame_count(self) -> int:
        '''
            Returns the number of frames contained in this compiled step.

            :return: Total number of binary command frames.
            :exceptions: None.
        '''
        return len(self.frames)

    @property
    def has_delay(self) -> bool:
        '''
            Checks whether this compiled step requires a pause or execution delay.

            :return: True if step duration is greater than zero, False otherwise.
            :exceptions: None.
        '''
        return self.duration_sec > 0.0
