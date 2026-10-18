# Detect string-escape corruption in raw exam JSON: control chars (\t \r \x08 \x0b \x0c \x07)
# and newlines inside $...$ math spans (e.g. "\notin" written in a non-raw string -> "\n" + "otin").
import json, re, glob, sys
# an escaped dollar (backslash + $, e.g. a MIPS register) is not a math delimiter
RX = re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$|(?<!\\)\$(.+?)(?<!\\)\$", re.S)
bad = 0
def walk(x, where):
    global bad
    if isinstance(x, str):
        for ch in "\t\r\x08\x0b\x0c\x07":
            if ch in x:
                bad += 1; print(f"{where}: control char {ch!r}: ...{x[max(0,x.index(ch)-40):x.index(ch)+20]!r}")
        # fenced code blocks are literal (no math): drop them before looking for $...$ spans
        scan = re.sub(r"^```[A-Za-z0-9+#_-]{0,12}[ \t]*\n.*?^```[ \t]*$", "", x, flags=re.S | re.M)
        for m in RX.finditer(scan):
            span = m.group(1) or m.group(2)
            if "\n" in span:
                bad += 1; print(f"{where}: newline inside math: {span[:80]!r}")
    elif isinstance(x, list):
        for i, v in enumerate(x): walk(v, f"{where}[{i}]")
    elif isinstance(x, dict):
        for k, v in x.items(): walk(v, f"{where}.{k}")
EXAM_RE = re.compile(r"^(\d{2}[A-Z]-[A-Z]|SAMP-\d+|DEMO-[A-Z])\.json$")
for f in sorted(glob.glob("tools/raw/*.json")):
    if not EXAM_RE.match(f.replace("\\", "/").split("/")[-1]): continue
    walk(json.load(open(f, encoding="utf-8")), f.split("\\")[-1].split("/")[-1])
print("escape problems:", bad); sys.exit(1 if bad else 0)
