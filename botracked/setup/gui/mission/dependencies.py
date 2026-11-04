# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Defines MissionDependencies bundle for MissionFactory.
'''

from __future__ import annotations

from dataclasses import dataclass
from tkinter import Tk
from tkinter.ttk import Frame

from botracked.core.service.dsl.iservice import ITbotDslService
from botracked.core.service.dsl.preset.irepository import IMissionPresetRepository
from botracked.core.service.motion.runner.irunner import IMissionRunner
from botracked.infrastructure.gui.console.observer.ilistener import ILogListener

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class MissionDependencies:
    '''
        Immutable collaborator bundle injected into MissionFactory.

        It defines:

            :attributes:
                | parent - Native parent container Frame or Tk window instance.
                | dsl_service - Mission DSL lexing, parsing, compilation service.
                | mission_runner - Asynchronous mission execution runner port.
                | preset_repository - Mission preset repository port.
                | log_listener - Diagnostic console log listener port.
    '''

    parent: Frame | Tk
    dsl_service: ITbotDslService
    mission_runner: IMissionRunner
    preset_repository: IMissionPresetRepository
    log_listener: ILogListener
