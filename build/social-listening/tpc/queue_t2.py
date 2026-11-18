"""Runs the T2 Liquid Death benchmark for Treg and Apify: each model 3 times, one run at a time per tool so each run's tool cost has its own time window."""
import json, subprocess, sys, time, threading
from datetime import datetime
from zoneinfo import ZoneInfo

SCOPE = "monid/monid"
DONE = {"completed", "failed", "error", "cancelled", "timed_out"}
SIDES = {
    "treg": {"task": "d374561b-2649-45e9-8f38-f42520452d73", "done": {"22ee025c-651f-4729-85c1-27fcba5e1683": ["aaa2f92b-0499-4a65-b037-cdac2b095c47"]},
             "envs": ["22ee025c-651f-4729-85c1-27fcba5e1683", "f37e7c35-e788-482e-9a4b-0885e9a3e6c1", "831837f6-3e25-41b4-9f5f-16c873028bac", "e61797a8-c1cc-4ee6-a033-5ed222b09366", "247997ea-fa28-4b9c-abb3-dbf81bd3107c"]},
    "apify": {"task": "42ee53cc-0702-4556-b0a1-1744b0fda0cb", "done": {"c0a1759c-1480-4b06-b890-3637a73649af": ["d3bbf96d-a74b-41ba-84f4-48371846592c"]},
              "envs": ["c0a1759c-1480-4b06-b890-3637a73649af", "733e1f6e-db14-4cb7-9c88-6e7a50b358b9", "9d281aa9-1137-4622-bcf2-15eef49b10d3", "cd96d65d-43d4-41be-a105-287747349c42", "07e199d0-ba2f-4fef-9099-b22a320a25d0"]},
}
LOG = "t2_runs.jsonl"
lock = threading.Lock()

def tpc(*a):
    return subprocess.run(["tpc", "sim", *a, "--scope", SCOPE], capture_output=True, text=True, timeout=120).stdout

def say(msg):
    with lock:
        print(datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%H:%M SF"), msg, flush=True)

def status(run_id):
    try:
        d = json.loads(tpc("run", "get", run_id, "--format", "json")); return d.get("run", d)
    except Exception:
        return {}

def side(name, s):
    plan = [(n, env) for n in range(1, 4) for env in s["envs"] if len(s["done"].get(env, [])) < n]
    for n, env in plan:
        out = ""
        for _ in range(10):
            out = tpc("run", s["task"], "--environment-id", env)
            if "-> run" in out: break
            time.sleep(60)
        if "-> run" not in out:
            say(f"{name} env {env[:8]} run {n}: not queued: {out.strip()[-120:]}"); continue
        rid = out.split("-> run")[1].split()[0]
        say(f"{name} env {env[:8]} run {n}/3 -> {rid}")
        while (r := status(rid)).get("status") not in DONE:
            time.sleep(30)
        with lock:
            open(LOG, "a").write(json.dumps({"side": name, "env": env, "n": n, "run": rid, "status": r.get("status"), "startedAt": r.get("startedAt"), "completedAt": r.get("completedAt"), "costUsd": r.get("costUsd")}) + "\n")
        say(f"{name} {rid[:8]} {r.get('status')}")
    say(f"{name} all done")

ts = [threading.Thread(target=side, args=(k, v)) for k, v in SIDES.items()]
[t.start() for t in ts]; [t.join() for t in ts]
