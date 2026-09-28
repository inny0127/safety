#!/bin/sh
# Full (non-subset) fonts, needed only when the poster text changes.
set -e
cd "$(dirname "$0")/fonts"
G=https://raw.githubusercontent.com/google/fonts/main/ofl
curl -sSfL -o NotoSerifKR-var.ttf "$G/notoserifkr/NotoSerifKR%5Bwght%5D.ttf"
for w in 400 600 900; do python3 -m fontTools.varLib.instancer NotoSerifKR-var.ttf wght=$w --update-name-table -o NotoSerifKR-$w.ttf -q; done
rm NotoSerifKR-var.ttf
for s in Regular Medium SemiBold Bold; do curl -sSfL -o IBMPlexSansKR-$s.ttf "$G/ibmplexsanskr/IBMPlexSansKR-$s.ttf"; done
for s in Regular Medium; do curl -sSfL -o IBMPlexMono-$s.ttf "$G/ibmplexmono/IBMPlexMono-$s.ttf"; done
