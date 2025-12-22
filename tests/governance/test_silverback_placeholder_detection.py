"""Tests for Silverback placeholder detection logic."""
import sys
from pathlib import Path

# Add scripts to path for direct import
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from silverback_validate import _is_placeholder_only


class TestPlaceholderDetection:
    """Tests for the _is_placeholder_only helper."""

    def test_flags_tbd(self):
        assert _is_placeholder_only("TBD") is True
        assert _is_placeholder_only("tbd") is True
        assert _is_placeholder_only("TODO") is True

    def test_flags_none_placeholder(self):
        assert _is_placeholder_only("None") is True
        assert _is_placeholder_only("N/A") is True
        assert _is_placeholder_only("...") is True

    def test_flags_empty(self):
        assert _is_placeholder_only("") is True
        assert _is_placeholder_only("   ") is True

    def test_flags_action_required_brackets(self):
        assert _is_placeholder_only("[ACTION REQUIRED]") is True
        assert _is_placeholder_only("[TODO: fill this in]") is True

    def test_accepts_constraints_markers(self):
        text = """
### Constraints
- **C-001**: Must remain deterministic.
- **C-002**: No network calls.

### Non-goals
- **NG-001**: Not a full rewrite.
"""
        assert _is_placeholder_only(text) is False

    def test_accepts_acceptance_criteria_markers(self):
        text = """
- **AC-001**: Ship fails if git is dirty.
- **AC-002**: Ship fails if Silverback fails.
"""
        assert _is_placeholder_only(text) is False

    def test_accepts_real_prose(self):
        text = "This component must validate all inputs before processing."
        assert _is_placeholder_only(text) is False
