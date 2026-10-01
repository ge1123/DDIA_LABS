"""Build the static DDIA notebook from Markdown and shared templates."""

import json
import re
import shutil
from datetime import date
from html import escape
from pathlib import Path
from string import Template

import markdown


SITE = Path(__file__).resolve().parent
OUTPUT = SITE / "public"
STATUS = {
    "pending": "尚未開始",
    "draft": "示範草稿",
    "in-progress": "整理中",
    "complete": "已整理",
}


def render(name, **values):
    return Template((SITE / "templates" / name).read_text(encoding="utf-8")).substitute(values)


def slugify(value, separator):
    return re.sub(r"[^\w]+", separator, value.lower()).strip(separator) or "section"


def badge(chapter):
    return f'<span class="chapter-status {chapter["status"]}">{STATUS[chapter["status"]]}</span>'


def chapter_url(chapter, root):
    return f'{root}chapters/{chapter["number"]:02d}.html'


def navigation(parts, root, current=None):
    groups = []
    for part in parts:
        links = []
        for chapter in part["chapters"]:
            active = ' aria-current="page"' if chapter["number"] == current else ""
            links.append(
                f'<li><a href="{chapter_url(chapter, root)}"{active}>'
                f'<span class="nav-number">{chapter["number"]:02d}</span>'
                f'<span>{escape(chapter["title"])}</span>'
                f'<i class="status-dot {chapter["status"]}" aria-hidden="true"></i>'
                f'<span class="sr-only">（{STATUS[chapter["status"]]}）</span></a></li>'
            )
        groups.append(
            f'<div class="nav-group"><p><span>{part["roman"]}</span> {escape(part["title"])}</p>'
            f'<ol>{"".join(links)}</ol></div>'
        )
    return '<nav aria-label="各篇章節">' + "".join(groups) + "</nav>"


def page(parts, title, description, content, root="./", current=None, toc=""):
    return render(
        "base.html", title=escape(title), description=escape(description, quote=True),
        content=content, root=root, chapter_nav=navigation(parts, root, current),
        layout="reading-layout" if current else "home-layout",
        page_toc=(
            '<aside class="page-toc"><p class="nav-label">本頁目錄</p>' + toc
            + '<a class="back-top" href="#main">回到頂端 ↑</a></aside>'
        ) if toc else "",
    )


def homepage(parts, chapters):
    written = [c for c in chapters if c.get("note")]
    groups = []
    for part in parts:
        rows = []
        for chapter in part["chapters"]:
            rows.append(
                f'<li><a class="chapter-row" href="{chapter_url(chapter, "./")}">'
                f'<span class="row-number">{chapter["number"]:02d}</span>'
                f'<span class="row-title">{escape(chapter["title"])}</span>{badge(chapter)}'
                '<span class="row-arrow" aria-hidden="true">→</span></a></li>'
            )
        first, last = part["chapters"][0]["number"], part["chapters"][-1]["number"]
        groups.append(
            f'<section class="part-section" id="part-{part["id"]}" aria-labelledby="part-title-{part["id"]}">'
            f'<div class="part-header"><span class="part-roman">{part["roman"]}</span>'
            f'<h3 id="part-title-{part["id"]}">{escape(part["title"])}</h3>'
            f'<span>第 {first}–{last} 章</span></div><ol>{"".join(rows)}</ol></section>'
        )
    content = render(
        "home.html", note_count=len(written), parts="".join(groups),
    )
    return page(parts, "我的 DDIA 筆記", "依 DDIA 第二版繁體中文講義整理的閱讀筆記、設計權衡與實驗紀錄。", content)


def placeholder(chapter):
    sections = "\n\n".join(
        f'### {section}\n\n待閱讀後，用自己的話整理這一節。' for section in chapter["sections"]
    )
    return (
        "## 學習目標\n\n待整理本章的學習目標。\n\n"
        f"## 閱讀筆記\n\n{sections}\n\n"
        "## 設計權衡\n\n待補充比較方向、適用情境與成本。\n\n"
        "## 實驗與案例\n\n尚未安排。理解觀念後，再選擇適合驗證的問題。\n\n"
        "## 尚未理解的問題\n\n把閱讀中的疑問留在這裡，之後回來修正。\n"
    )


def pagination(chapter, label, direction):
    if not chapter:
        return '<span class="pagination-spacer"></span>'
    return (
        f'<a class="pagination-link {direction}" href="{chapter["number"]:02d}.html">'
        f'<span>{label}</span><strong>{chapter["number"]:02d} {escape(chapter["title"])}</strong></a>'
    )


def chapter_page(parts, chapters, chapter, index):
    part = next(p for p in parts if chapter in p["chapters"])
    source = (SITE / "content" / chapter["note"]).read_text(encoding="utf-8") if chapter.get("note") else placeholder(chapter)
    converter = markdown.Markdown(
        extensions=["fenced_code", "tables", "admonition", "toc"],
        extension_configs={"toc": {"slugify": slugify, "toc_depth": "2-3"}},
    )
    body = converter.convert(source)
    body = body.replace('<table>', '<div class="table-scroll" tabindex="0" role="region" aria-label="比較表，可左右捲動"><table>').replace('</table>', '</table></div>')
    content = render(
        "chapter.html", number=chapter["number"], padded_number=f'{chapter["number"]:02d}',
        part_id=part["id"], part_name=escape(part["title"]), chapter_title=escape(chapter["title"]),
        status=chapter["status"], status_label=STATUS[chapter["status"]], summary=escape(chapter["summary"]),
        updated=f'<span>更新於 <time datetime="{chapter["updated"]}">{chapter["updated"]}</time></span>' if chapter.get("updated") else '<span>筆記尚未開始</span>',
        notice="" if chapter.get("note") else '<div class="empty-notice"><strong>這一章的筆記還沒開始。</strong><p>先保留講義的小節順序，閱讀後逐步補上理解、權衡與實驗。</p></div>',
        body=body, toc=converter.toc,
        previous=pagination(chapters[index - 1] if index else None, "← 上一章", "previous"),
        next=pagination(chapters[index + 1] if index + 1 < len(chapters) else None, "下一章 →", "next"),
    )
    return page(parts, f'第 {chapter["number"]} 章：{chapter["title"]}', chapter["summary"], content, "../", chapter["number"], converter.toc)


def main():
    parts = json.loads((SITE / "content" / "chapters.json").read_text(encoding="utf-8"))
    chapters = [chapter for part in parts for chapter in part["chapters"]]
    if [c["number"] for c in chapters] != list(range(1, 15)):
        raise ValueError("Chapter metadata must contain chapters 1–14 in order.")
    for chapter in chapters:
        if chapter["status"] not in STATUS:
            raise ValueError(f'Invalid status for chapter {chapter["number"]}.')
        if chapter["status"] != "pending" and not chapter.get("note"):
            raise ValueError("A started chapter must have a Markdown note.")
        if chapter.get("note"):
            note = (SITE / "content" / chapter["note"]).resolve()
            if note.parent != (SITE / "content").resolve() or note.suffix != ".md":
                raise ValueError("Notes must be Markdown files in site/content/.")
            date.fromisoformat(chapter["updated"])
            if not note.is_file():
                raise ValueError(f"Missing note: {note.name}")
    # Render everything before replacing output, so a failed conversion keeps the preview intact.
    pages = {"index.html": homepage(parts, chapters)}
    for index, chapter in enumerate(chapters):
        pages[f'chapters/{chapter["number"]:02d}.html'] = chapter_page(parts, chapters, chapter, index)
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "chapters").mkdir(exist_ok=True)
    for path, content in pages.items():
        (OUTPUT / path).write_text(content, encoding="utf-8")
    shutil.copytree(SITE / "assets", OUTPUT / "assets", dirs_exist_ok=True)
    print(f"Built {len(pages)} pages → {OUTPUT}")


if __name__ == "__main__":
    main()
