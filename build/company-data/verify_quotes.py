import html, json, re, time, urllib.request
UA = {"User-Agent": "The Prompting Company research contact@promptingco.com"}
norm = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
def text_of(doc):
    doc = re.sub(r"(?is)<(script|style|ix:header)[^>]*>.*?</\1>", " ", doc)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", doc)))
c = {x["cik"]: x for x in json.load(open("candidates_step2.json"))}
res = []
for r in json.load(open("employees.json")):
    if r["status"] != "ok": continue
    time.sleep(0.15)
    t = norm(text_of(urllib.request.urlopen(urllib.request.Request(c[r["cik"]]["url"], headers=UA), timeout=60).read().decode("utf8", "replace")))
    q = norm(r["quote"] or "")
    num = f"{r['employees']:,}"
    res.append({"cik": r["cik"], "name": r["name"], "quote_found": bool(q) and q in t, "number_in_quote": num in (r["quote"] or "") or str(r["employees"]) in (r["quote"] or "")})
json.dump(res, open("quote_check.json", "w"), indent=1)
bad = [x for x in res if not (x["quote_found"] and x["number_in_quote"])]
print(len(res), "checked;", len(bad), "flagged"); [print(" ", x) for x in bad]
