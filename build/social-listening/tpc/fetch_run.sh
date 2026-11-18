#!/bin/bash
# Usage: fetch_run.sh <run-uuid>  -> runs/<id8>/{run.json,home.bin,agent-user/work}
set -e
R=$1; D=runs/${R:0:8}; mkdir -p $D
TOK=$(tpc auth token show 2>/dev/null | tail -1)
J=$(mktemp)
curl -s -c $J -b $J -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -X POST https://app.promptingco.com/api/auth/organization/set-active -d '{"organizationSlug":"monid"}' >/dev/null
tpc sim run get $R --scope monid/monid --format json > $D/run.json
curl -s -b $J -H "Authorization: Bearer $TOK" -o $D/home.bin "https://app.promptingco.com/api/v1/agent-simulation/runs/$R/sandbox-home"
rm -f $J
(cd $D && tar -xf home.bin 'agent-user/work/out' 'agent-user/work/brand.txt' 2>/dev/null || tar -xzf home.bin 'agent-user/work/out' 'agent-user/work/brand.txt')
ls $D/agent-user/work/out
