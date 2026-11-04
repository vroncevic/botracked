# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for CockpitDependencies.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.service.bundle.services import BotServicesBundle
from botracked.infrastructure.gui.console.observer.ilistener import ILogListener
from botracked.infrastructure.gui.console.observer.isink import IPacketStreamSink
from botracked.setup.gui.cockpit.dependencies import CockpitDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CockpitDependenciesTest(TestCase):
    '''
        Tests CockpitDependencies bundle fields.
    '''

    def test_fields(self) -> None:
        '''
            Verifies collaborator retention on CockpitDependencies.

            :exceptions: None.
        '''
        root = MagicMock(spec=Tk)
        deps = CockpitDependencies(
            root=root,
            parent=root,
            services=MagicMock(spec=BotServicesBundle),
            log_listener=MagicMock(spec=ILogListener),
            packet_sink=MagicMock(spec=IPacketStreamSink),
        )
        self.assertIs(deps.root, root)
        self.assertIs(deps.parent, root)


if __name__ == '__main__':
    main()
