"""Business overview from each 10-K and a live check of the website it names."""
import html, json, re, ssl, time, urllib.request
UA = {"User-Agent": "The Prompting Company research contact@promptingco.com"}
BROWSER = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"}
def get(url, headers, timeout=60):
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout)
def text_of(doc):
    doc = re.sub(r"(?is)<(script|style|ix:header)[^>]*>.*?</\1>", " ", doc)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", doc)))
def overview(t):
    hits = [m.start() for m in re.finditer(r"(?i)item\s*1\.?\s*(?:&#160;|\s)*business\b", t)]
    start = hits[1] if len(hits) > 1 else (hits[0] if hits else 0)
    return t[start:start + 2500]
def live(domain):
    for url in (f"https://{domain}", f"https://www.{domain}"):
        try:
            r = get(url, BROWSER, 20)
            return {"tried": url, "status": r.status, "final": r.geturl()}
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 405, 429): return {"tried": url, "status": e.code, "final": e.geturl(), "note": "blocked but up"}
            last = {"tried": url, "error": f"HTTP {e.code}"}
        except Exception as e: last = {"tried": url, "error": str(e)[:120]}
    return last
c = json.load(open("candidates_raw.json"))
for i, x in enumerate(c):
    time.sleep(0.15)
    try: x["overview"] = overview(text_of(get(x["url"], UA).read().decode("utf8", "replace")))
    except Exception as e: x["overview_error"] = str(e)[:120]
    x["site_checks"] = {d: live(d) for d, _ in (x.get("websites") or [])[:2]}
    if i % 25 == 0: print(i, flush=True); json.dump(c, open("candidates_step2.json", "w"), indent=1)
json.dump(c, open("candidates_step2.json", "w"), indent=1); print("done", flush=True)
