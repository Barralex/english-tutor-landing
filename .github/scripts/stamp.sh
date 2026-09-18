#!/usr/bin/env bash
# Cache busting at deploy time. GitHub Pages sends max-age=600 and the asset
# names never change, so a browser that already has site.css keeps showing the
# old styles after a deploy. Every local asset URL gets ?v=<commit> appended in
# the published copy only; the repository keeps clean URLs.
set -euo pipefail

v="${GITHUB_SHA::7}"
pages="index.html kids/index.html professionals/index.html"

sed -E -i "s#((href|src)=\"(\.\./)?assets/[^\"?]+)\"#\1?v=$v\"#g" $pages
sed -E -i "s#url\(\"([a-z-]+\.css)\"\)#url(\"\1?v=$v\")#g" assets/css/site.css

n=$(grep -c "?v=$v" $pages assets/css/site.css | awk -F: '{s+=$2} END {print s}')
echo "stamped $n asset references with v=$v"
[ "$n" -ge 5 ] || { echo "cache busting stamped nothing: the asset URL pattern changed"; exit 1; }
