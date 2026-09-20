# Public OSS Tool Digest

A small, dependency-free Python CLI that reads public GitHub repository metadata and the latest published release for three named open-source tools, then writes a Markdown digest with direct citations.

## Included tools

- curl/curl
- jqlang/jq
- BurntSushi/ripgrep

## Usage

```bash
python oss_digest.py --output OSS_DIGEST.md
```

Choose repositories explicitly with repeated `--repository OWNER/NAME` options. The program uses only unauthenticated public GitHub API endpoints and does not read local credentials.

## Tests

```bash
python -m unittest -v test_oss_digest.py
```

## License

Original code in this repository is released under the MIT License. The digest links to, but does not reproduce, third-party project content.
