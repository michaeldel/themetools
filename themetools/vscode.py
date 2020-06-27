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
                font_style=tc['settings'].get('fontStyle'),
                foreground=tc['settings'].get('foreground'),
            )
            paths = [tc['scope']] if isinstance(tc['scope'], str) else tc['scope']
            scope = Scope(name=tc.get('name'), paths=paths, settings=settings)
            spec.append(scope)

        return cls(name=data['name'], spec=spec, parent=parent)


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
    BOLD = 'bold'
    UNDERLINE = 'underline'


assert len(sys.argv) == 2
theme = VSCodeTheme.load(sys.argv[1])
