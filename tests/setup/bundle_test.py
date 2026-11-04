# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit tests for BotrackedBundle.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.base.setup.bundle import BaseBundle

from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.infrastructure.cli.icli import ICLI
from botracked.infrastructure.gui.igui import IGUI
from botracked.setup.bundle import BotrackedBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class BotrackedBundleTest(TestCase):
    '''
        Tests BotrackedBundle attribute retention and serialization.
    '''

    def test_bundle_to_dict(self) -> None:
        '''
            Verifies BotrackedBundle fields and to_dict output.

            :exceptions: None.
        '''
        bnd = BotrackedBundle(
            base=MagicMock(spec=BaseBundle),
            service=MagicMock(spec=BotRuntimeBundle),
            gui=MagicMock(spec=IGUI),
            cli=MagicMock(spec=ICLI),
        )
        dct = bnd.to_dict()
        self.assertIn('gui', dct)
        self.assertIn('cli', dct)


if __name__ == '__main__':
    main()
