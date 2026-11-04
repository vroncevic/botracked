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
    Unit tests for BotrackedBundleDependenciesValidator.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.exceptions import ATSTypeError

from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.infrastructure.cli.icli import ICLI
from botracked.infrastructure.gui.igui import IGUI
from botracked.setup.dep_validator import BotrackedBundleDependenciesValidator
from botracked.setup.dependencies import BotrackedBundleDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class BotrackedBundleDependenciesValidatorTest(TestCase):
    '''
        Tests BotrackedBundleDependenciesValidator validation checks.
    '''

    def test_validate_dependencies(self) -> None:
        '''
            Verifies valid dependencies pass and invalid types fail.

            :exceptions: None.
        '''
        deps: BotrackedBundleDependencies = {
            'base': MagicMock(spec=BaseBundle),
            'service': MagicMock(spec=BotRuntimeBundle),
            'gui': MagicMock(spec=IGUI),
            'cli': MagicMock(spec=ICLI),
        }
        BotrackedBundleDependenciesValidator.validate(deps)
        self.assertTrue(BotrackedBundleDependenciesValidator.is_valid(deps))

        bad_val: object = 99
        with self.assertRaises(ATSTypeError):
            BotrackedBundleDependenciesValidator.validate(bad_val)  # type: ignore[arg-type]
        self.assertFalse(
            BotrackedBundleDependenciesValidator.is_valid(bad_val)  # type: ignore[arg-type]
        )


if __name__ == '__main__':
    main()
