# Reopens the pages judge_pages.js could not read (bot walls, 403s, empty shells) in real Chrome via browser-harness,
# then writes a full snapshot for a second judge pass: PAGES_SNAPSHOT=<out> node judge_pages.js.
# Usage: python3 browser_pages.py emit IN OUT > run.py && browser-harness < run.py   (rejudge.sh does this)
import json, sys

def emit(src, dst):
    pages = [json.loads(l) for l in open(src)]
    walls = ("just a moment", "captcha", "prove your humanity", "verify you are human", "access denied", "are you a robot")
    unread = lambda p: p["status"] == "blocked" or (p["status"] == "ok" and (len(p["text"]) < 300 or any(w in (p["title"] + p["text"][:600]).lower() for w in walls)))
    todo = [p["url"] for p in pages if unread(p)]
    print(f"""
import json, time
pages = [json.loads(l) for l in open({src!r})]
todo = set({todo!r})
for p in pages:
    if p["url"] not in todo:
        continue
    try:
        goto_url(p.get("final_url") or p["url"])
        wait_for_load(); time.sleep(3)
        title = (js("document.title") or "").replace("\\U0001f434", "").strip()
        desc = js("(document.querySelector('meta[name=description]')||{{}}).content||''") or ""
        text = js("document.body ? document.body.innerText : ''") or ""
        blocked = len(text) < 300 or any(w in (title + text[:600]).lower() for w in ("just a moment", "captcha", "prove your humanity", "verify you are human", "access denied", "are you a robot"))
        p.update(final_url=js("location.href"), title=title, text=(desc + " " + " ".join(text.split()))[:1500], status="blocked" if blocked else "ok", via="browser")
    except Exception as e:
        p.update(via="browser", error=str(e)[:200])
    print(p["status"], p["url"][:90], flush=True)
open({dst!r}, "w").write("".join(json.dumps(p) + "\\n" for p in pages))
""")

if __name__ == "__main__":
    emit(sys.argv[2], sys.argv[3])
