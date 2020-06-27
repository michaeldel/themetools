from __future__ import annotations

import enum
import sys

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class VSCodeTheme:
    name: str
    parent: Optional[VSCodeTheme]
    spec: List[Scope]


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
