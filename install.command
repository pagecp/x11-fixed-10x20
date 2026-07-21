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

echo "Where should the fonts be installed?"
echo
echo "  1) Current user only — ~/Library/Fonts (no sudo)"
echo "  2) All users — /Library/Fonts (requires sudo)"
echo
read -r -p "Choice [1]: " CHOICE
CHOICE="${CHOICE:-1}"

case "$CHOICE" in
    1)
        DESTINATION="$HOME/Library/Fonts"
        mkdir -p "$DESTINATION"
        cp "$ORIGINAL" "$DESTINATION/Fixed20-Original.ttf"
        cp "$UNICODE" "$DESTINATION/X11Fixed10x20-Regular.ttf"
        ;;

    2)
        DESTINATION="/Library/Fonts"
        sudo mkdir -p "$DESTINATION"
        sudo cp "$ORIGINAL" "$DESTINATION/Fixed20-Original.ttf"
        sudo cp "$UNICODE" "$DESTINATION/X11Fixed10x20-Regular.ttf"
        ;;

    *)
        echo "Invalid choice."
        exit 1
        ;;
esac

echo
echo "Both editions were installed in:"
echo "$DESTINATION"
echo
echo "Choose ‘Fixed’ at size 20 for the exact 2003 Mac bitmap."
echo "Choose ‘X11 Fixed 10x20’ for broader Unicode coverage."
echo
read -r -p "Press Return to close."
