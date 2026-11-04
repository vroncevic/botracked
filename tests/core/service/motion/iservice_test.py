# -*- coding: UTF-8 -*-

'''
Module
    iservice_test.py
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
    Unit tests for IBotMotionService structural protocol contract.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.connection.dispatcher.idispatcher import IFrameDispatcher
from botracked.core.service.motion.iservice import IBotMotionService
from botracked.core.service.motion.service import BotMotionService

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotMotionServiceProtocolTest(TestCase):
    '''
        Verifies runtime structural subtyping of IBotMotionService.
    '''

    def test_conformance(self) -> None:
        '''
            Verifies BotMotionService satisfies IBotMotionService structurally.

            :exceptions: None.
        '''
        svc = BotMotionService(dispatcher=Mock(spec=IFrameDispatcher))
        self.assertIsInstance(svc, IBotMotionService)
        self.assertNotIsInstance(object(), IBotMotionService)


if __name__ == '__main__':
    main()
