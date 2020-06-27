#!/usr/bin/env bash
set -eu
url='https://api.github.com/repos/microsoft/vscode/contents/extensions/theme-defaults/themes'
curl $url | jq -r 'map(.download_url) | .[]' | wget -P data -i -
