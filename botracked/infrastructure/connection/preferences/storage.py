# -*- coding: UTF-8 -*-

'''
Module
    storage.py
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
    Provides PreferencesStorage adapter implementing IPreferencesStorage over ATS config_io.
'''

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from ats_utilities.config_io.loader.engine import Loader
from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.config_io.storer.engine import Storer
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.utils.reflection import to_str

from botracked.core.model.exceptions.preferences_error import PreferencesError

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PreferencesStorage:
    '''
        Defines class PreferencesStorage implementing IPreferencesStorage structurally.
        Manages persistent configuration reading and writing via ats_utilities config_io.

        It defines:

            :attributes:
                | _config_file - Resolved filesystem path for preferences file.
                | _context - ATS context bundle instance for config operations.
            :methods:
                | __init__ - Initializes storage adapter with target file path and context.
                | exists - Checks if persistent storage file currently exists.
                | read_payload - Reads and parses dictionary payload from storage.
                | write_payload - Serializes and writes dictionary payload to storage.
                | __str__ - Returns string representation of storage adapter.
    '''

    _config_file: Path
    _context: ContextBundle

    def __init__(self, config_file: Path, context_bundle: ContextBundle) -> None:
        '''
            Initializes storage adapter with target file path and context.

            :param config_file: Target filesystem path for configuration JSON.
            :param context_bundle: ATS context bundle instance for file operations.
            :exceptions: None.
        '''
        self._config_file = config_file.resolve()
        self._context = context_bundle

    def exists(self) -> bool:
        '''
            Checks if persistent storage file currently exists.

            :return: True if storage file exists, False otherwise.
            :exceptions: None.
        '''
        return self._config_file.is_file()

    def read_payload(self) -> dict[str, object]:
        '''
            Reads and parses dictionary payload from storage using ATS Loader.

            :return: Parsed key-value dictionary payload.
            :exceptions:
                | PreferencesError: If file is missing, empty, or unreadable.
        '''
        if not self._config_file.is_file():
            raise PreferencesError(
                f'Preferences file does not exist: {self._config_file}'
            )
        try:
            bundle = ConfigIOBundleFactory.create_bundle(
                ConfigIOBundleOptions(
                    file_path=str(self._config_file),
                    context_bundle=self._context,
                )
            )
            loader = Loader(bundle)
            payload: dict[str, object] = loader.load_configuration()

        except (OSError, ATSValueError, ATSTypeError) as err:
            raise PreferencesError(
                f'Failed reading preferences JSON: {err}'
            ) from err

        if not isinstance(payload, dict) or not payload:
            raise PreferencesError(
                f'Preferences file is empty, malformed, or not an object: {self._config_file}'
            )

        return {str(key): value for key, value in payload.items()}

    def write_payload(self, payload: Mapping[str, object]) -> None:
        '''
            Serializes and writes dictionary payload to storage using ATS Storer.

            :param payload: Mapping of preference keys to primitive values.
            :exceptions:
                | PreferencesError: If writing fails or payload is invalid.
        '''
        try:
            self._config_file.parent.mkdir(parents=True, exist_ok=True)
            self._config_file.touch(exist_ok=True)
            bundle = ConfigIOBundleFactory.create_bundle(
                ConfigIOBundleOptions(
                    file_path=str(self._config_file),
                    context_bundle=self._context,
                )
            )
            storer = Storer(bundle)
            stored = storer.store_configuration(dict(payload))

            if not stored:
                raise PreferencesError(
                    f'Failed storing preferences to: {self._config_file}'
                )

        except (OSError, TypeError, ATSValueError, ATSTypeError) as err:
            raise PreferencesError(
                f'Failed writing preferences JSON: {err}'
            ) from err

    def __str__(self) -> str:
        '''
            Returns string representation of storage adapter.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
