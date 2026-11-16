"""Post-render: write llms-full.txt (plain-text program + speakers) into the site output.

Built from program.qmd and speakers.qmd on every render, so talk titles never go stale.
Standard library only (runs in CI as a Quarto post-render script).
"""
import html, os, re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
out_dir = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", root / "_site"))
if not out_dir.is_absolute():
    out_dir = root / out_dir

def text(s):
    s = re.sub(r"<br\s*/?>", " — ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()

lines = []
llms = (root / "llms.txt").read_text(encoding="utf-8").rstrip()
lines += [llms, "", "---", "", "# Full program", ""]

prog = (root / "program.qmd").read_text(encoding="utf-8")
for line in prog.splitlines():
    if line.startswith("## "):
        lines += ["", line.replace("## ", "## ", 1), ""]
    m = re.match(r'<div class="slot[^"]*"><div class="time">(.*?)</div><div class="event">(.*)</div></div>\s*$', line)
    if not m:
        continue
    time, ev = m.group(1), m.group(2)
    ribbon = re.search(r'<span class="ribbon">(.*?)</span>', ev)
    ev_wo = re.sub(r'<span class="ribbon">.*?</span>', "", ev)
    head = re.split(r"<ul", ev_wo, 1)[0]
    entry = f"- {text(time)}: {text(head)}"
    if ribbon:
        entry += f" ({text(ribbon.group(1))})"
    lines.append(entry)
    for li in re.findall(r"<li>(.*?)</li>", ev_wo):
        who = re.search(r'<span class="who">(.*?)</span>', li)
        talk = re.search(r'<span class="talk[^"]*">(.*?)</span>', li)
        if who:
            lines.append(f"  - {text(who.group(1))}: {text(talk.group(1)) if talk else ''}".rstrip(": "))
        else:
            lines.append(f"  - {text(li)}")

lines += ["", "# Speakers and organizers", ""]
spk = (root / "speakers.qmd").read_text(encoding="utf-8")
section = None
for block in re.split(r"\n(?=## |::: \{\.person-card\})", spk):
    if block.startswith("## "):
        section = block.splitlines()[0][3:].strip()
        continue
    name = re.search(r"^### (.+)$", block, re.M)
    if not name:
        continue
    role = re.search(r'<p class="role">(.*?)</p>', block)
    aff = re.search(r'<p class="affiliation">(.*?)</p>', block)
    link = re.search(r'<a href="(https?://[^"]+)"', block)
    parts = [text(name.group(1))]
    if role: parts.append(text(role.group(1)))
    if aff: parts.append(text(aff.group(1)))
    if link: parts.append(link.group(1))
    lines.append("- " + " · ".join(parts))

out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "llms-full.txt").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
print("llms-full.txt written")
