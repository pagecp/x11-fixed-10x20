#!/bin/bash
set -euo pipefail

USER_FONT_DIR="$HOME/Library/Fonts"
SYSTEM_FONT_DIR="/Library/Fonts"
FOUND=false

for NAME in Fixed20-Original.ttf X11Fixed10x20-Regular.ttf; do
    USER_FONT="$USER_FONT_DIR/$NAME"

    if [[ -f "$USER_FONT" ]]; then
        mv "$USER_FONT" "$HOME/.Trash/$NAME"
        FOUND=true
        echo "Moved user font to Trash: $NAME"
    fi
done

SYSTEM_FOUND=false

for NAME in Fixed20-Original.ttf X11Fixed10x20-Regular.ttf; do
    if [[ -f "$SYSTEM_FONT_DIR/$NAME" ]]; then
        SYSTEM_FOUND=true
    fi
done

if $SYSTEM_FOUND; then
    echo
    read -r -p \
        "System-wide fonts were found in /Library/Fonts. Remove them? [y/N] " \
        ANSWER

    case "$ANSWER" in
        y|Y|yes|YES)
            sudo rm -f \
                "$SYSTEM_FONT_DIR/Fixed20-Original.ttf" \
                "$SYSTEM_FONT_DIR/X11Fixed10x20-Regular.ttf"
            FOUND=true
            echo "System-wide fonts removed."
            ;;
    esac
fi

if ! $FOUND; then
    echo "No installed X11 Fixed 10x20 fonts were found."
fi

echo
read -r -p "Press Return to close."
