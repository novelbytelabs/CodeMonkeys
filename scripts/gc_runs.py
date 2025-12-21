#!/usr/bin/env python3
"""
Garbage Collector for Run Artifacts.

Removes old run directories, keeping only the most recent N runs per product.

Usage:
    python scripts/gc_runs.py --keep 10
    python scripts/gc_runs.py --keep 5 --product codemonkeys-dash
    python scripts/gc_runs.py --keep 3 --dry-run

Example:
    # Keep last 10 runs for all products
    python scripts/gc_runs.py --keep 10
"""
import argparse
import os
import shutil
from pathlib import Path


RUNS_DIR = Path("dash/runs")


def get_run_dirs(product_dir: Path) -> list[Path]:
    """
    Get all run directories for a product, sorted by name (newest first).
    
    Run IDs are formatted as run_YYYYMMDD_HHMMSS, so lexicographic sort works.
    """
    runs = []
    for item in product_dir.iterdir():
        if item.is_dir() and item.name.startswith("run_"):
            runs.append(item)
    
    # Sort by name descending (newest first)
    runs.sort(key=lambda p: p.name, reverse=True)
    return runs


def gc_product(product_dir: Path, keep: int, dry_run: bool = False) -> int:
    """
    Remove old runs for a product, keeping the most recent N.
    
    Returns:
        Number of directories removed.
    """
    run_dirs = get_run_dirs(product_dir)
    
    if len(run_dirs) <= keep:
        return 0
    
    to_remove = run_dirs[keep:]
    removed = 0
    
    for run_dir in to_remove:
        if dry_run:
            print(f"[DRY-RUN] Would remove: {run_dir}")
        else:
            print(f"[*] Removing: {run_dir}")
            shutil.rmtree(run_dir)
        removed += 1
    
    return removed


def main():
    parser = argparse.ArgumentParser(description="Garbage collect old run artifacts")
    parser.add_argument("--keep", type=int, required=True, help="Number of runs to keep per product")
    parser.add_argument("--product", help="Only GC a specific product (default: all)")
    parser.add_argument("--runs-dir", default=str(RUNS_DIR), help="Runs directory path")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be removed without removing")
    args = parser.parse_args()

    runs_dir = Path(args.runs_dir)
    
    if not runs_dir.exists():
        print(f"[!] Runs directory not found: {runs_dir}")
        return 1

    total_removed = 0
    
    if args.product:
        # GC specific product
        product_dir = runs_dir / args.product
        if not product_dir.exists():
            print(f"[!] Product not found: {args.product}")
            return 1
        
        removed = gc_product(product_dir, args.keep, args.dry_run)
        total_removed += removed
        print(f"[*] {args.product}: removed {removed} old runs")
    else:
        # GC all products
        for product_dir in runs_dir.iterdir():
            if product_dir.is_dir():
                removed = gc_product(product_dir, args.keep, args.dry_run)
                total_removed += removed
                product_name = product_dir.name
                print(f"[*] {product_name}: removed {removed} old runs")

    verb = "Would remove" if args.dry_run else "Removed"
    print(f"\n[*] {verb} {total_removed} total run directories.")
    return 0


if __name__ == "__main__":
    exit(main())
