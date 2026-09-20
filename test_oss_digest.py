import unittest

from oss_digest import Repository, render_digest


class DigestRenderingTests(unittest.TestCase):
    def test_render_digest_contains_public_repo_and_release_citations(self):
        repository = Repository(
            slug="acme/widget",
            name="widget",
            description="A public command-line tool.",
            html_url="https://github.com/acme/widget",
            license_name="MIT",
            stars=12,
            forks=3,
            open_issues=1,
            updated_at="2026-09-20T12:00:00Z",
            latest_release_tag="v1.2.0",
            latest_release_url="https://github.com/acme/widget/releases/tag/v1.2.0",
        )

        digest = render_digest([repository])

        self.assertIn("# OSS Tool Digest", digest)
        self.assertIn("acme/widget", digest)
        self.assertIn("v1.2.0", digest)
        self.assertIn("[1](https://github.com/acme/widget)", digest)
        self.assertIn("[2](https://github.com/acme/widget/releases/tag/v1.2.0)", digest)

    def test_render_digest_rejects_empty_tool_list(self):
        with self.assertRaises(ValueError):
            render_digest([])


if __name__ == "__main__":
    unittest.main()
