# -*- coding: UTF-8 -*-

'''
Module
    dep_validator_test.py
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
    Unit tests for CLIBundleDependenciesValidator.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.option.imanager import IOptionManager

from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.infrastructure.cli.setup.dep_validator import CLIBundleDependenciesValidator
from botracked.infrastructure.cli.setup.dependencies import CLIBundleDependencies
from botracked.infrastructure.command.bundle import CommandBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class CLIBundleDependenciesValidatorTest(TestCase):
    '''
        Tests CLIBundleDependenciesValidator validation rules.
    '''

    def test_validate_valid_and_invalid_dependencies(self) -> None:
        '''
            Verifies valid mapping and rejection of malformed inputs.

            :exceptions: None.
        '''
        deps: CLIBundleDependencies = {
            'service': MagicMock(spec=BotRuntimeBundle),
            'parser': MagicMock(spec=IOptionManager),
            'commands': (MagicMock(spec=CommandBundle),),
        }
        CLIBundleDependenciesValidator.validate(deps)
        self.assertTrue(CLIBundleDependenciesValidator.is_valid(deps))

        bad_val: object = 'invalid'
        with self.assertRaises(ATSTypeError):
            CLIBundleDependenciesValidator.validate(bad_val)  # type: ignore[arg-type]
        self.assertFalse(
            CLIBundleDependenciesValidator.is_valid(bad_val)  # type: ignore[arg-type]
        )

        missing_deps: dict[str, object] = {'service': deps['service']}
        with self.assertRaises(ATSValueError):
            CLIBundleDependenciesValidator.validate(missing_deps)  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
