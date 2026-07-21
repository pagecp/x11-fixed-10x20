#!/bin/bash
set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"
ORIGINAL="$SOURCE_DIR/fonts/ttf/Fixed20-Original.ttf"
UNICODE="$SOURCE_DIR/fonts/ttf/X11Fixed10x20-Regular.ttf"

if [[ ! -f "$ORIGINAL" || ! -f "$UNICODE" ]]; then
    echo "Font files were not found under fonts/ttf."
    read -r -p "Press Return to close."
    exit 1
fi

mkdir -p "$HOME/Library/Fonts"
cp "$ORIGINAL" "$HOME/Library/Fonts/Fixed20-Original.ttf"
cp "$UNICODE" "$HOME/Library/Fonts/X11Fixed10x20-Regular.ttf"

echo "Both editions have been installed for this user."
echo "Choose ‘Fixed’ at size 20 for Christian's exact 2003 Mac bitmap."
echo "Choose ‘X11 Fixed 10x20’ when broader Unicode coverage is needed."
echo "Logging out may be required before every application sees it."
read -r -p "Press Return to close."
