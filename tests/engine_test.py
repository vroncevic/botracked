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
    Unit tests for Botracked tool engine.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.exceptions import ATSValueError
from ats_utilities.logger.ilogger import ILogger
from ats_utilities.option.imanager import IOptionManager

from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.engine import Botracked
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

class BotrackedTest(TestCase):
    '''
        Tests Botracked engine bootstrap, lifecycle, and process execution.
    '''

    _mock_base: MagicMock
    _mock_logger: MagicMock
    _mock_service: MagicMock
    _mock_gui: MagicMock
    _mock_cli: MagicMock
    _bundle: BotrackedBundle

    def setUp(self) -> None:
        '''
            Sets up test fixture before each test execution.

            :exceptions: None.
        '''
        self._mock_base = MagicMock(spec=BaseBundle)
        self._mock_logger = MagicMock(spec=ILogger)
        opt_mgr = MagicMock(spec=IOptionManager)
        opt_mgr.is_initialized.return_value = True
        self._mock_base.option_manager = opt_mgr
        self._mock_base.context_bundle.logger = self._mock_logger

        self._mock_service = MagicMock(spec=BotRuntimeBundle)
        self._mock_service.is_initialized.return_value = True
        self._mock_gui = MagicMock(spec=IGUI)
        self._mock_gui.is_initialized.return_value = True
        self._mock_cli = MagicMock(spec=ICLI)
        self._mock_cli.is_initialized.return_value = True

        self._bundle = BotrackedBundle(
            base=self._mock_base,
            service=self._mock_service,
            gui=self._mock_gui,
            cli=self._mock_cli,
        )

    @patch('ats_utilities.base.engine.Base.__init__', return_value=None)
    @patch('ats_utilities.base.engine.Base.get_context')
    def test_engine_process_success_and_failure(
        self, mock_get_context: MagicMock, mock_base_init: MagicMock
    ) -> None:
        '''
            Verifies successful and failing CLI returncode paths.

            :param mock_get_context: Mocked context provider.
            :param mock_base_init: Mocked base class constructor.
            :exceptions: None.
        '''
        mock_ctx = MagicMock()
        mock_ctx.logger = self._mock_logger
        mock_get_context.return_value = mock_ctx

        self._mock_cli.run.return_value = {
            'returncode': 0,
            'stdout': 'ok',
            'stderr': '',
        }
        engine = Botracked(self._bundle)
        self.assertTrue(engine.is_initialized())
        self.assertTrue(engine.process(verbose=True))
        mock_base_init.assert_called_once()

        self._mock_cli.run.return_value = {
            'returncode': 1,
            'stdout': '',
            'stderr': 'err',
        }
        self.assertFalse(engine.process(verbose=False))

    def test_engine_invalid_bundle_and_uninitialized_process(self) -> None:
        '''
            Verifies safe error handling when bundle validation fails.

            :exceptions: None.
        '''
        with patch('botracked.engine.stdout.write') as mock_out:
            bad_obj: object = 'invalid_bundle'
            engine = Botracked(bad_obj)  # type: ignore[arg-type]
            self.assertFalse(engine.is_initialized())
            self.assertFalse(engine.process())
            mock_out.assert_called()

    @patch('ats_utilities.base.engine.Base.__init__', return_value=None)
    @patch('ats_utilities.base.engine.Base.get_context')
    def test_engine_unexpected_init_exception(
        self, mock_get_context: MagicMock, _mock_base_init: MagicMock
    ) -> None:
        '''
            Verifies handling of unexpected initialization exception.

            :param mock_get_context: Mocked context provider.
            :param _mock_base_init: Mocked base constructor.
            :exceptions: None.
        '''
        mock_ctx = MagicMock()
        mock_ctx.logger = self._mock_logger
        mock_get_context.return_value = mock_ctx

        with patch(
            'botracked.setup.validator.BotrackedBundleValidator.validate',
            side_effect=RuntimeError('catastrophic'),
        ), patch('botracked.engine.stdout.write') as mock_out:
            engine = Botracked(self._bundle)
            self.assertFalse(engine.is_initialized())
            mock_out.assert_called()

    @patch('ats_utilities.base.engine.Base.__init__', return_value=None)
    @patch('ats_utilities.base.engine.Base.get_context')
    def test_engine_cli_exceptions(
        self, mock_get_context: MagicMock, _mock_base_init: MagicMock
    ) -> None:
        '''
            Verifies ATS and generic exception handling during process.

            :param mock_get_context: Mocked context provider.
            :param _mock_base_init: Mocked base constructor.
            :exceptions: None.
        '''
        mock_ctx = MagicMock()
        mock_ctx.logger = self._mock_logger
        mock_get_context.return_value = mock_ctx

        engine = Botracked(self._bundle)
        self._mock_cli.run.side_effect = ATSValueError('bad opt')
        self.assertFalse(engine.process())

        self._mock_cli.run.side_effect = RuntimeError('boom')
        self.assertFalse(engine.process())
        self._mock_logger.write_log.assert_called()


if __name__ == '__main__':
    main()
