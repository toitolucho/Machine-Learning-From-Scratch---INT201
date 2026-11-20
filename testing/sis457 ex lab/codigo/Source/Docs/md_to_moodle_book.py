"""Convert a guide .md into a zip of HTML chapters for Moodle Book "Import chapter".

Usage: python md_to_moodle_book.py guide.md out_dir
Splits on '## ' headings: everything before the first '## Paso' becomes the
Introduction chapter; each later '## ' heading starts a new chapter.
"""
import html
import os
import re
import sys
import unicodedata
import zipfile

PRE_STYLE = ("background:#f6f8fa;border:1px solid #d0d7de;border-radius:4px;"
             "padding:12px;overflow-x:auto;font-size:0.9em;line-height:1.45;")
CODE_STYLE = "background:#f0f0f0;padding:1px 4px;border-radius:3px;"


def inline(text):
    codes = []

    def keep(m):
        codes.append(f'<code style="{CODE_STYLE}">{html.escape(m.group(1))}</code>')
        return "@@C%d@@" % (len(codes) - 1)

    s = re.sub(r"`([^`]+)`", keep, text)
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", lambda m: "<strong>" + m.group(1) + "</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", lambda m: "<em>" + m.group(1) + "</em>", s)
    return re.sub(r"@@C(\d+)@@", lambda m: codes[int(m.group(1))], s)


def render(lines):
    out, i, n = [], 0, len(lines)
    para = []

    def flush_para():
        if para:
            out.append("<p>" + "<br>\n".join(inline(l) for l in para) + "</p>")
            para.clear()

    while i < n:
        line = lines[i]
        s = line.strip()
        if s.startswith("```"):
            flush_para()
            i += 1
            code = []
            while i < n and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            out.append(f'<pre style="{PRE_STYLE}"><code>{html.escape(chr(10).join(code))}</code></pre>')
            continue
        if not s or s == "---":
            flush_para()
            i += 1
            continue
        m = re.match(r"^(#{3,6})\s+(.*)", s)
        if m:
            flush_para()
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue
        if s.startswith("|"):
            flush_para()
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[1:] if not all(re.match(r"^:?-+:?$", c) for c in r)]
            t = ['<table class="table table-bordered table-sm" style="width:auto;border-collapse:collapse;">', "<thead><tr>"]
            t += [f"<th style=\"border:1px solid #c8c8c8;padding:6px 10px;background:#f2f2f2;text-align:left;\">{inline(c)}</th>" for c in head]
            t.append("</tr></thead><tbody>")
            for r in body:
                t.append("<tr>" + "".join(f"<td style=\"border:1px solid #c8c8c8;padding:6px 10px;\">{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue
        if re.match(r"^(\d+\.|[*-])\s+", s):
            flush_para()
            i = render_list(lines, i, out)
            continue
        if para and s.startswith("**"):
            para.append(s)
        else:
            para.append(s)
        i += 1
    flush_para()
    return "\n".join(out)


def indent_of(line):
    return len(line) - len(line.lstrip(" "))


def render_list(lines, i, out):
    base = indent_of(lines[i])
    ordered = bool(re.match(r"^\d+\.", lines[i].strip()))
    tag = "ol" if ordered else "ul"
    out.append(f"<{tag}>")
    n = len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            # list continues only if next non-empty line is an item at same indent
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            if j < n and indent_of(lines[j]) == base and re.match(r"^(\d+\.|[*-])\s+", lines[j].strip()):
                i = j
                continue
            break
        ind = indent_of(line)
        m = re.match(r"^(\d+\.|[*-])\s+(.*)", s)
        if ind == base and m:
            out.append(f"<li>{inline(m.group(2))}")
            i += 1
            if i < n and lines[i].strip() and indent_of(lines[i]) > base and re.match(r"^(\d+\.|[*-])\s+", lines[i].strip()):
                i = render_list(lines, i, out)
            out.append("</li>")
        elif ind > base and m:
            out[-1] = out[-1][:-5] if out[-1].endswith("</li>") else out[-1]
            i = render_list(lines, i, out)
            out.append("</li>")
        else:
            break
    out.append(f"</{tag}>")
    return i


def page(title, body):
    return (f'<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="UTF-8">\n'
            f"<title>{html.escape(title)}</title>\n</head>\n<body>\n{body}\n</body>\n</html>\n")


def main(md_path, out_dir):
    text = open(md_path, encoding="utf-8").read()
    text = text.replace("(sección 5)", "(capítulo «Escenarios de demostración»)")
    lines = text.splitlines()

    chapters, cur_title, cur = [], "Introducción", []
    intro = True
    for line in lines:
        if line.startswith("# "):
            continue  # document title is the Book's own name
        m = re.match(r"^##\s+(.*)", line)
        if m:
            title = m.group(1).strip()
            if intro and not title.startswith("Paso"):
                cur.append("### " + title)  # subtitle and sections 1-4 stay in the introduction
                continue
            intro = False
            chapters.append((cur_title, cur))
            cur_title, cur = title, []
            continue
        cur.append(line)
    chapters.append((cur_title, cur))

    os.makedirs(out_dir, exist_ok=True)
    files = []
    for idx, (title, body) in enumerate(chapters, 1):
        clean = re.sub(r"^\d+\.\s+", "", title)
        clean = clean.replace("`", "")
        slug = re.sub(r"[^a-z0-9]+", "_", unicodedata.normalize("NFKD", clean.lower()).encode("ascii", "ignore").decode()).strip("_")[:40]
        name = f"{idx:02d}_{slug}.html"
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write(page(clean, render(body)))
        files.append(name)
        print(f"{name}  ->  {clean}")

    zip_path = out_dir.rstrip("/\\") + ".zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in files:
            z.write(os.path.join(out_dir, name), name)
    print(f"\nZip: {zip_path} ({len(files)} chapters)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
