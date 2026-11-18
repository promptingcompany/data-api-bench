#!/bin/bash
# usage: snap.sh id url -> out/html/<id>.html, out/text/<id>.txt
id="$1"; url="$2"
timeout 90 google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --virtual-time-budget=25000 \
  --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36" \
  --window-size=1400,3000 --dump-dom "$url" > "out/html/$id.html" 2>/dev/null
python3 to_text.py "out/html/$id.html" "out/text/$id.txt"
echo "$id $(wc -c < out/text/$id.txt) dollars=$(grep -c '\$' out/text/$id.txt)"
