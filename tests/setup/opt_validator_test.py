# -*- coding: UTF-8 -*-

'''
Module
    opt_validator_test.py
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
    Unit tests for BotrackedBundleOptionsValidator.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.exceptions import ATSTypeError

from botracked.setup.opt_validator import BotrackedBundleOptionsValidator
from botracked.setup.options import BotrackedBundleOptions

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class BotrackedBundleOptionsValidatorTest(TestCase):
    '''
        Tests BotrackedBundleOptionsValidator validation checks.
    '''

    def test_validate_options(self) -> None:
        '''
            Verifies valid options pass and malformed option types fail.

            :exceptions: None.
        '''
        opts: BotrackedBundleOptions = {'baud': 115200, 'verbose': False}
        BotrackedBundleOptionsValidator.validate(opts)
        self.assertTrue(BotrackedBundleOptionsValidator.is_valid(opts))

        bad_opts: object = {'baud': 'not_int'}
        with self.assertRaises(ATSTypeError):
            BotrackedBundleOptionsValidator.validate(bad_opts)  # type: ignore[arg-type]
        self.assertFalse(
            BotrackedBundleOptionsValidator.is_valid(bad_opts)  # type: ignore[arg-type]
        )


if __name__ == '__main__':
    main()
