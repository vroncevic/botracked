# -*- coding: UTF-8 -*-

'''
Module
    dep_validator.py
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
    Validator for the botracked bundle dependencies.
'''

from __future__ import annotations

from collections.abc import Mapping

from ats_utilities.exceptions import ATSTypeError, ATSValueError
from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_none

from botracked.setup.dependencies import BotrackedBundleDependencies
from botracked.setup.keys import BotrackedBundleKeys

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotrackedBundleDependenciesValidator:
    '''
        Validator for the botracked bundle dependencies.

        It defines:

            :methods:
                | validate - Validates the botracked bundle dependencies.
                | is_valid - Checks if the botracked bundle dependencies are valid.
    '''

    @classmethod
    def validate(cls, dependencies: BotrackedBundleDependencies) -> None:
        '''
            Validates the botracked bundle dependencies.

            :param dependencies: The bundle dependencies to be validated.
            :exceptions:
                | ATSValueError: The botracked bundle dependencies must be provided and have proper values.
                | ATSTypeError:  The botracked bundle dependencies must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
        '''
        ctx: str = 'botracked_bundle_dependencies_validator::validate(...)'
        msg_dependencies_none: str = 'the botracked bundle dependencies must be provided'
        msg_dependencies_istype: str = 'the botracked bundle dependencies must be a Mapping'

        not_none(dependencies, ctx, msg_dependencies_none)
        istype(dependencies, Mapping, ctx, msg_dependencies_istype)

        for attr_name, expected_type in BotrackedBundleKeys.get_dependency_to_type().items():
            msg_attr_name_none: str = f'the {attr_name.replace("_", " ")} must be provided'
            msg_attr_name_istype: str = f'the {attr_name.replace("_", " ")} must be an instance of {expected_type.__name__}'

            attr_val = dependencies.get(attr_name)

            not_none(attr_val, ctx, msg_attr_name_none)
            istype(attr_val, expected_type, ctx, msg_attr_name_istype)

    @classmethod
    def is_valid(cls, dependencies: BotrackedBundleDependencies) -> bool:
        '''
            Checks if the botracked bundle dependencies are valid.

            :param dependencies: The bundle dependencies to check.
            :return: True if valid, False otherwise.
            :exceptions: None.
        '''
        try:
            cls.validate(dependencies)
            return True

        except (ATSValueError, ATSTypeError):
            return False
