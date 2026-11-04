# -*- coding: UTF-8 -*-

'''
Module
    opt_validator.py
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
    Validator for the botracked bundle options.
'''

from __future__ import annotations

from collections.abc import Mapping

from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_none

from botracked.setup.keys import BotrackedBundleKeys
from botracked.setup.options import BotrackedBundleOptions

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class BotrackedBundleOptionsValidator:
    '''
        Validator for the botracked bundle options.

        It defines:

            :methods:
                | validate - Validates the botracked bundle options.
                | is_valid - Checks if the botracked bundle options are valid.
    '''

    @classmethod
    def validate(cls, options: BotrackedBundleOptions) -> None:
        '''
            Validates the botracked bundle options.

            :param options: The bundle options to be validated.
            :exceptions:
                | ATSValueError: If bundle options are missing.
                | ATSTypeError: If bundle options have invalid types.
        '''
        ctx: str = 'botracked_bundle_options_validator::validate(...)'
        not_none(
            options, ctx, 'the botracked bundle options must be provided'
        )
        istype(
            options,
            Mapping,
            ctx,
            'the botracked bundle options must be a Mapping',
        )

        opt_types = BotrackedBundleKeys.get_option_to_type()
        for attr_name, expected_type in opt_types.items():
            if attr_name in options:
                label: str = attr_name.replace('_', ' ')
                attribute = options.get(attr_name)
                istype(
                    attribute,
                    expected_type,
                    ctx,
                    f'the {label} must be an instance of '
                    f'{expected_type.__name__}',
                )

    @classmethod
    def is_valid(cls, options: BotrackedBundleOptions) -> bool:
        '''
            Checks if the botracked bundle options are valid.

            :param options: The bundle options to check.
            :return: True if valid, False otherwise.
            :exceptions: None.
        '''
        try:
            cls.validate(options)
            return True
        except (ATSValueError, ATSTypeError):
            return False
