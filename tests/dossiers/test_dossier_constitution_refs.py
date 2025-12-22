
import pytest
import frontmatter
from pathlib import Path

# Use the test dossier created during verify
TEST_DOSSIER = list(Path("docs/dossiers").glob("DOS-*-test-product.md"))[0]

def test_dossier_has_constitution_refs():
    post = frontmatter.load(TEST_DOSSIER)
    refs = post.metadata.get("constitution_refs", [])
    assert refs, "Dossier missing constitution_refs"
    assert "constitution.md" in refs, "Dossier must ref constitution.md"

def test_silverback_logic_replicates_in_test():
    # This mimics the Silverback check
    post = frontmatter.load(TEST_DOSSIER)
    refs = post.metadata.get("constitution_refs", [])
    for ref in refs:
        assert Path(ref).exists(), f"Referenced doc {ref} missing"
