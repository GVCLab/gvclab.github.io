#!/usr/bin/env python3
"""Fetch Google Scholar citations (via Semantic Scholar) and GitHub stars,
then update the front matter of _researches/*.md files."""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

RESEARCHES_DIR = os.path.join(os.path.dirname(__file__), "..", "_researches")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_front_matter(content):
    """Return (front_matter_str, body_str) split on the second '---'."""
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content
    return parts[1], parts[2]


def extract_field(front, key):
    """Extract a YAML scalar value from front matter text."""
    m = re.search(rf"^{key}:\s*(.+)$", front, re.MULTILINE)
    if m:
        return m.group(1).strip().strip("'\"")
    return ""


def set_field(content, key, value):
    """Replace an existing front-matter field value."""
    return re.sub(
        rf"^({key}:\s*).*$",
        rf"\g<1>{value}",
        content,
        count=1,
        flags=re.MULTILINE,
    )


# ---------------------------------------------------------------------------
# Semantic Scholar: citations
# ---------------------------------------------------------------------------

def fetch_citations(arxiv_map):
    """Batch-fetch citation counts from Semantic Scholar.
    arxiv_map: {filename: arxiv_id}
    Returns: {filename: citation_count}
    """
    results = {}
    fnames = list(arxiv_map.keys())
    arxiv_ids = list(arxiv_map.values())

    batch_size = 50
    for i in range(0, len(arxiv_ids), batch_size):
        batch = arxiv_ids[i : i + batch_size]
        batch_fnames = fnames[i : i + batch_size]
        payload = json.dumps({"ids": [f"ArXiv:{aid}" for aid in batch]}).encode()

        req = urllib.request.Request(
            "https://api.semanticscholar.org/graph/v1/paper/batch?fields=citationCount",
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "gvclab-metrics"},
            method="POST",
        )
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            data = json.loads(resp.read())
            for j, item in enumerate(data):
                fname = batch_fnames[j]
                if item and "citationCount" in item:
                    results[fname] = item["citationCount"]
                else:
                    results[fname] = 0
        except Exception as e:
            print(f"  [citations] batch error: {e}", file=sys.stderr)
            for fname in batch_fnames:
                results.setdefault(fname, 0)
        time.sleep(1)  # rate-limit courtesy

    return results


# ---------------------------------------------------------------------------
# GitHub API: stars
# ---------------------------------------------------------------------------

def fetch_stars(repo_map):
    """Fetch star counts from GitHub API.
    repo_map: {filename: 'owner/repo'}
    Returns: {filename: star_count}
    """
    # Deduplicate repos
    unique = {}
    for fname, repo in repo_map.items():
        unique.setdefault(repo, []).append(fname)

    star_cache = {}
    results = {}

    for repo, fnames in unique.items():
        if repo in star_cache:
            stars = star_cache[repo]
        else:
            stars = 0
            try:
                headers = {"User-Agent": "gvclab-metrics", "Accept": "application/vnd.github.v3+json"}
                if GITHUB_TOKEN:
                    headers["Authorization"] = f"token {GITHUB_TOKEN}"
                req = urllib.request.Request(
                    f"https://api.github.com/repos/{repo}",
                    headers=headers,
                )
                resp = urllib.request.urlopen(req, timeout=15)
                data = json.loads(resp.read())
                stars = data.get("stargazers_count", 0)
            except Exception as e:
                print(f"  [stars] {repo}: {e}", file=sys.stderr)
            star_cache[repo] = stars
            time.sleep(0.3)

        for fname in fnames:
            results[fname] = stars

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    researches_dir = os.path.normpath(RESEARCHES_DIR)
    if not os.path.isdir(researches_dir):
        print(f"Directory not found: {researches_dir}", file=sys.stderr)
        sys.exit(1)

    # Collect arxiv IDs and GitHub repos
    arxiv_map = {}
    repo_map = {}
    files_content = {}

    for fname in sorted(os.listdir(researches_dir)):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(researches_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        files_content[fname] = content

        front, _ = parse_front_matter(content)
        if front is None:
            continue

        arxiv_id = extract_field(front, "arxiv")
        if arxiv_id:
            arxiv_map[fname] = arxiv_id

        code_url = extract_field(front, "code")
        if "github.com/" in code_url:
            repo = code_url.replace("https://github.com/", "")
            repo_map[fname] = repo

    print(f"Found {len(arxiv_map)} papers with arxiv IDs, {len(repo_map)} with GitHub repos")

    # Fetch data
    citations = fetch_citations(arxiv_map)
    stars = fetch_stars(repo_map)

    # Update files
    updated = 0
    for fname, content in files_content.items():
        new_content = content
        c = citations.get(fname, 0)
        s = stars.get(fname, 0)

        if c > 0:
            new_content = set_field(new_content, "scholar_citations", str(c))
        if s > 0:
            new_content = set_field(new_content, "github_stars", str(s))

        if new_content != content:
            fpath = os.path.join(researches_dir, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            updated += 1
            print(f"  Updated: {fname} (citations={c}, stars={s})")

    print(f"Done. Updated {updated} files.")


if __name__ == "__main__":
    main()
