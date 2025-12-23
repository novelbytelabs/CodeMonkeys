#!/usr/bin/env python3
"""Generate science index for Dash Science Lane view."""
import json
import sys
from datetime import datetime
from pathlib import Path

import frontmatter


def find_linked_design_dossier(science_dossier_id: str, dossiers_dir: Path) -> str | None:
    """Find if a design dossier was created from this science dossier."""
    for dos_file in dossiers_dir.glob("DOS-*.md"):
        try:
            post = frontmatter.load(dos_file)
            evidence = post.metadata.get("evidence", {})
            if evidence.get("science_source") == science_dossier_id:
                return str(dos_file)
        except Exception:
            continue
    return None


def generate_science_index(
    science_dir: Path,
    dossiers_dir: Path,
    output_path: Path
) -> dict:
    """Generate science index JSON."""
    items = []

    if not science_dir.exists():
        return {"generated_at": datetime.now().isoformat() + "Z", "items": []}

    for sci_file in sorted(science_dir.glob("SCI-*.md")):
        try:
            post = frontmatter.load(sci_file)
            meta = post.metadata

            dossier_id = meta.get("dossier_id", sci_file.stem)
            topic = meta.get("topic", "Unknown")
            status = meta.get("status", "draft")
            created_at = meta.get("created_at", "")
            owner = meta.get("owner", "unknown")

            # Find linked design dossier
            design_path = find_linked_design_dossier(dossier_id, dossiers_dir)

            items.append({
                "dossier_id": dossier_id,
                "topic": topic,
                "status": status,
                "created_at": str(created_at),
                "owner": owner,
                "science_path": str(sci_file),
                "design_dossier_path": design_path
            })
        except Exception as e:
            print(f"Warning: Could not parse {sci_file}: {e}", file=sys.stderr)
            continue

    index = {
        "generated_at": datetime.now().isoformat() + "Z",
        "items": items
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(index, f, indent=2)

    return index


def main():
    science_dir = Path("docs/science")
    dossiers_dir = Path("docs/dossiers")
    output_path = Path("dash/science_index.json")

    index = generate_science_index(science_dir, dossiers_dir, output_path)

    print(f"Generated: {output_path}")
    print(f"  Items: {len(index['items'])}")

    for item in index["items"]:
        status_icon = "✅" if item["status"] == "validated" else "📝"
        converted = "→ " + item["design_dossier_path"] if item["design_dossier_path"] else ""
        print(f"  {status_icon} {item['dossier_id']}: {item['topic']} {converted}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
