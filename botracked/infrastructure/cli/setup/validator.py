# -*- coding: UTF-8 -*-

'''
Module
    validator.py
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
    Validator for the CLIBundle dependencies.
'''

from __future__ import annotations

from collections.abc import Sequence

from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.option.imanager import IOptionManager
from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_none

from botracked.core.service.bot_service import BotService
from botracked.infrastructure.cli.setup.bundle import CLIBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLIBundleValidator:
    '''
        Validator ensuring CLIBundle structure integrity.

        It defines:

            :methods:
                | validate - Validates the CLI bundle.
                | is_valid - Checks if the CLI bundle is valid.
    '''

    @classmethod
    def validate(cls, bundle: CLIBundle) -> None:
        '''
            Validates the CLI bundle.

            :param bundle: The CLI bundle to validate.
            :type bundle: CLIBundle

            :return: None.
            :rtype: None

            :exceptions: ATSValueError, ATSTypeError.
        '''
        ctx: str = 'cli_bundle_validator::validate(...)'
        not_none(bundle, ctx, 'the cli bundle must be provided')
        istype(bundle, CLIBundle, ctx, 'the cli bundle must be an instance of CLIBundle')

        not_none(bundle.service, ctx, 'the service must be provided')
        not_none(bundle.parser, ctx, 'the parser must be provided')
        not_none(bundle.commands, ctx, 'the commands sequence must be provided')

        istype(bundle.service, BotService, ctx, 'the service must be an instance of BotService')
        istype(bundle.parser, IOptionManager, ctx, 'the parser must be an instance of IOptionManager')
        istype(bundle.commands, Sequence, ctx, 'the commands sequence must be an instance of Sequence')

    @classmethod
    def is_valid(cls, bundle: CLIBundle) -> bool:
        '''
            Checks if the CLI bundle is valid without raising exceptions.

            :param bundle: The CLI bundle to check.
            :type bundle: CLIBundle

            :return: True if valid, False otherwise.
            :rtype: bool

            :exceptions: None.
        '''
        try:
            cls.validate(bundle)
            return True
        except (ATSValueError, ATSTypeError):
            return False
