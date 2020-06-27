import sys

import json5 as json


def load_theme(filename: str):
    with open(filename, 'r') as f:
        theme = json.load(f)

    assert theme['$schema'] == 'vscode://schemas/color-theme'
    return theme


assert len(sys.argv) == 2
theme = load_theme(sys.argv[1])
print(f"Theme: {theme['name']}")

scopes = {}

for tc in theme['tokenColors']:
    settings = tc['settings']
    scope = tc['scope']

    if isinstance(scope, str):
        scopes[scope] = settings
    elif isinstance(scope, list):
        for s in scope:
            scopes[s] = settings
    else:
        raise

for scope, settings in scopes.items():
    hexcode = settings['foreground'].lstrip('#').upper()
    r, g, b = tuple(int(hexcode[i : i + 2], 16) for i in (0, 2, 4))
    formatted = f"\033[38;2;{r};{g};{b}m#{hexcode.lower()}\033[0m"

    print(scope, formatted)
