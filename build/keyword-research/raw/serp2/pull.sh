#!/bin/zsh
cd "$(dirname $0)"; M=monid
KW=("project management software" "asana pricing" "gantt chart maker")
j(){ python3 -c "import json,sys;print(json.dumps(json.loads(sys.argv[1])))" "$1"; }
for r in 1 2; do for i in 1 2 3; do k=$KW[$i]
  $M run -p dataforseo -e /serp/google-organic -i "{\"keyword\":\"$k\",\"location_code\":2840,\"language_code\":\"en\",\"depth\":10}" -w 120 -o dfs_r${r}_$i.json >/dev/null 2>&1; echo "$(date +%T) dfs r$r $i"
  $M run -p mrscraper -e /serp/google -i "{\"query\":\"$k\",\"region\":\"us\",\"language\":\"en\"}" -w 120 -o mrs_r${r}_$i.json >/dev/null 2>&1; echo "$(date +%T) mrs r$r $i"
  $M run -p cloro -e /google/search -i "{\"query\":\"$k\",\"location\":\"United States\",\"hl\":\"en\"}" -w 120 -o clo_r${r}_$i.json >/dev/null 2>&1; echo "$(date +%T) clo r$r $i"
  [ $r = 1 ] && { $M run -p api.strale.io -e /x402/google-search --query "{\"query\":\"$k\",\"country\":\"US\",\"language\":\"en\",\"num_results\":10}" -w 120 -o str_r${r}_$i.json >/dev/null 2>&1; echo "$(date +%T) str r$r $i"; }
done; done; echo DONE
