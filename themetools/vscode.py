from __future__ import annotations

import enum
import os
import pathlib
import sys

from dataclasses import dataclass
from typing import List, Optional

import pyjson5 as json


@dataclass(frozen=True)
class VSCodeTheme:
    name: str
    parent: Optional[VSCodeTheme]
    spec: List[Scope]

    @classmethod
    def load(cls, filename: str):
        with open(filename, 'r') as f:
            data = json.load(f)
        assert data['$schema'] == 'vscode://schemas/color-theme'

        parent = None
        if parent_filename := data.get('include'):
            directory = pathlib.Path(os.path.dirname(filename))
            parent = cls.load(directory / parent_filename)

        spec = []
        for path, hexcode in data.get('colors', {}).items():
            settings = Settings(foreground=hexcode)
            spec.append(Scope(name=None, paths=[path], settings=settings))

        for tc in data.get('tokenColors', []):
            settings = Settings(
                font_style=FontStyle[tc['settings'].get('fontStyle', 'normal').upper()],
                foreground=tc['settings'].get('foreground'),
            )
            paths = [tc['scope']] if isinstance(tc['scope'], str) else tc['scope']
            scope = Scope(name=tc.get('name'), paths=paths, settings=settings)
            spec.append(scope)

        return cls(name=data['name'], spec=spec, parent=parent)

    def pprint(self):
        if self.parent:
            self.parent.pprint()

        for scope in self.spec:
            for path in scope.paths:
                if scope.settings.foreground:
                    hexcode = scope.settings.foreground.lstrip('#').upper()
                    if len(hexcode) == 3:
                        hexcode = f'{hexcode}{hexcode}'
                    elif (
                        len(hexcode) == 4
                    ):  # TODO: properly handle that case (e.g. #0000)
                        hexcode = f'{hexcode}{hexcode}'

                    r, g, b = tuple(int(hexcode[i : i + 2], 16) for i in (0, 2, 4))
                    formatted = f"\033[38;2;{r};{g};{b}m#{hexcode.lower()}\033[0m"
                else:
                    formatted = "#xxxxxx"

                if scope.settings.font_style == FontStyle.BOLD:
                    formatted = f"\033[1m{formatted}\033[0m"
                elif scope.settings.font_style == FontStyle.ITALIC:
                    formatted = f"\033[3m{formatted}\033[0m"
                elif scope.settings.font_style == FontStyle.UNDERLINE:
                    formatted = f"\033[4m{formatted}\033[0m"
                print(path, formatted)


@dataclass(frozen=True)
class Scope:
    name: Optional[str]
    paths: List[str]
    settings: Settings


@dataclass(frozen=True)
class Settings:
    font_style: Optional[FontStyle] = None
    foreground: Optional[str] = None


class FontStyle(enum.Enum):
    NORMAL = 'normal'
    BOLD = 'bold'
    ITALIC = 'italic'
    UNDERLINE = 'underline'


assert len(sys.argv) == 2
theme = VSCodeTheme.load(sys.argv[1])
theme.pprint()
