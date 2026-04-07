#!/usr/bin/env python3
"""Local Reader Server — serves paper-notes + local collections"""
import os, json, re, mimetypes
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
PORT = 8080

# Collection config: name -> {path, type, icon, color}
COLLECTIONS = {
    "papers": {
        "path": ROOT / "posts",
        "type": "papers",  # special: uses index.json
        "icon": "sparkles",
        "color": "#c45d3e",
        "label": "Paper Notes",
    },
    "video-notes": {
        "path": Path.home() / "Documents" / "video-notes",
        "type": "markdown",
        "icon": "video",
        "color": "#8b5cf6",
        "label": "Video Notes",
    },
    "buffett-articles": {
        "path": Path.home() / "Documents" / "buffett" / "articles",
        "type": "markdown",
        "icon": "landmark",
        "color": "#0ea5e9",
        "label": "Buffett Articles",
    },
    "buffett-cn": {
        "path": Path.home() / "Documents" / "buffett" / "articles-cn",
        "type": "markdown",
        "icon": "book-open-text",
        "color": "#dc2626",
        "label": "Buffett 解读",
    },
    "buffett-letters-cn": {
        "path": Path.home() / "Documents" / "buffett" / "letters-cn",
        "type": "markdown",
        "icon": "languages",
        "color": "#e11d48",
        "label": "Buffett 中文全文",
    },
    "buffett-meetings": {
        "path": Path.home() / "Documents" / "buffett" / "annual-meetings-cn",
        "type": "markdown",
        "icon": "users",
        "color": "#8b5cf6",
        "label": "Buffett 股东大会",
    },
    "buffett-letters": {
        "path": Path.home() / "Documents" / "buffett" / "shareholder-letters" / "markdown",
        "type": "markdown",
        "icon": "mail",
        "color": "#10b981",
        "label": "Buffett Letters EN",
    },
}


def scan_markdown_dir(dirpath):
    """Scan a directory of .md files into a paper-like index."""
    items = []
    if not dirpath.is_dir():
        return items
    for f in sorted(dirpath.glob("*.md"), reverse=True):
        content = f.read_text(errors="ignore")
        # Try to extract title from first # heading
        title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else f.stem

        # Try to extract date from filename or frontmatter
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', f.stem)
        if date_match:
            date = date_match.group(1)
            # Remove date prefix from title if title starts with it
            title = re.sub(r'^\d{4}-\d{2}-\d{2}[-_]?', '', title).strip() or f.stem
        else:
            # Try frontmatter
            fm_match = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
            date = fm_match.group(1) if fm_match else datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d')

        # Clean up title from filename if no heading found
        if not title_match:
            title = f.stem
            if date_match:
                title = title[len(date_match.group(0)):].lstrip('-_ ')
            title = title.replace('-', ' ').replace('_', ' ')

        items.append({
            "date": date,
            "title": title,
            "file": str(f.name),
            "size": f.stat().st_size,
        })
    return items


def scan_html_dir(dirpath):
    """Scan a directory of .html files."""
    items = []
    if not dirpath.is_dir():
        return items
    for f in sorted(dirpath.glob("*.html"), reverse=True):
        year = f.stem
        items.append({
            "date": f"{year}-01-01" if year.isdigit() else "",
            "title": f"Shareholder Letter {year}" if year.isdigit() else f.stem,
            "file": f.name,
            "size": f.stat().st_size,
        })
    return items


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        p = parsed.path

        # Serve index.html
        if p == "/" or p == "/index.html":
            return self._file(ROOT / "index.html", "text/html")

        # API: list collections
        if p == "/api/collections":
            result = []
            for key, cfg in COLLECTIONS.items():
                if cfg["type"] == "papers":
                    idx_file = cfg["path"] / "index.json"
                    count = len(json.loads(idx_file.read_text())) if idx_file.exists() else 0
                elif cfg["type"] == "markdown":
                    count = len(list(cfg["path"].glob("*.md"))) if cfg["path"].is_dir() else 0
                elif cfg["type"] == "html-files":
                    count = len(list(cfg["path"].glob("*.html"))) if cfg["path"].is_dir() else 0
                else:
                    count = 0
                result.append({
                    "key": key,
                    "label": cfg["label"],
                    "icon": cfg["icon"],
                    "color": cfg["color"],
                    "count": count,
                    "type": cfg["type"],
                })
            return self._json(result)

        # API: list items in a collection
        if p.startswith("/api/items/"):
            key = p[11:].strip("/")
            cfg = COLLECTIONS.get(key)
            if not cfg:
                return self._json({"error": "not found"}, 404)

            if cfg["type"] == "papers":
                idx_file = cfg["path"] / "index.json"
                if idx_file.exists():
                    items = json.loads(idx_file.read_text())
                    return self._json(items)
                return self._json([])

            elif cfg["type"] == "markdown":
                return self._json(scan_markdown_dir(cfg["path"]))

            elif cfg["type"] == "html-files":
                return self._json(scan_html_dir(cfg["path"]))

            return self._json([])

        # API: get a file from a collection
        if p.startswith("/api/file/"):
            rest = unquote(p[10:])
            parts = rest.split("/", 1)
            if len(parts) < 2:
                return self._json({"error": "need collection/filename"}, 400)
            key, fname = parts
            cfg = COLLECTIONS.get(key)
            if not cfg:
                return self._json({"error": "collection not found"}, 404)
            fpath = cfg["path"] / fname
            if not fpath.exists() or not fpath.is_file():
                return self._json({"error": "file not found"}, 404)
            mime = mimetypes.guess_type(str(fpath))[0] or "text/plain"
            return self._file(fpath, mime)

        # Static files (JS, CSS, etc.)
        fpath = ROOT / p.lstrip("/")
        if fpath.exists() and fpath.is_file():
            mime = mimetypes.guess_type(str(fpath))[0] or "application/octet-stream"
            return self._file(fpath, mime)

        # Also serve posts/ directory for backward compat
        if p.startswith("/posts/"):
            fpath = ROOT / p.lstrip("/")
            if fpath.exists():
                mime = mimetypes.guess_type(str(fpath))[0] or "text/plain"
                return self._file(fpath, mime)

        return self._json({"error": "not found"}, 404)

    def do_POST(self):
        p = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        body_raw = self.rfile.read(length) if length else b""

        if p == "/api/translate":
            body = json.loads(body_raw)
            text = body.get("text", "")
            try:
                import anthropic
                client = anthropic.Anthropic()
                msg = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": f"Translate the following English text to Chinese. Return ONLY the Chinese translation, nothing else.\n\n{text}"}]
                )
                translation = msg.content[0].text
                return self._json({"translation": translation})
            except Exception as e:
                return self._json({"error": str(e)}, 500)

        return self._json({"error": "not found"}, 404)

    def _json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def _file(self, path, mime):
        self.send_response(200)
        self.send_header("Content-Type", f"{mime}; charset=utf-8")
        self.end_headers()
        self.wfile.write(path.read_bytes())

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    import socketserver
    socketserver.TCPServer.allow_reuse_address = True
    s = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"\n  Local Reader: http://localhost:{PORT}\n")
    print(f"  Collections:")
    for k, v in COLLECTIONS.items():
        print(f"    {v['label']:20s} {v['path']}")
    print()
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        s.server_close()
