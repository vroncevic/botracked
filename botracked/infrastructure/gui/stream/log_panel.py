# -*- coding: UTF-8 -*-

'''
Module
    log_panel.py
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
    Provides LogPanel rendering live packet traffic and wire hex traces.
'''

from __future__ import annotations

from datetime import datetime
from tkinter import BOTH, END, LEFT, RIGHT, X, Scrollbar, Text
from tkinter.ttk import Button, Frame, Label

from botracked.infrastructure.gui.stream.log_panel_config import LogPanelConfig
from botracked.infrastructure.gui.theme.colors import UIColors

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LogPanel:
    '''
        Scrolling packet inspector with colored TX / RX tags and hex data
        inspection.

        It defines:

            :attributes:
                | _frame - Root Frame widget.
                | _config - Configuration instance holding UI tokens.
                | _text - Text widget displaying communication packet log.
            :methods:
                | __init__ - Initializes communication log viewer.
                | get_widget - Returns root Frame widget.
                | append_packet - Appends packet trace line into the log widget.
                | select_all - Selects all text content in packet console.
                | copy_to_clipboard - Copies selected or all content to clipboard.
                | clear - Clears the packet log console.
    '''

    _frame: Frame
    _config: LogPanelConfig
    _text: Text

    def __init__(
        self, parent: Frame, config: LogPanelConfig | None = None
    ) -> None:
        '''
            Initializes communication log viewer.

            :param parent: Parent Tk widget.
            :type parent: Frame

            :param config: Optional log panel configuration instance.
            :type config: LogPanelConfig | None

            :return: None.
            :rtype: None

            :exceptions: None.
        '''
        self._config = config if config is not None else LogPanelConfig()
        self._frame = Frame(
            parent, style='Panel.TFrame', padding=self._config.padding_main
        )
        self._build_ui()

    def get_widget(self) -> Frame:
        '''
            Returns root Frame widget.

            :return: Frame instance.
            :rtype: Frame

            :exceptions: None.
        '''
        return self._frame

    def _build_ui(self) -> None:
        '''
            Constructs toolbar buttons and scrolling text area.

            :return: None.
            :rtype: None

            :exceptions: None.
        '''
        cfg: LogPanelConfig = self._config
        header: Frame = Frame(self._frame, style='Surface.TFrame', padding=cfg.padding_header)
        header.pack(fill=X, pady=(0, 6))

        Label(
            header,
            text=cfg.title_header,
            style='Header.TLabel',
        ).pack(side=LEFT, padx=4)

        clear_btn: Button = Button(
            header, text=cfg.btn_clear, width=8, command=self.clear
        )
        clear_btn.pack(side=RIGHT, padx=2)

        copy_btn: Button = Button(
            header, text=cfg.btn_copy, width=8, command=self.copy_to_clipboard
        )
        copy_btn.pack(side=RIGHT, padx=2)

        select_btn: Button = Button(
            header, text=cfg.btn_select_all, width=10, command=self.select_all
        )
        select_btn.pack(side=RIGHT, padx=2)

        log_frame: Frame = Frame(self._frame, style='Panel.TFrame')
        log_frame.pack(fill=BOTH, expand=True)

        scrollbar: Scrollbar = Scrollbar(log_frame)
        scrollbar.pack(side=RIGHT, fill='y')

        self._text = Text(
            log_frame,
            height=cfg.log_height,
            bg=UIColors.BG_DARK,
            fg=UIColors.TEXT_MAIN,
            font=(cfg.font_family, cfg.font_size),
            yscrollcommand=scrollbar.set,
            relief='flat',
            padx=8,
            pady=8,
            state='disabled',
        )
        self._text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self._text.yview)

        # Configure color tags
        self._text.tag_config('tx', foreground=UIColors.CYAN)
        self._text.tag_config('rx', foreground=UIColors.GREEN)
        self._text.tag_config('time', foreground=UIColors.TEXT_DIM)
        self._text.tag_config('hex', foreground=UIColors.AMBER)

    def append_packet(self, direction: str, opcode_name: str, raw_hex: str) -> None:
        '''
            Appends packet trace line into the log widget.

            :param direction: Direction string ('TX' or 'RX').
            :type direction: str

            :param opcode_name: Opcode mnemonic label.
            :type opcode_name: str

            :param raw_hex: Hex string representation of wire bytes.
            :type raw_hex: str

            :return: None.
            :rtype: None

            :exceptions: None.
        '''
        ts: str = datetime.now().strftime(self._config.time_format)[:-3]
        tag: str = 'tx' if direction == 'TX' else 'rx'

        self._text.configure(state='normal')
        self._text.insert(END, f'[{ts}] ', 'time')
        self._text.insert(END, f'[{direction}] ', tag)
        self._text.insert(END, f'{opcode_name:<16} ', tag)
        self._text.insert(END, f'RAW: {raw_hex}\n', 'hex')
        self._text.see(END)
        self._text.configure(state='disabled')

    def select_all(self) -> None:
        '''
            Selects all text content in the packet stream console.

            :return: None.
            :rtype: None

            :exceptions: None.
        '''
        self._text.tag_add('sel', '1.0', 'end')

    def copy_to_clipboard(self) -> None:
        '''
            Copies current selected text or all logged content to system clipboard.

            :return: None.
            :rtype: None

            :exceptions: None.
        '''
        try:
            content: str = self._text.get('sel.first', 'sel.last')
        except Exception:
            content = self._text.get('1.0', 'end-1c')
        self._frame.clipboard_clear()
        self._frame.clipboard_append(content)

    def clear(self) -> None:
        '''
            Clears the packet log console.

            :return: None.
            :rtype: None

            :exceptions: None.
        '''
        self._text.configure(state='normal')
        self._text.delete('1.0', END)
        self._text.configure(state='disabled')
