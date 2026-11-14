#!/bin/bash
# Kullanım: bash yap.sh <html dosyası> <çıktı.mp4> [süre_sn]
# Fontları (Playfair Display + Inter, fontsource) hazırlar, kareleri çizer, MP4 üretir.
set -e
HTML=$(realpath "$1"); OUT=$(realpath -m "$2"); DUR=${3:-22.5}
D=$(dirname "$HTML"); W=$(mktemp -d)
if [ ! -d "$D/F" ]; then
  (cd "$W" && npm pack @fontsource/playfair-display @fontsource/inter >/dev/null 2>&1 && for f in *.tgz; do tar xzf "$f" --one-top-level; done)
  mkdir -p "$D/F" && cp "$W"/fontsource-*/package/files/{playfair-display,inter}-latin*-{400,600,700,900}-*.woff2 "$D/F/" 2>/dev/null || true
fi
mkdir -p "$W/fr"
DUR=$DUR python3 "$(dirname "$0")/render.py" "$HTML" "$W/fr"
ffmpeg -y -loglevel error -framerate 30 -i "$W/fr/f%04d.png" -f lavfi -i anullsrc=r=44100:cl=stereo -shortest \
  -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart "$OUT"
echo "Tamam: $OUT"
