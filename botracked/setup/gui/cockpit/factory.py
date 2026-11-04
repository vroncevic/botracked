# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Defines CockpitFactory assembling motion and telemetry cockpit panels.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from typing import ClassVar

from botracked.infrastructure.gui.motion.adapter.dependencies import MotionAdapterDependencies
from botracked.infrastructure.gui.motion.adapter.factory import MotionAdapterFactory
from botracked.infrastructure.gui.motion.dependencies import MotionPanelDependencies
from botracked.infrastructure.gui.motion.dpad.dependencies import MotionDpadDependencies
from botracked.infrastructure.gui.motion.dpad.factory import MotionDpadFactory
from botracked.infrastructure.gui.motion.factory import MotionPanelFactory
from botracked.infrastructure.gui.motion.keyboard.dependencies import MotionKeyboardDependencies
from botracked.infrastructure.gui.motion.keyboard.factory import MotionKeyboardFactory
from botracked.infrastructure.gui.motion.speed.dependencies import MotionSpeedDependencies
from botracked.infrastructure.gui.motion.speed.factory import MotionSpeedFactory
from botracked.infrastructure.gui.telemetry.card.dependencies import TelemetryCardDependencies
from botracked.infrastructure.gui.telemetry.card.factory import TelemetryCardFactory
from botracked.infrastructure.gui.telemetry.config import TelemetryPanelConfig
from botracked.infrastructure.gui.telemetry.dependencies import TelemetryPanelDependencies
from botracked.infrastructure.gui.telemetry.factory import TelemetryPanelFactory
from botracked.infrastructure.gui.telemetry.observer.dependencies import TelemetryObserverDependencies
from botracked.infrastructure.gui.telemetry.observer.factory import TelemetryObserverFactory
from botracked.setup.gui.cockpit.dependencies import CockpitDependencies
from botracked.setup.gui.cockpit.provides import CockpitProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CockpitFactory:
    '''
        Defines class CockpitFactory assembling motion and telemetry UI.

        It defines:

            :attributes:
                | DEFAULT_SPEED - Initial manual PWM locomotion speed byte.
                | PANEL_STYLE - Panel ttk Frame style identifier.
                | PANEL_PADDING - Horizontal and vertical panel padding.
            :methods:
                | create - Wires motion and telemetry panels and observer link.
                | get_version - Returns factory version string.
    '''

    DEFAULT_SPEED: ClassVar[int] = 180
    PANEL_STYLE: ClassVar[str] = 'Panel.TFrame'
    PANEL_PADDING: ClassVar[tuple[int, int]] = (8, 8)

    @classmethod
    def create(
        cls, dependencies: CockpitDependencies
    ) -> CockpitProvides:
        '''
            Wires motion panel, keyboard hotkeys, telemetry panel, and observer.

            :param dependencies: Cockpit GUI composition collaborators.
            :return: Assembled CockpitProvides bundle.
            :exceptions: None.
        '''
        motion_delegate = MotionAdapterFactory.create(
            MotionAdapterDependencies(
                motion_service=dependencies.services.motion,
                log_listener=dependencies.log_listener,
            )
        ).delegate
        motion_frame = Frame(
            dependencies.parent,
            style=cls.PANEL_STYLE,
            padding=cls.PANEL_PADDING,
        )
        motion_panel = MotionPanelFactory.create(
            MotionPanelDependencies(
                frame=motion_frame,
                dpad_section=MotionDpadFactory.create(
                    MotionDpadDependencies(
                        parent=motion_frame,
                        delegate=motion_delegate,
                    )
                ).section,
                speed_section=MotionSpeedFactory.create(
                    MotionSpeedDependencies(
                        parent=motion_frame,
                        delegate=motion_delegate,
                        default_speed=cls.DEFAULT_SPEED,
                    )
                ).section,
                keyboard_controller=MotionKeyboardFactory.create(
                    MotionKeyboardDependencies(delegate=motion_delegate)
                ).controller,
            )
        ).panel
        motion_panel.bind_keyboard(dependencies.root)

        telem_cfg = TelemetryPanelConfig()
        telem_frame = Frame(
            dependencies.parent,
            style=cls.PANEL_STYLE,
            padding=cls.PANEL_PADDING,
        )
        telem_prov = TelemetryPanelFactory.create(
            TelemetryPanelDependencies(
                frame=telem_frame,
                card_section=TelemetryCardFactory.create(
                    TelemetryCardDependencies(
                        parent=telem_frame,
                        config=telem_cfg,
                    )
                ).section,
                config=telem_cfg,
            )
        )
        telem_observer = TelemetryObserverFactory.create(
            TelemetryObserverDependencies(
                scheduler=dependencies.root,
                view=telem_prov.view,
                packet_sink=dependencies.packet_sink,
            )
        )
        dependencies.services.telemetry.add_observer(telem_observer.observer)

        return CockpitProvides(
            motion_panel=motion_panel,
            telemetry_panel=telem_prov.panel,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
