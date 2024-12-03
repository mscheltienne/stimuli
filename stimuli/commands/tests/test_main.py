from __future__ import annotations

from click.testing import CliRunner

from stimuli.commands.main import run


def test_main() -> None:
    """Test the main package entry-point."""
    runner = CliRunner()
    result = runner.invoke(run)
    assert result.exit_code == 0
    assert "Main package entry-point" in result.output
    assert "Options:" in result.output
    assert "Commands:" in result.output
