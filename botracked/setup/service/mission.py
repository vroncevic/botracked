# -*- coding: UTF-8 -*-

'''
Module
    mission.py
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
    Defines MissionAssembler wiring mission execution runner and pacer.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.service.concurrency.iclock import IClock
from botracked.core.service.motion.protocol.iactuator import IMissionActuator
from botracked.core.service.motion.runner.dependencies import MissionRunnerDependencies
from botracked.core.service.motion.runner.factory import MissionRunnerFactory
from botracked.core.service.motion.runner.irunner import IMissionRunner
from botracked.core.service.motion.runner.pacer.dependencies import MissionPacerDependencies
from botracked.core.service.motion.runner.pacer.factory import MissionPacerFactory
from botracked.core.service.motion.runner.worker.dependencies import MissionWorkerDependencies
from botracked.core.service.motion.runner.worker.factory import MissionWorkerFactory
from botracked.infrastructure.concurrency.controller.dependencies import LoopControllerDependencies
from botracked.infrastructure.concurrency.controller.factory import LoopControllerFactory
from botracked.infrastructure.concurrency.flag.factory import SignalFlagFactory
from botracked.infrastructure.concurrency.runner.dependencies import ThreadRunnerDependencies
from botracked.infrastructure.concurrency.runner.factory import ThreadRunnerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionAssembler:
    '''
        Defines class MissionAssembler wiring mission execution runner.

        It defines:

            :attributes:
                | MISSION_TICK_SEC - Mission pacer slice interval in seconds.
                | MISSION_THREAD_NAME - Thread prefix for mission runner.
                | WORKER_JOIN_TIMEOUT - Thread runner shutdown timeout in seconds.
            :methods:
                | assemble - Wires pacer, worker, controller, returns runner.
                | get_version - Returns assembler version string.
    '''

    MISSION_TICK_SEC: ClassVar[float] = 0.05
    MISSION_THREAD_NAME: ClassVar[str] = 'MissionRunner'
    WORKER_JOIN_TIMEOUT: ClassVar[float] = 0.5

    @classmethod
    def assemble(
        cls, *, clock: IClock, actuator: IMissionActuator
    ) -> IMissionRunner:
        '''
            Wires mission execution pacer, worker, and thread runner.

            :param clock: Monotonic clock port.
            :param actuator: Locomotion actuator port.
            :return: Fully configured IMissionRunner instance.
            :exceptions: None.
        '''
        pause_flag = SignalFlagFactory.create().flag
        stop_flag = SignalFlagFactory.create().flag
        pacer = MissionPacerFactory.create(
            MissionPacerDependencies(
                clock=clock,
                pause_flag=pause_flag,
                stop_flag=stop_flag,
                tick_interval_sec=cls.MISSION_TICK_SEC,
            )
        ).pacer
        worker = MissionWorkerFactory.create(
            MissionWorkerDependencies(
                pacer=pacer,
                actuator=actuator,
                stop_flag=stop_flag,
            )
        ).worker
        controller = LoopControllerFactory.create(
            LoopControllerDependencies(
                runner=ThreadRunnerFactory.create(
                    ThreadRunnerDependencies(
                        thread_name=cls.MISSION_THREAD_NAME,
                        join_timeout=cls.WORKER_JOIN_TIMEOUT,
                    )
                ).runner,
                stop_flag=stop_flag,
            )
        ).controller
        return MissionRunnerFactory.create(
            MissionRunnerDependencies(
                worker=worker,
                controller=controller,
                pause_flag=pause_flag,
            )
        ).runner

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns assembler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
