# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for CLIFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.option.imanager import IOptionManager

from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.infrastructure.cli.dependencies import CLIDependencies
from botracked.infrastructure.cli.factory import CLIFactory
from botracked.infrastructure.cli.icli import ICLI
from botracked.infrastructure.cli.setup.bundle import CLIBundle
from botracked.infrastructure.command.bundle import CommandBundle
from botracked.infrastructure.command.definition import StudioCommandDefinition
from botracked.infrastructure.command.iexecutor import ICommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class CLIFactoryTest(TestCase):
    '''
        Tests CLIFactory wiring and version reporting.
    '''

    def test_create_and_version(self) -> None:
        '''
            Verifies CLIFactory creates valid ICLI adapter.

            :exceptions: None.
        '''
        cmd = CommandBundle(
            definition=StudioCommandDefinition(),
            executor=MagicMock(spec=ICommandExecutor),
        )
        bundle = CLIBundle(
            service=MagicMock(spec=BotRuntimeBundle),
            parser=MagicMock(spec=IOptionManager),
            commands=(cmd,),
        )
        prov = CLIFactory.create(CLIDependencies(bundle=bundle))
        self.assertIsInstance(prov.cli, ICLI)
        self.assertEqual(CLIFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
