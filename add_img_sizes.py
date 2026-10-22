import re, subprocess, pathlib, urllib.parse, sys

apply = "--apply" in sys.argv

for html in sorted(pathlib.Path(".").glob("*.html")):
    text = html.read_text(encoding="utf-8")

    def fix(m):
        tag = m.group(0)
        if re.search(r"\s(width|height)=", tag):
            return tag  # ha già le dimensioni
        src = re.search(r'src="([^"]+)"', tag)
        if not src or src.group(1).startswith(("http", "data:")):
            return tag
        path = html.parent / urllib.parse.unquote(src.group(1))
        if not path.is_file():
            print(f"  file non trovato: {src.group(1)}")
            return tag
        out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
                             capture_output=True, text=True).stdout
        w = re.search(r"pixelWidth: (\d+)", out)
        h = re.search(r"pixelHeight: (\d+)", out)
        if not (w and h):
            return tag
        print(f"  {src.group(1)} -> {w.group(1)} x {h.group(1)}")
        return tag.replace("<img", f'<img width="{w.group(1)}" height="{h.group(1)}"', 1)

    new = re.sub(r"<img\b[^>]*>", fix, text)
    if new != text:
        print(f"{html.name}: {'modificato' if apply else 'da modificare'}")
        if apply:
            html.write_text(new, encoding="utf-8")
