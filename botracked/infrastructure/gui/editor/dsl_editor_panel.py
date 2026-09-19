# -*- coding: UTF-8 -*-

'''
Module
    dsl_editor_panel.py
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
    Provides DslEditorPanel for authoring, compiling, and running .track mission scripts.
'''

from __future__ import annotations

from tkinter import (
    BOTH,
    BOTTOM,
    END,
    LEFT,
    RIGHT,
    X,
    Scrollbar,
    StringVar,
    Text,
    Tk,
)
from tkinter.ttk import Button, Combobox, Frame, Label

from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.service.dsl.tbot_dsl_service import TbotDslService
from botracked.infrastructure.gui.editor.dsl_editor_panel_config import (
    DslEditorPanelConfig,
)
from botracked.infrastructure.gui.editor.dsl_preset_loader import (
    DslPresetLoader,
)
from botracked.infrastructure.gui.editor.dsl_syntax_highlighter import (
    DslSyntaxHighlighter,
)
from botracked.infrastructure.gui.editor.mission_callbacks import (
    MissionCallbacks,
)
from botracked.infrastructure.gui.theme.colors import UIColors

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslEditorPanel:
    '''
        Script editor and execution manager for .track mission routines.

        It defines:

            :attributes:
                | _frame - Root Frame widget.
                | _dsl_service - Compiler and validator orchestrator.
                | _callbacks - MissionCallbacks bundle holding delegates.
                | _config - Configuration instance holding UI tokens.
                | _editor - Text editing widget for .track scripting.
                | _highlighter - Syntax highlighting manager for .track scripts.
                | _status_var - StringVar holding editor status text.
                | _status_lbl - Label widget for displaying status.
                | _preset_combo - Combobox for selecting script presets.
                | _presets - Dictionary mapping preset names to scripts.
            :methods:
                | __init__ - Initializes mission script editor panel.
                | get_widget - Returns root Frame widget.
                | load_script - Loads script text into the editor.
                | get_script - Returns currently authored script text.
                | set_status - Sets status bar message with custom color.
    '''

    _frame: Frame
    _dsl_service: TbotDslService
    _callbacks: MissionCallbacks
    _config: DslEditorPanelConfig
    _editor: Text
    _highlighter: DslSyntaxHighlighter
    _status_var: StringVar
    _status_lbl: Label
    _preset_combo: Combobox
    _presets: dict[str, str]

    def __init__(
        self,
        parent: Tk | Frame,
        dsl_service: TbotDslService,
        callbacks: MissionCallbacks,
        config: DslEditorPanelConfig | None = None,
    ) -> None:
        '''
            Initializes mission script editor panel.

            :param parent: Parent Tk widget.
            :param dsl_service: Compiler and validator orchestrator.
            :param callbacks: MissionCallbacks bundle holding delegates.
            :param config: Optional editor configuration instance.
            :exceptions: None.
        '''
        self._dsl_service = dsl_service
        self._callbacks = callbacks
        self._config = config if config is not None else DslEditorPanelConfig()
        self._highlighter = DslSyntaxHighlighter()
        self._frame = Frame(
            parent, style='Panel.TFrame', padding=self._config.padding_main
        )
        self._presets = DslPresetLoader.load_presets()
        self._build_ui()

    def get_widget(self) -> Frame:
        '''
            Returns root Frame widget.

            :return: Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def load_script(self, script_text: str) -> None:
        '''
            Loads script text into the editor and applies syntax highlighting.

            :param script_text: Raw .track script text.
            :exceptions: None.
        '''
        self._editor.delete('1.0', END)
        self._editor.insert('1.0', script_text)
        self._highlighter.apply_highlight(self._editor)

    def get_script(self) -> str:
        '''
            Returns currently authored script text.

            :return: String script content.
            :exceptions: None.
        '''
        return self._editor.get('1.0', END)

    def set_status(self, text: str, fg: str = UIColors.TEXT_MAIN) -> None:
        '''
            Sets status bar message with custom color.

            :param text: Message string.
            :param fg: Color hex code.
            :exceptions: None.
        '''
        self._status_var.set(text)
        self._status_lbl.configure(foreground=fg)

    def _build_toolbar(self) -> None:
        '''
            Constructs toolbar widgets including presets and control buttons.

            :exceptions: None.
        '''
        cfg: DslEditorPanelConfig = self._config
        toolbar_frame: Frame = Frame(self._frame, style='Surface.TFrame', padding=cfg.padding_bar)
        toolbar_frame.pack(fill=X, pady=(0, 4))

        Label(toolbar_frame, text=cfg.title_header, style='Header.TLabel').pack(side=LEFT, padx=4)
        Label(toolbar_frame, text=cfg.label_preset, style='CardTitle.TLabel').pack(side=LEFT, padx=(8, 2))

        preset_names: list[str] = list(self._presets.keys())
        self._preset_combo = Combobox(toolbar_frame, values=preset_names, width=22)
        if preset_names:
            self._preset_combo.current(0)
        self._preset_combo.pack(side=LEFT, padx=2)
        self._preset_combo.bind('<<ComboboxSelected>>', self._handle_preset_select)

        Button(toolbar_frame, text=cfg.btn_load, command=self._handle_preset_select).pack(side=LEFT, padx=2)
        Button(toolbar_frame, text=cfg.btn_validate, command=self._handle_validate).pack(side=LEFT, padx=4)
        Button(toolbar_frame, text=cfg.btn_run, style='Success.TButton', command=self._handle_run).pack(side=LEFT, padx=4)
        Button(toolbar_frame, text=cfg.btn_pause, command=self._handle_pause).pack(side=LEFT, padx=2)
        Button(toolbar_frame, text=cfg.btn_resume, command=self._handle_resume).pack(side=LEFT, padx=2)
        Button(toolbar_frame, text=cfg.btn_abort, style='Danger.TButton', command=self._handle_abort).pack(side=LEFT, padx=2)

    def _build_editor_area(self) -> None:
        '''
            Constructs scrollable text editor area.

            :exceptions: None.
        '''
        cfg: DslEditorPanelConfig = self._config
        area: Frame = Frame(self._frame, style='Panel.TFrame')
        area.pack(fill=BOTH, expand=True)

        scrollbar: Scrollbar = Scrollbar(area)
        scrollbar.pack(side=RIGHT, fill='y')

        self._editor = Text(
            area,
            bg=UIColors.BG_DARK,
            fg=UIColors.TEXT_MAIN,
            insertbackground=UIColors.CYAN,
            font=(cfg.font_family, cfg.font_size),
            yscrollcommand=scrollbar.set,
            relief='flat',
            height=cfg.editor_height,
        )
        self._editor.pack(fill=BOTH, expand=True)
        scrollbar.config(command=self._editor.yview)

        self._highlighter.setup_tags(self._editor)
        self._editor.bind(
            '<KeyRelease>',
            lambda _event: self._highlighter.apply_highlight(self._editor),
        )

        first_key: str = next(iter(self._presets)) if self._presets else 'default'
        self.load_script(self._presets.get(first_key, DslPresetLoader.DEFAULT_SCRIPT))

    def _build_status_bar(self) -> None:
        '''
            Constructs status bar for diagnostic feedback.

            :exceptions: None.
        '''
        cfg: DslEditorPanelConfig = self._config
        status_frame: Frame = Frame(self._frame, style='Surface.TFrame', padding=cfg.padding_bar)
        status_frame.pack(fill=X, side=BOTTOM, pady=(4, 0))

        self._status_var = StringVar(value=cfg.default_status)
        self._status_lbl = Label(
            status_frame,
            textvariable=self._status_var,
            style='Panel.TLabel',
            foreground=UIColors.TEXT_MUTED,
            font=('Helvetica', 9, 'italic'),
        )
        self._status_lbl.pack(side=LEFT, padx=4)

    def _build_ui(self) -> None:
        '''
            Constructs toolbar, script editor, and status bar.

            :exceptions: None.
        '''
        self._build_toolbar()
        self._build_editor_area()
        self._build_status_bar()

    def _handle_preset_select(self, _event: object = None) -> None:
        '''
            Callback invoked when a script preset is chosen.

            :param _event: Optional event triggering selection.
            :exceptions: None.
        '''
        selected_name: str = self._preset_combo.get()
        if selected_name in self._presets:
            self.load_script(self._presets[selected_name])
            self.set_status(f'ℹ️ Loaded preset: {selected_name}', UIColors.CYAN)

    def _handle_validate(self) -> None:
        '''
            Callback invoked to validate script syntax and semantics.

            :exceptions: None.
        '''
        code: str = self.get_script()
        valid: bool
        msg: str
        valid, msg = self._dsl_service.validate(code)
        if valid:
            self.set_status(f'✅ {msg}', UIColors.GREEN)
        else:
            self.set_status(f'❌ {msg}', UIColors.RED)

    def _handle_run(self) -> None:
        '''
            Callback invoked to compile and run the mission script.

            :exceptions: None.
        '''
        code: str = self.get_script()
        valid: bool
        msg: str
        valid, msg = self._dsl_service.validate(code)
        if not valid:
            self.set_status(f'❌ Compilation failed: {msg}', UIColors.RED)
            return

        try:
            steps: list[CompiledStep] = self._dsl_service.compile(code)
            self.set_status(f'🚀 Running mission ({len(steps)} steps)...', UIColors.GREEN)
            self._callbacks.on_start(steps)
        except Exception as err:
            self.set_status(f'❌ Compilation failed: {err}', UIColors.RED)

    def _handle_pause(self) -> None:
        '''
            Callback invoked to pause the running mission.

            :exceptions: None.
        '''
        self.set_status('⏸ Mission paused', UIColors.AMBER)
        self._callbacks.on_pause()

    def _handle_resume(self) -> None:
        '''
            Callback invoked to resume the paused mission.

            :exceptions: None.
        '''
        self.set_status('⏯ Mission resumed', UIColors.GREEN)
        self._callbacks.on_resume()

    def _handle_abort(self) -> None:
        '''
            Callback invoked to abort the active mission.

            :exceptions: None.
        '''
        self.set_status('⏹ Mission aborted', UIColors.RED)
        self._callbacks.on_abort()
