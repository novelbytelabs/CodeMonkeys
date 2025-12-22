#!/usr/bin/env python3
"""
Preflight Check - Release Gate
Enforces Article I: "The Factory is the sole mechanism for software production."

Checks:
1. Git status is clean (no uncommitted changes).
2. Silverback validation passes (--all).
3. Recent run artifacts exist for the product being shipped (optional/future).
"""
import sys
import subprocess
from pathlib import Path
from rich.console import Console

console = Console()

def check_git_clean():
    """Ensure git working directory is clean."""
    console.print("[bold blue]1. Checking Git Status...[/bold blue]")
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if result.stdout.strip():
        console.print("[bold red]❌ Git working directory is dirty.[/bold red]")
        console.print(result.stdout)
        return False
    console.print("[green]✅ Git clean.[/green]")
    return True

def run_silverback():
    """Run Silverback validation."""
    console.print("[bold blue]2. Running Silverback Validation...[/bold blue]")
    # We call the codemonkeys command to ensure consistency
    result = subprocess.run(["codemonkeys", "silverback", "--all"], capture_output=True, text=True)
    if result.returncode != 0:
        console.print("[bold red]❌ Silverback Validation Failed.[/bold red]")
        console.print(result.stdout)
        console.print(result.stderr)
        return False
    console.print("[green]✅ Silverback passed.[/green]")
    return True

def main():
    console.print("\n[bold yellow]=== 🛫 Factory Preflight Check ===[/bold yellow]\n")
    
    if not check_git_clean():
        sys.exit(1)
        
    if not run_silverback():
        sys.exit(1)
        
    console.print("\n[bold green]🚀 Preflight passed. Cleared for takeoff.[/bold green]\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
