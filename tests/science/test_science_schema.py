"""Tests for science dossier schema validation."""
import json
from pathlib import Path

import pytest
from jsonschema import validate, ValidationError


@pytest.fixture
def schema():
    """Load the science dossier schema."""
    schema_path = Path("docs/schemas/science_dossier.schema.json")
    return json.loads(schema_path.read_text())


@pytest.fixture
def valid_science_dossier():
    """A minimal valid science dossier metadata."""
    return {
        "schema_version": "0.1",
        "dossier_type": "science",
        "dossier_id": "SCI-20251222-test-topic",
        "topic": "Test Topic",
        "owner": "science-monkeys",
        "status": "draft",
        "created_at": "2025-12-22",
        "hypothesis": {
            "statement": "If X then Y"
        },
        "acceptance_hooks": {
            "code_proofs": ["Proof 1"],
            "test_requirements": ["Test 1"]
        },
        "evidence_plan": {
            "final_artifacts": ["artifact.json"]
        },
        "constitution_refs": ["constitution.md"]
    }


class TestScienceDossierSchema:
    """Tests for science dossier schema."""

    def test_schema_file_exists(self):
        """Schema file should exist."""
        schema_path = Path("docs/schemas/science_dossier.schema.json")
        assert schema_path.exists()

    def test_schema_is_valid_json(self, schema):
        """Schema should be valid JSON."""
        assert "$schema" in schema
        assert schema["$id"] == "science_dossier.schema.json"

    def test_valid_dossier_passes(self, schema, valid_science_dossier):
        """Valid science dossier should pass validation."""
        validate(instance=valid_science_dossier, schema=schema)

    def test_missing_hypothesis_fails(self, schema, valid_science_dossier):
        """Missing hypothesis should fail validation."""
        del valid_science_dossier["hypothesis"]
        with pytest.raises(ValidationError):
            validate(instance=valid_science_dossier, schema=schema)

    def test_missing_dossier_type_fails(self, schema, valid_science_dossier):
        """Missing dossier_type should fail validation."""
        del valid_science_dossier["dossier_type"]
        with pytest.raises(ValidationError):
            validate(instance=valid_science_dossier, schema=schema)

    def test_wrong_dossier_type_fails(self, schema, valid_science_dossier):
        """Wrong dossier_type should fail validation."""
        valid_science_dossier["dossier_type"] = "design"
        with pytest.raises(ValidationError):
            validate(instance=valid_science_dossier, schema=schema)

    def test_invalid_dossier_id_pattern_fails(self, schema, valid_science_dossier):
        """Invalid dossier_id pattern should fail."""
        valid_science_dossier["dossier_id"] = "DOS-20251222-test"  # Wrong prefix
        with pytest.raises(ValidationError):
            validate(instance=valid_science_dossier, schema=schema)

    def test_empty_constitution_refs_fails(self, schema, valid_science_dossier):
        """Empty constitution_refs should fail."""
        valid_science_dossier["constitution_refs"] = []
        with pytest.raises(ValidationError):
            validate(instance=valid_science_dossier, schema=schema)


class TestExampleScienceDossier:
    """Tests for the ArqonHPO example dossier."""

    def test_example_exists(self):
        """Example dossier should exist."""
        path = Path("docs/science/SCI-20251222-arqonhpo-runtime-optimization.md")
        assert path.exists()

    def test_example_validates(self, schema):
        """Example dossier should validate against schema."""
        import frontmatter
        path = Path("docs/science/SCI-20251222-arqonhpo-runtime-optimization.md")
        post = frontmatter.load(path)
        validate(instance=post.metadata, schema=schema)

    def test_example_has_hypothesis(self):
        """Example should have a hypothesis statement."""
        import frontmatter
        path = Path("docs/science/SCI-20251222-arqonhpo-runtime-optimization.md")
        post = frontmatter.load(path)
        assert "hypothesis" in post.metadata
        assert "statement" in post.metadata["hypothesis"]

    def test_example_has_acceptance_hooks(self):
        """Example should have acceptance hooks."""
        import frontmatter
        path = Path("docs/science/SCI-20251222-arqonhpo-runtime-optimization.md")
        post = frontmatter.load(path)
        assert "acceptance_hooks" in post.metadata
        assert "code_proofs" in post.metadata["acceptance_hooks"]
