"""Corporate domain from the 10-K sentence where the company names its own website."""
import html, json, re, time, urllib.request
UA = {"User-Agent": "The Prompting Company research contact@promptingco.com"}
def text_of(doc):
    doc = re.sub(r"(?is)<(script|style|ix:header)[^>]*>.*?</\1>", " ", doc)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", doc)))
OWN = re.compile(r"[^.]{0,200}\b(?:our|the company's|company's)\s+(?:corporate\s+|primary\s+|principal\s+|investor relations\s+|internet\s+|main\s+)?(?:web\s?site|internet (?:web)?site|internet address|website address|web address)\b[^.]{0,250}?\b(?:https?://)?(?:www\.)?([a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,})(?:/[^\s,;)]*)?", re.I)
prov = json.load(open("provenance.json"))
out = []
for p in prov:
    time.sleep(0.15)
    t = text_of(urllib.request.urlopen(urllib.request.Request(p["ten_k"], headers=UA), timeout=60).read().decode("utf8", "replace"))
    hits = [(m.group(1).lower(), m.group(0).strip()[-300:]) for m in OWN.finditer(t)]
    hits = [h for h in hits if "sec.gov" not in h[0]]
    out.append({"id": p["id"], "company": p["company"], "own_site_hits": hits[:4], "old_key_named": p["domain_named_in_10k"]})
json.dump(out, open("domains_v2_raw.json", "w"), indent=1)
found = sum(bool(o["own_site_hits"]) for o in out)
print(found, "of", len(out), "have an own-website sentence")
