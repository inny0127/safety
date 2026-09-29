#!/bin/sh
# Full (non-subset) fonts. Needed only when the poster text changes.
set -e
cd "$(dirname "$0")/fonts"
G=https://raw.githubusercontent.com/google/fonts/main/ofl
curl -sSfL -o BlackHanSans-Regular.ttf "$G/blackhansans/BlackHanSans-Regular.ttf"
for s in Bold ExtraBold Black; do curl -sSfL -o GothicA1-$s.ttf "$G/gothica1/GothicA1-$s.ttf"; done
