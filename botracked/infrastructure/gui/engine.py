# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Main Tkinter graphical interface engine coordinating panels, tabs, and events.
'''

from __future__ import annotations

from tkinter import BOTH, BOTTOM, LEFT, RIGHT, TOP, X, Tk
from tkinter.ttk import Frame, Style

from botracked.core.service.bot_service import BotService
from botracked.core.service.dsl.tbot_dsl_service import TbotDslService
from botracked.infrastructure.gui.connection.connection_callbacks import (
    ConnectionCallbacks,
)
from botracked.infrastructure.gui.connection.connection_panel import (
    ConnectionPanel,
)
from botracked.infrastructure.gui.controls.jog_panel import JogPanel
from botracked.infrastructure.gui.controls.jog_panel_callbacks import (
    JogPanelCallbacks,
)
from botracked.infrastructure.gui.editor.dsl_editor_panel import DslEditorPanel
from botracked.infrastructure.gui.editor.mission_callbacks import (
    MissionCallbacks,
)
from botracked.infrastructure.gui.gui_config import GuiConfig
from botracked.infrastructure.gui.gui_event_mediator import GuiEventMediator
from botracked.infrastructure.gui.stream.log_panel import LogPanel
from botracked.infrastructure.gui.telemetry.telemetry_panel import (
    TelemetryPanel,
)
from botracked.infrastructure.gui.theme.style import StyleConfigurator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotrackedGUI:
    '''
        Primary GUI engine hosting cockpit, telemetry cards, mission editor,
        and logs.

        It defines:

            :attributes:
                | _root - Root Tk window instance.
                | _bot_service - Core robot interactor service.
                | _dsl_service - Compiler and validator for mission scripts.
                | _config - Layout and window parameters configuration.
                | _connection_panel - Connection toolbar component.
                | _jog_panel - Actuator jog controls component.
                | _telemetry_panel - Telemetry dashboard component.
                | _editor_panel - Script editor and execution component.
                | _log_panel - Packet trace and wire stream log component.
                | _mediator - Thread-safe GUI event mediator.
                | _is_initialized - Flag tracking initialization status.
            :methods:
                | __init__ - Initializes GUI engine and mounts subcomponents.
                | is_initialized - Checks if GUI window is ready.
                | load_script - Loads mission script into editor panel.
                | start - Starts Tkinter event loop.
                | stop - Destroys GUI window and exits loop.
    '''

    _root: Tk
    _bot_service: BotService
    _dsl_service: TbotDslService
    _config: GuiConfig
    _connection_panel: ConnectionPanel
    _jog_panel: JogPanel
    _telemetry_panel: TelemetryPanel
    _editor_panel: DslEditorPanel
    _log_panel: LogPanel
    _mediator: GuiEventMediator
    _is_initialized: bool

    def __init__(
        self,
        bot_service: BotService,
        root: Tk | None = None,
        config: GuiConfig | None = None,
    ) -> None:
        '''
            Initializes GUI engine and mounts all subcomponents.

            :param bot_service: Core robot interactor service.
            :param root: Optional parent Tk instance.
            :param config: Optional GuiConfig holding window constants.
            :exceptions: None.
        '''
        self._bot_service = bot_service
        self._dsl_service = TbotDslService()
        self._root = root if root is not None else Tk()
        self._config = config if config is not None else GuiConfig()
        self._is_initialized = False

        self._configure_window()
        self._build_components()
        self._is_initialized = True

    def _configure_window(self) -> None:
        '''
            Configures root window properties, titles, and styles.

            :exceptions: None.
        '''
        cfg: GuiConfig = self._config
        self._root.title(cfg.window_title)

        screen_w: int = self._root.winfo_screenwidth()
        screen_h: int = self._root.winfo_screenheight()
        min_w: int = min(cfg.min_width, screen_w)
        min_h: int = min(cfg.min_height, screen_h - 60)
        self._root.minsize(min_w, min_h)
        self._root.resizable(True, True)

        try:
            self._root.attributes('-zoomed', True)
        except Exception:
            try:
                self._root.state('zoomed')
            except Exception:
                self._root.geometry(f'{screen_w}x{screen_h - 60}+0+0')

        self._root.protocol('WM_DELETE_WINDOW', self._handle_window_close)
        StyleConfigurator.apply(Style(self._root))

    def _build_connection_toolbar(self) -> None:
        '''
            Constructs and mounts connection panel.

            :exceptions: None.
        '''
        conn_cb = ConnectionCallbacks(
            on_connect=self._bot_service.connect,
            on_disconnect=self._bot_service.disconnect,
        )
        self._connection_panel = ConnectionPanel(
            parent=self._root, callbacks=conn_cb
        )
        self._connection_panel.get_widget().pack(fill=X, side=TOP)

    def _build_cockpit_row(self) -> None:
        '''
            Constructs and mounts cockpit controls and telemetry panels.

            :exceptions: None.
        '''
        cfg: GuiConfig = self._config
        cockpit_row: Frame = Frame(self._root, style='Panel.TFrame')
        cockpit_row.pack(
            fill=X, side=TOP, padx=cfg.padding_row_x,
            pady=(cfg.padding_cockpit_y_top, cfg.padding_cockpit_y_bot),
        )

        motion = self._bot_service.get_motion()
        jog_cb = JogPanelCallbacks(
            on_motion=motion.send_motion,
            on_speed=motion.set_speed,
            on_stop=motion.stop_motors,
            on_ping=motion.ping,
            on_clear_err=motion.clear_errors,
        )
        self._jog_panel = JogPanel(parent=cockpit_row, callbacks=jog_cb)
        self._jog_panel.get_widget().pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 4))
        self._jog_panel.bind_keyboard(self._root)

        self._telemetry_panel = TelemetryPanel(parent=cockpit_row)
        self._telemetry_panel.get_widget().pack(side=RIGHT, fill=BOTH, expand=True, padx=(4, 0))

    def _build_editor_and_log(self) -> None:
        '''
            Constructs and mounts script editor panel and packet stream log panel.

            :exceptions: None.
        '''
        cfg: GuiConfig = self._config
        self._log_panel = LogPanel(parent=self._root)
        self._log_panel.get_widget().pack(
            fill=BOTH, side=BOTTOM, expand=True, padx=cfg.padding_row_x,
            pady=(0, cfg.padding_log_y_bot),
        )

        mission = self._bot_service.get_mission_runner()
        mission_cb = MissionCallbacks(
            on_start=mission.start,
            on_pause=mission.pause,
            on_resume=mission.resume,
            on_abort=mission.abort,
        )
        self._editor_panel = DslEditorPanel(
            parent=self._root,
            dsl_service=self._dsl_service,
            callbacks=mission_cb,
        )
        self._editor_panel.get_widget().pack(
            side=TOP, fill=BOTH, expand=True, padx=cfg.padding_row_x,
            pady=(cfg.padding_editor_y_top, cfg.padding_editor_y_bot),
        )

    def _build_mediator(self) -> None:
        '''
            Constructs event mediator and binds observers.

            :exceptions: None.
        '''
        self._mediator = GuiEventMediator(
            root=self._root,
            conn_panel=self._connection_panel,
            telem_panel=self._telemetry_panel,
            log_panel=self._log_panel,
        )
        self._bot_service.get_telemetry().add_observer(self._mediator)

    def _build_components(self) -> None:
        '''
            Constructs and mounts all GUI subpanels into layout rows.

            :exceptions: None.
        '''
        self._build_connection_toolbar()
        self._build_cockpit_row()
        self._build_editor_and_log()
        self._build_mediator()

    def _handle_window_close(self) -> None:
        '''
            Callback invoked on window close event.

            :exceptions: None.
        '''
        self._bot_service.disconnect()
        self.stop()

    def is_initialized(self) -> bool:
        '''
            Checks if GUI window is ready.

            :return: True if ready, False otherwise.
            :exceptions: None.
        '''
        return self._is_initialized

    def load_script(self, content: str) -> None:
        '''
            Loads mission script text into editor panel.

            :param content: Script code string.
            :exceptions: None.
        '''
        self._editor_panel.load_script(content)

    def start(self) -> None:
        '''
            Starts Tkinter event loop.

            :exceptions: None.
        '''
        self._root.mainloop()

    def stop(self) -> None:
        '''
            Destroys GUI window and exits loop.

            :exceptions: None.
        '''
        try:
            self._root.destroy()
        except Exception:
            pass
