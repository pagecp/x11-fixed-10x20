#!/bin/bash
set -euo pipefail

found=false
for NAME in Fixed20-Original.ttf X11Fixed10x20-Regular.ttf; do
    FONT="$HOME/Library/Fonts/$NAME"
    if [[ -f "$FONT" ]]; then
        mv "$FONT" "$HOME/.Trash/$NAME"
        found=true
    fi
done
if $found; then echo "The fonts were moved to the Trash."
else echo "The fonts are not installed in ~/Library/Fonts."
fi
read -r -p "Press Return to close."
