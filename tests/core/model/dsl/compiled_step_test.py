# -*- coding: UTF-8 -*-

'''
Module
    compiled_step_test.py
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
    Unit tests for CompiledStep value object.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from botracked.core.model.dsl.compiled_step import CompiledStep

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CompiledStepTest(TestCase):
    '''
        Tests CompiledStep initialization, attributes, immutability, and equality.
    '''

    def test_instantiation_and_fields(self) -> None:
        '''
            Verifies field values upon standard instantiation.

            :exceptions: None.
        '''
        step = CompiledStep(
            frames=(b'\x02\x01\x96', b'\x01\x01\x01'),
            duration_sec=1.5,
            auto_stop_after=True,
            description='Forward 1.5s',
            line_number=3
        )
        self.assertEqual(step.frames, (b'\x02\x01\x96', b'\x01\x01\x01'))
        self.assertEqual(step.duration_sec, 1.5)
        self.assertTrue(step.auto_stop_after)
        self.assertEqual(step.description, 'Forward 1.5s')
        self.assertEqual(step.line_number, 3)

    def test_immutability(self) -> None:
        '''
            Verifies that modifying frozen dataclass attributes raises FrozenInstanceError.

            :exceptions: None.
        '''
        step = CompiledStep(
            frames=(),
            duration_sec=0.0,
            auto_stop_after=False,
            description='Stop',
            line_number=1
        )
        with self.assertRaises(FrozenInstanceError):
            step.duration_sec = 2.0  # type: ignore[misc]

    def test_equality(self) -> None:
        '''
            Verifies equality comparison between CompiledStep instances.

            :exceptions: None.
        '''
        step1 = CompiledStep((b'\x01',), 1.0, True, 'Step 1', 1)
        step2 = CompiledStep((b'\x01',), 1.0, True, 'Step 1', 1)
        step3 = CompiledStep((b'\x01',), 2.0, False, 'Step 2', 2)
        self.assertEqual(step1, step2)
        self.assertNotEqual(step1, step3)


if __name__ == '__main__':
    main()
