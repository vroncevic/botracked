# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
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
    Unit tests for CLI engine.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.option.imanager import IOptionManager

from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.infrastructure.cli.engine import CLI
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

class CLITest(TestCase):
    '''
        Tests CLI subcommand registration, parsing, and execution dispatch.
    '''

    def test_cli_run_known_and_unknown_commands(self) -> None:
        '''
            Verifies execution of registered studio command and unknown fallback.

            :exceptions: None.
        '''
        parser = MagicMock(spec=IOptionManager)
        exe = MagicMock(spec=ICommandExecutor)
        exe.execute.return_value = {'returncode': 0, 'stdout': 'done', 'stderr': ''}
        cmd = CommandBundle(definition=StudioCommandDefinition(), executor=exe)
        bundle = CLIBundle(
            service=MagicMock(spec=BotRuntimeBundle),
            parser=parser,
            commands=(cmd,),
        )
        cli = CLI(bundle)
        self.assertTrue(cli.is_initialized())
        self.assertTrue(str(cli))

        parser.parse_command.return_value = ('studio', {'port': '/dev/ttyACM0'})
        res = cli.run()
        self.assertEqual(res['returncode'], 0)
        exe.execute.assert_called_once()

        parser.parse_command.return_value = ('', {})
        default_res = cli.run()
        self.assertEqual(default_res['returncode'], 0)

        parser.parse_command.return_value = ('missing', {})
        bad_res = cli.run()
        self.assertEqual(bad_res['returncode'], 1)

        parser.parse_command.side_effect = RuntimeError('parse failure')
        err_res = cli.run()
        self.assertEqual(err_res['returncode'], 1)


if __name__ == '__main__':
    main()
