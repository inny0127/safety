#!/bin/sh
# Full (non-subset) fonts. Needed only when the poster text changes.
set -e
cd "$(dirname "$0")/fonts"
G=https://raw.githubusercontent.com/google/fonts/main/ofl
curl -sSfL -o BlackHanSans-Regular.ttf "$G/blackhansans/BlackHanSans-Regular.ttf"
curl -sSfL -o GasoekOne-Regular.ttf "$G/gasoekone/GasoekOne-Regular.ttf"
curl -sSfL -o DoHyeon-Regular.ttf "$G/dohyeon/DoHyeon-Regular.ttf"
for s in Bold ExtraBold Black; do curl -sSfL -o GothicA1-$s.ttf "$G/gothica1/GothicA1-$s.ttf"; done
