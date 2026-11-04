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
    Unit tests for CLIBundleOptionsValidator.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.option.imanager import IOptionManager

from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.infrastructure.cli.setup.opt_validator import CLIBundleOptionsValidator
from botracked.infrastructure.cli.setup.options import CLIBundleOptions
from botracked.infrastructure.command.bundle import CommandBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class CLIBundleOptionsValidatorTest(TestCase):
    '''
        Tests CLIBundleOptionsValidator validation paths.
    '''

    def test_validate_options(self) -> None:
        '''
            Verifies acceptance of valid options and rejection of bad types.

            :exceptions: None.
        '''
        opts: CLIBundleOptions = {
            'service': MagicMock(spec=BotRuntimeBundle),
            'parser': MagicMock(spec=IOptionManager),
            'commands': (MagicMock(spec=CommandBundle),),
        }
        CLIBundleOptionsValidator.validate(opts)
        self.assertTrue(CLIBundleOptionsValidator.is_valid(opts))

        bad_input: object = 42
        with self.assertRaises(ATSTypeError):
            CLIBundleOptionsValidator.validate(bad_input)  # type: ignore[arg-type]
        self.assertFalse(
            CLIBundleOptionsValidator.is_valid(bad_input)  # type: ignore[arg-type]
        )

        incomplete: dict[str, object] = {'service': opts['service']}
        with self.assertRaises(ATSValueError):
            CLIBundleOptionsValidator.validate(incomplete)  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
