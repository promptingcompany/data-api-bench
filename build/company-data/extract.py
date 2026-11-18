"""Sample candidates and pull the employee sentence and website from each one's latest 10-K."""
import html, json, random, re, sys, time, urllib.request
UA = {"User-Agent": "The Prompting Company research contact@promptingco.com"}
US = set("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY PR".split())
HAVENS = {"Bermuda", "Cayman Islands", "Jersey", "Guernsey", "Bahamas", "British Virgin Islands", "Marshall Islands", None}
def get(url):
    for attempt in range(4):
        try:
            time.sleep(0.15 + attempt * 2)
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode("utf8", "replace")
        except Exception as error: last = error
    raise last
def text_of(doc):
    doc = re.sub(r"(?is)<(script|style|ix:header)[^>]*>.*?</\1>", " ", doc)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", doc)))
EMP = re.compile(r"[^.]{0,250}\b(employ(?:ed|ees)|full-time|team members|associates|headcount|workforce)\b[^.]{0,250}\.", re.I)
NUM = re.compile(r"\b\d{1,3}(?:,\d{3})+\b|\b\d{2,6}\b")
WEB = re.compile(r"\b(?:https?://)?(?:www\.)([a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,})", re.I)
universe = [u for u in json.load(open("universe.json")) if u["country_desc"] is not None]
rng = random.Random(20261116)
us = [u for u in universe if u["state_or_country"] in US]
intl = [u for u in universe if u["state_or_country"] not in US and u["country_desc"] not in HAVENS and u["country_desc"] != "United States"]
picks = rng.sample(us, 110) + rng.sample(intl, min(45, len(intl)))
print(len(us), "US pool;", len(intl), "non-US pool", flush=True)
out = []
for i, u in enumerate(picks):
    k = u["latest_10k"]
    url = f"https://www.sec.gov/Archives/edgar/data/{u['cik']}/{k['accession'].replace('-', '')}/{k['doc']}"
    try: t = text_of(get(url))
    except Exception as error:
        out.append({**u, "url": url, "error": str(error)}); continue
    sentences = [m.group(0).strip() for m in EMP.finditer(t) if NUM.search(m.group(0)) and re.search(r"employ|full-time|team members|associates|headcount|workforce", m.group(0), re.I)]
    sentences = [s for s in sentences if re.search(r"(had|have|employ|employed|approximately|total of|consisted of)", s, re.I)][:8]
    sites = {}
    for m in WEB.finditer(t):
        d = m.group(1).lower().rstrip(".")
        if "sec.gov" in d: continue
        sites[d] = sites.get(d, 0) + 1
    out.append({**u, "url": url, "employee_sentences": sentences, "websites": sorted(sites.items(), key=lambda kv: -kv[1])[:5]})
    if i % 20 == 0:
        print(i, u["name"], flush=True); json.dump(out, open("candidates_raw.json", "w"), indent=1)
json.dump(out, open("candidates_raw.json", "w"), indent=1)
print("done", len(out), "errors", sum("error" in o for o in out))
