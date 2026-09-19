# -*- coding: UTF-8 -*-

'''
Module
    setup_and_preferences_test.py
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
    Unit tests for setup container, preferences repository, and domain extensions.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from tempfile import TemporaryDirectory
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from botracked.core.service.dsl.tbot_compiler import TbotCompiler
from botracked.core.service.dsl.tbot_lexer import TbotLexer
from botracked.core.service.dsl.tbot_parser import TbotParser
from botracked.infrastructure.communication.crc8_calculator import (
    Crc8Calculator,
)
from botracked.infrastructure.communication.preferences.connection_preferences_repository import (
    ConnectionPreferencesRepository,
)
from botracked.infrastructure.gui.editor.dsl_preset_loader import (
    DslPresetLoader,
)
from botracked.setup.bundle import BotrackedBundle
from botracked.setup.dep_validator import (
    BotrackedBundleDependenciesValidator,
)
from botracked.setup.factory import BotrackedBundleFactory
from botracked.setup.keys import BotrackedBundleKeys
from botracked.setup.opt_validator import BotrackedBundleOptionsValidator
from botracked.setup.options import BotrackedBundleOptions
from botracked.setup.registry import BotrackedBundleRegistry

from botracked.infrastructure.gui.connection.connection_panel_config import (
    ConnectionPanelConfig,
)
from botracked.infrastructure.gui.controls.jog_panel_config import (
    JogPanelConfig,
)
from botracked.infrastructure.gui.editor.dsl_editor_panel_config import (
    DslEditorPanelConfig,
)
from botracked.infrastructure.gui.gui_config import GuiConfig
from botracked.infrastructure.gui.stream.log_panel_config import LogPanelConfig
from botracked.infrastructure.gui.telemetry.telemetry_panel_config import (
    TelemetryPanelConfig,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSetupAndPreferences(TestCase):
    '''
    Tests setup validators, bundle registry, preferences persistence, and domain methods.
    '''

    def test_crc8_update_matches_calculate(self) -> None:
        calc = Crc8Calculator()
        data = b'TEST_PAYLOAD_123'
        full_crc = calc.calculate(data)

        running_crc = 0x00
        for byte in data:
            running_crc = calc.update(running_crc, byte)

        self.assertEqual(full_crc, running_crc)

    def test_dsl_domain_methods(self) -> None:
        source = 'SPEED 150\nFORWARD 1.5\nSTOP\n'
        lexer = TbotLexer()
        token_count = lexer.count_tokens(source)
        self.assertGreater(token_count, 0)

        tokens = lexer.tokenize(source)
        parser = TbotParser()
        is_valid, msg = parser.validate_syntax(tokens)
        self.assertTrue(is_valid)

        ast = parser.parse(tokens)
        compiler = TbotCompiler()
        est_time = compiler.estimate_duration(ast)
        self.assertAlmostEqual(est_time, 1.5)

    def test_dsl_preset_loader(self) -> None:
        presets = DslPresetLoader.load_presets()
        self.assertIsInstance(presets, dict)
        self.assertGreater(len(presets), 0)

    def test_preferences_save_and_load(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            pref_file = f'{tmp_dir}/test_conn.json'
            repo = ConnectionPreferencesRepository(config_file=pref_file)

            port, baud = repo.load_preference()
            self.assertIsNone(port)
            self.assertIsNone(baud)

            saved = repo.save_preference(port='/dev/ttyUSB1', baud=115200)
            self.assertTrue(saved)

            loaded_port, loaded_baud = repo.load_preference()
            self.assertEqual(loaded_port, '/dev/ttyUSB1')
            self.assertEqual(loaded_baud, 115200)

    def test_bundle_options_validation(self) -> None:
        valid_opts: BotrackedBundleOptions = {
            'port': '/dev/ttyUSB0',
            'baud': 9600,
            'verbose': True,
        }
        self.assertTrue(BotrackedBundleOptionsValidator.is_valid(valid_opts))

    def test_bundle_factory_creation(self) -> None:
        bundle = BotrackedBundleFactory.create_bundle()
        self.assertIsInstance(bundle, BotrackedBundle)
        self.assertIsNotNone(bundle.base)
        self.assertIsNotNone(bundle.service)
        self.assertIsNotNone(bundle.gui)
        self.assertIsNotNone(bundle.cli)
        self.assertEqual(BotrackedBundleRegistry.get_version(), '1.0.0')

    def test_gui_configs(self) -> None:
        gui_cfg = GuiConfig()
        self.assertEqual(gui_cfg.min_width, 1200)
        self.assertEqual(gui_cfg.min_height, 800)

        jog_cfg = JogPanelConfig()
        self.assertEqual(jog_cfg.max_speed, 255)
        self.assertAlmostEqual(jog_cfg.default_speed, 180.0)

        conn_cfg = ConnectionPanelConfig()
        self.assertEqual(conn_cfg.default_baud, '9600')
        self.assertIn('115200', conn_cfg.baud_rates)

        telem_cfg = TelemetryPanelConfig()
        self.assertEqual(telem_cfg.default_mode, 'OFFLINE')
        self.assertEqual(telem_cfg.card_mode, 'SYSTEM MODE')

        dsl_cfg = DslEditorPanelConfig()
        self.assertEqual(dsl_cfg.font_family, 'Courier')
        self.assertEqual(dsl_cfg.editor_height, 6)

        log_cfg = LogPanelConfig()
        self.assertEqual(log_cfg.log_height, 8)
        self.assertEqual(log_cfg.time_format, '%H:%M:%S.%f')


if __name__ == '__main__':
    main()
