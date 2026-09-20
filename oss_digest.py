"""Build a cited digest from public GitHub repository and release pages."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_REPOSITORIES = (
    "curl/curl",
    "jqlang/jq",
    "BurntSushi/ripgrep",
)


@dataclass(frozen=True)
class Repository:
    slug: str
    name: str
    description: str
    html_url: str
    license_name: str
    stars: int
    forks: int
    open_issues: int
    updated_at: str
    latest_release_tag: str | None
    latest_release_url: str | None


def _get_json(url: str, timeout: int = 20) -> Any:
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "oss-public-digest/1.0",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.load(response)
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"public GitHub request failed for {url}: {exc}") from exc


def fetch_repository(slug: str) -> Repository:
    if slug.count("/") != 1 or any(not part for part in slug.split("/")):
        raise ValueError(f"repository must be OWNER/NAME: {slug!r}")
    repository = _get_json(f"https://api.github.com/repos/{slug}")
    releases = _get_json(
        f"https://api.github.com/repos/{slug}/releases?per_page=1"
    )
    release = releases[0] if releases else {}
    license_data = repository.get("license") or {}
    return Repository(
        slug=slug,
        name=repository.get("name", slug.rsplit("/", 1)[-1]),
        description=repository.get("description") or "No description provided.",
        html_url=repository["html_url"],
        license_name=license_data.get("spdx_id") or "Not declared",
        stars=int(repository.get("stargazers_count", 0)),
        forks=int(repository.get("forks_count", 0)),
        open_issues=int(repository.get("open_issues_count", 0)),
        updated_at=repository.get("updated_at", "Unknown"),
        latest_release_tag=release.get("tag_name"),
        latest_release_url=release.get("html_url"),
    )


def _date(value: str) -> str:
    if value == "Unknown":
        return value
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return value


def render_digest(repositories: list[Repository]) -> str:
    if not repositories:
        raise ValueError("at least one repository is required")
    lines = [
        "# OSS Tool Digest",
        "",
        f"Snapshot date: {datetime.now(timezone.utc).date().isoformat()} (UTC)",
        "",
        "This digest uses public GitHub repository and release metadata. Counts and release state can change after publication.",
        "",
    ]
    for index, repository in enumerate(repositories, start=1):
        release_index = index + len(repositories)
        release = repository.latest_release_tag or "No published release returned"
        lines.extend(
            [
                f"## {repository.slug}",
                "",
                f"{repository.description}",
                "",
                f"- License: {repository.license_name}",
                f"- Stars: {repository.stars:,}; forks: {repository.forks:,}; open issues: {repository.open_issues:,}",
                f"- Repository metadata last updated: {_date(repository.updated_at)}",
                f"- Latest published release: {release}",
                f"- Repository: [{index}]({repository.html_url})",
            ]
        )
        if repository.latest_release_url:
            lines.append(f"- Release page: [{release_index}]({repository.latest_release_url})")
        lines.append("")
    lines.extend(
        [
            "## Sources",
            "",
            *[f"[{index}]({repository.html_url})" for index, repository in enumerate(repositories, start=1)],
            *[
                f"[{index + len(repositories)}]({repository.latest_release_url})"
                for index, repository in enumerate(repositories, start=1)
                if repository.latest_release_url
            ],
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", action="append", dest="repositories")
    parser.add_argument("--output", default="OSS_DIGEST.md")
    args = parser.parse_args()
    slugs = args.repositories or list(DEFAULT_REPOSITORIES)
    repositories = [fetch_repository(slug) for slug in slugs]
    with open(args.output, "w", encoding="utf-8") as output:
        output.write(render_digest(repositories))
    print(f"wrote {args.output} ({len(repositories)} repositories)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
