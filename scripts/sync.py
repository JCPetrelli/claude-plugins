#!/usr/bin/env python3
"""Keep the marketplace in step with the tool repos.

For each plugin in plugins.json it asks GitHub for the latest release. With a release, the marketplace entry
pins that tag (`ref`) and its version; without one, it follows the default branch and takes the version from
the repo's .claude-plugin/plugin.json. Then it rewrites .claude-plugin/marketplace.json and the version table
in README.md (between the <!-- plugins:start --> / <!-- plugins:end --> markers).

    python3 scripts/sync.py            # rewrite the files
    python3 scripts/sync.py --check    # exit 1 if the files are out of date (CI)

Needs only the standard library. Set GITHUB_TOKEN to avoid the unauthenticated rate limit.
"""
from __future__ import annotations

import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "plugins.json"
MARKETPLACE = ROOT / ".claude-plugin/marketplace.json"
README = ROOT / "README.md"


def gh(path: str):
    req = urllib.request.Request(f"https://api.github.com/{path}", headers={"Accept": "application/vnd.github+json",
                                                                          "User-Agent": "claude-plugins-sync"})
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def plugin_json(repo: str, ref: str | None) -> dict:
    q = f"?ref={ref}" if ref else ""
    f = gh(f"repos/{repo}/contents/.claude-plugin/plugin.json{q}")
    if not f:
        raise SystemExit(f"{repo}: no .claude-plugin/plugin.json at {ref or 'the default branch'}")
    return json.loads(base64.b64decode(f["content"]))


def resolve(p: dict) -> dict:
    """Latest release tag (if any) and the plugin.json at that point."""
    rel = gh(f"repos/{p['repo']}/releases/latest")
    tag = rel["tag_name"] if rel and not rel.get("draft") and not rel.get("prerelease") else None
    meta = plugin_json(p["repo"], tag)
    sha = gh(f"repos/{p['repo']}/commits/{tag}")["sha"] if tag else None
    return {**p, "tag": tag, "sha": sha, "version": meta.get("version", tag.lstrip("v") if tag else ""),
            "description": p.get("description") or meta.get("description", ""), "keywords": meta.get("keywords", [])}


def marketplace(cfg: dict, plugins: list[dict]) -> dict:
    entries = []
    for p in plugins:
        source = {"source": "github", "repo": p["repo"]}
        if p["tag"]:  # pin the release: tag for people, commit for the installer
            source.update(ref=p["tag"], sha=p["sha"])
        # no "version" here: the plugin's own plugin.json version wins at install time (and validate warns on both)
        entry = {"name": p["name"], "source": source, "description": p["description"]}
        entry.update({"author": cfg["owner"], "homepage": f"https://github.com/{p['repo']}", "license": "MIT",
                      "keywords": p["keywords"], "category": p.get("category", "productivity")})
        entries.append(entry)
    return {"name": cfg["name"], "description": cfg["description"], "owner": cfg["owner"], "plugins": entries}


def table(cfg: dict, plugins: list[dict]) -> str:
    rows = ["| Plugin | What it does | Version | Install |", "|---|---|---|---|"]
    for p in plugins:
        ver = f"[{p['version']}](https://github.com/{p['repo']}/releases/tag/{p['tag']})" if p["tag"] else f"{p['version']} (main)"
        rows.append(f"| [{p['title']}](https://github.com/{p['repo']}) | {p['summary']} | {ver} | `/plugin install {p['name']}@{cfg['name']}` |")
    return "\n".join(rows)


def main() -> int:
    check = "--check" in sys.argv
    cfg = json.loads(CONFIG.read_text())
    plugins = [resolve(p) for p in cfg["plugins"]]
    want_mp = json.dumps(marketplace(cfg, plugins), indent=2, ensure_ascii=False) + "\n"
    readme = README.read_text()
    want_readme = re.sub(r"<!-- plugins:start -->.*?<!-- plugins:end -->",
                         lambda m: "<!-- plugins:start -->\n" + table(cfg, plugins) + "\n<!-- plugins:end -->", readme, flags=re.S)
    have_mp = MARKETPLACE.read_text() if MARKETPLACE.exists() else ""
    stale = [f for f, a, b in ((MARKETPLACE, have_mp, want_mp), (README, readme, want_readme)) if a != b]
    for p in plugins:
        print(f"{p['name']:<10} {p['version'] or '?':<8} {p['tag'] or 'default branch'}")
    if check:
        if stale:
            print("out of date:", ", ".join(str(f.relative_to(ROOT)) for f in stale))
            return 1
        return 0
    MARKETPLACE.write_text(want_mp)
    README.write_text(want_readme)
    print("updated:", ", ".join(str(f.relative_to(ROOT)) for f in stale) or "nothing")
    return 0


if __name__ == "__main__":
    sys.exit(main())
