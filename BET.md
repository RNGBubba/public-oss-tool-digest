# Bet: Public OSS Tool Digest

## Offer

A dependency-free CLI that produces a compact, cited Markdown snapshot for three named open-source tools. It is useful as a repeatable starting point for engineering teams, maintainers, and technical writers who need public project metadata without copying project content.

## Price and 30-day path

Suggested one-time price: $9.00 for the original CLI/template. The 30-day path is public GitHub discovery: keep the repository README clear, publish small improvements from observed public API changes, and invite users to open issues for additional public repositories. No paid promotion or private data is required.

## Human click

A buyer would need to discover the public repository and choose to use or adapt it. No checkout rail is configured or used here; this is a public artifact, not a claim of revenue.

## Artifact and verification

- Repository: https://github.com/RNGBubba/public-oss-tool-digest
- Artifact: `OSS_DIGEST.md` generated from the public GitHub API by `oss_digest.py`.
- Test command: `python -m unittest -v test_oss_digest.py`
- Generation command: `python oss_digest.py --output OSS_DIGEST.md`

## Public sources

The generated digest cites the repository and release pages for each tool:

1. curl/curl repository: https://github.com/curl/curl
2. curl/curl release page: https://github.com/curl/curl/releases/tag/curl-8_22_0
3. jqlang/jq repository: https://github.com/jqlang/jq
4. jqlang/jq release page: https://github.com/jqlang/jq/releases/tag/jq-1.8.2
5. BurntSushi/ripgrep repository: https://github.com/BurntSushi/ripgrep
6. BurntSushi/ripgrep release page: https://github.com/BurntSushi/ripgrep/releases/tag/15.2.0

GitHub API documentation used to confirm the public metadata/release endpoints:

- https://docs.github.com/en/rest/repos/repos
- https://docs.github.com/en/rest/releases/releases
- https://cli.github.com/manual/gh_api

All research used public pages only. The code does not bundle third-party source, credentials, or private data.
