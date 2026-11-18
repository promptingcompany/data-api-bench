"""Exchange-listed operating companies that file 10-Ks, with SEC business address, from the Nov 3 2026 submissions dump."""
import json, sys, zipfile
from datetime import date
tick = json.load(open("tickers_exchange.json"))
listed = {}
for cik, name, ticker, ex in tick["data"]:
    if ex in ("Nasdaq", "NYSE", "CBOE", "TXSE"):
        listed.setdefault(int(cik), {"tickers": [], "exchanges": set()})
        listed[int(cik)]["tickers"].append(ticker); listed[int(cik)]["exchanges"].add(ex)
z = zipfile.ZipFile(sys.argv[1])
out = []
for cik, info in listed.items():
    try: s = json.loads(z.read(f"CIK{cik:010d}.json"))
    except KeyError: continue
    rec = s["filings"]["recent"]
    tenk = [(d, a, p) for f, d, a, p in zip(rec["form"], rec["filingDate"], rec["accessionNumber"], rec["primaryDocument"]) if f == "10-K"]
    if not tenk or tenk[0][0] < "2025-06-01": continue
    sic = str(s.get("sic") or "")
    if sic in ("6770", "6798", "6726", "6722", "6221") or s.get("entityType") != "operating": continue
    biz = s["addresses"].get("business") or {}
    out.append({"cik": cik, "name": s["name"], "tickers": info["tickers"], "exchanges": sorted(info["exchanges"]), "sic": sic, "sic_desc": s.get("sicDescription"),
                "state_or_country": biz.get("stateOrCountry"), "country_desc": biz.get("stateOrCountryDescription"), "city": biz.get("city"),
                "latest_10k": {"date": tenk[0][0], "accession": tenk[0][1], "doc": tenk[0][2]}})
json.dump(out, open("universe.json", "w"), indent=1)
from collections import Counter
US = set("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY PR".split())
print(len(out), "10-K filers;", sum(o["state_or_country"] in US for o in out), "US HQ")
print(Counter(o["country_desc"] for o in out if o["state_or_country"] not in US).most_common(25))
