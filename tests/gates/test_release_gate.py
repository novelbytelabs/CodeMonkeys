
import pytest
import subprocess
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from codemonkeys.commands.ship import ship

@pytest.fixture
def runner():
    return CliRunner()

def test_ship_preflight_fail_git_dirty(runner):
    """Test that ship aborts if git is dirty."""
    with patch('subprocess.run') as mock_run:
        # Mock preflight script return code 1
        mock_run.return_value.returncode = 1
        
        result = runner.invoke(ship, ['v1.0.0'])
        assert result.exit_code == 1
        assert "Release Gate Closed" in result.output

def test_ship_preflight_pass(runner):
    """Test that ship proceeds if preflight passes."""
    with patch('subprocess.run') as mock_run:
        # 1. Preflight script returns 0
        # 2. Git tag check returns empty (no exist)
        # 3. Git tag command returns 0
        
        def side_effect(args, **kwargs):
            cmd = args[0] if isinstance(args, list) else args
            if "scripts/preflight_check.py" in str(args):
                return MagicMock(returncode=0)
            if "git" in args and "tag" in args and "-l" in args:
                return MagicMock(stdout="")
            if "git" in args and "tag" in args and "-a" in args:
                return MagicMock(returncode=0)
            return MagicMock(returncode=0)

        mock_run.side_effect = side_effect
        
        # Use dry-run to avoid actual git ops if mock fails
        result = runner.invoke(ship, ['v1.0.0', '--dry-run'])
        assert result.exit_code == 0
        assert "Dry run passed" in result.output

def test_ship_tag_exists(runner):
    """Test that ship aborts if tag exists."""
    with patch('subprocess.run') as mock_run:
        # Mock preflight pass
        # Mock git tag -l returns "v1.0.0"
        
        def side_effect(args, **kwargs):
            if "scripts/preflight_check.py" in str(args):
                 return MagicMock(returncode=0)
            if "git" in args and "tag" in args and "-l" in args:
                return MagicMock(stdout="v1.0.0")
            return MagicMock(returncode=0)

        mock_run.side_effect = side_effect

        result = runner.invoke(ship, ['v1.0.0'])
        assert result.exit_code == 1
        assert "already exists" in result.output
