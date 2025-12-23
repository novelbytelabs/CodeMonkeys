"""Tests for dash refresh command."""
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from click.testing import CliRunner

from codemonkeys.commands.dash import dash, refresh


class TestDashRefresh:
    """Tests for dash refresh command."""

    def test_refresh_creates_science_index(self):
        """Refresh should create/update science_index.json."""
        runner = CliRunner()

        # Run refresh
        result = runner.invoke(dash, ['refresh'])

        # Should succeed
        assert result.exit_code == 0
        assert "Science index generated" in result.output or "✓" in result.output

        # File should exist
        assert Path("dash/science_index.json").exists()

    def test_refresh_science_index_valid_json(self):
        """Generated science_index.json should be valid JSON."""
        runner = CliRunner()
        runner.invoke(dash, ['refresh'])

        index_path = Path("dash/science_index.json")
        assert index_path.exists()

        # Should be valid JSON
        data = json.loads(index_path.read_text())
        assert "generated_at" in data
        assert "items" in data
        assert isinstance(data["items"], list)

    def test_refresh_uses_active_python(self):
        """Refresh should use sys.executable."""
        import sys

        with patch("codemonkeys.commands.dash.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="OK", stderr="")

            runner = CliRunner()
            runner.invoke(dash, ['refresh'])

            # Should have called with sys.executable
            call_args = mock_run.call_args[0][0]
            assert call_args[0] == sys.executable

    def test_refresh_fails_on_script_error(self):
        """Refresh should fail if script fails."""
        with patch("codemonkeys.commands.dash.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1,
                stdout="",
                stderr="Script error"
            )

            runner = CliRunner()
            result = runner.invoke(dash, ['refresh'])

            assert result.exit_code == 1


class TestDashServe:
    """Tests for dash serve command."""

    def test_serve_help(self):
        """Serve should have help."""
        runner = CliRunner()
        result = runner.invoke(dash, ['serve', '--help'])

        assert result.exit_code == 0
        assert "Serve the Dash interface" in result.output
        assert "--port" in result.output
