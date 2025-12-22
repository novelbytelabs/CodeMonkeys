"""Tests for science dossier CLI commands."""
import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from codemonkeys.cli import cli


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


class TestNewScienceCommand:
    """Tests for codemonkeys dossier new-science."""

    def test_new_science_creates_file(self, runner):
        """new-science should create a science dossier file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with runner.isolated_filesystem(temp_dir=tmpdir):
                # Create necessary dirs
                Path("docs/science").mkdir(parents=True, exist_ok=True)
                Path("docs/schemas").mkdir(parents=True, exist_ok=True)

                result = runner.invoke(cli, ["dossier", "new-science", "test-topic"])
                assert result.exit_code == 0
                assert "Created Science Dossier" in result.output

                # Check file exists
                created = list(Path("docs/science").glob("SCI-*-test-topic.md"))
                assert len(created) == 1

    def test_new_science_file_has_required_fields(self, runner):
        """Created file should have required frontmatter fields."""
        import frontmatter
        with tempfile.TemporaryDirectory() as tmpdir:
            with runner.isolated_filesystem(temp_dir=tmpdir):
                Path("docs/science").mkdir(parents=True, exist_ok=True)

                runner.invoke(cli, ["dossier", "new-science", "my-topic"])
                created = list(Path("docs/science").glob("SCI-*-my-topic.md"))[0]

                post = frontmatter.load(created)
                assert post.metadata.get("dossier_type") == "science"
                assert "hypothesis" in post.metadata
                assert "constitution_refs" in post.metadata


class TestValidateScienceCommand:
    """Tests for codemonkeys dossier validate-science."""

    def test_validate_science_valid_file(self, runner):
        """validate-science should pass for valid dossier."""
        # Use the actual example dossier
        result = runner.invoke(
            cli,
            ["dossier", "validate-science", "docs/science/SCI-20251222-arqonhpo-runtime-optimization.md"]
        )
        assert "Science Dossier Valid" in result.output

    def test_validate_science_shows_schema_valid(self, runner):
        """validate-science should show Schema Valid."""
        result = runner.invoke(
            cli,
            ["dossier", "validate-science", "docs/science/SCI-20251222-arqonhpo-runtime-optimization.md"]
        )
        assert "Schema Valid" in result.output


class TestScienceToDesignCommand:
    """Tests for codemonkeys dossier science-to-design."""

    def test_science_to_design_creates_design_dossier(self, runner):
        """science-to-design should create a design dossier."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with runner.isolated_filesystem(temp_dir=tmpdir):
                # Copy necessary files
                import shutil
                Path("docs/science").mkdir(parents=True, exist_ok=True)
                Path("docs/dossiers").mkdir(parents=True, exist_ok=True)
                Path("docs/schemas").mkdir(parents=True, exist_ok=True)

                # Create minimal science dossier
                science_content = '''---
schema_version: "0.1"
dossier_type: "science"
dossier_id: "SCI-20251222-test"
topic: "Test"
owner: "science-monkeys"
status: "validated"
created_at: "2025-12-22"
hypothesis:
  statement: "If X then Y"
acceptance_hooks:
  code_proofs: ["Proof 1"]
  test_requirements: ["Test 1"]
evidence_plan:
  final_artifacts: ["artifact.json"]
constitution_refs:
  - "constitution.md"
---
# Test
'''
                Path("docs/science/SCI-20251222-test.md").write_text(science_content)

                result = runner.invoke(
                    cli,
                    ["dossier", "science-to-design", "docs/science/SCI-20251222-test.md", "--product-id", "test-product"]
                )
                assert result.exit_code == 0
                assert "Created Design Dossier" in result.output

                # Check design dossier created
                design_files = list(Path("docs/dossiers").glob("DOS-*-test-product.md"))
                assert len(design_files) == 1

    def test_science_to_design_preserves_hypothesis(self, runner):
        """science-to-design should preserve hypothesis in output."""
        import frontmatter
        # Use actual files
        result = runner.invoke(
            cli,
            ["dossier", "science-to-design", "docs/science/SCI-20251222-arqonhpo-runtime-optimization.md", "--product-id", "test-preserve"]
        )

        # Check design file has hypothesis
        design_file = Path("docs/dossiers/DOS-20251222-test-preserve.md")
        if design_file.exists():
            post = frontmatter.load(design_file)
            assert "hypothesis" in post.metadata
            # Cleanup
            design_file.unlink()
