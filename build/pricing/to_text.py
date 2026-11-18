import sys, re, html
s = open(sys.argv[1], errors="ignore").read()
s = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", s)
s = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr|section|span|button|a)>", "\n", s)
s = html.unescape(re.sub(r"<[^>]+>", " ", s))
lines = [re.sub(r"[ \t ]+", " ", l).strip() for l in s.split("\n")]
open(sys.argv[2], "w").write("\n".join(l for l in lines if l))
