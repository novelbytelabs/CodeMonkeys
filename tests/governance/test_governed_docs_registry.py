
import pytest
from pathlib import Path
import json

GOVERNED_DOCS_PATH = Path("docs/pm/GOVERNED_DOCS.md")

def test_governed_docs_registry_exists():
    assert GOVERNED_DOCS_PATH.exists()

def test_governed_docs_registry_content():
    content = GOVERNED_DOCS_PATH.read_text()
    assert "| `constitution.md` | Constitution |" in content
    assert "| `docs/pm/GOVERNED_DOCS.md` | Registry |" in content

def test_all_registered_docs_exist():
    # Simple parser to extract paths from the markdown table
    content = GOVERNED_DOCS_PATH.read_text()
    lines = content.splitlines()
    table_started = False
    
    for line in lines:
        if "| Document |" in line:
            table_started = True
            continue
        if not table_started or not line.strip().startswith("|"):
            continue
        if "---" in line:
            continue
            
        parts = [p.strip() for p in line.split("|")]
        if len(parts) > 2:
            doc_path_raw = parts[1].strip("`")
            # Handle glob patterns roughly (just skip them for now or verify dir exists)
            if "*" in doc_path_raw:
                # e.g. docs/dossiers/*.md
                dir_path = Path(doc_path_raw.split("*")[0])
                assert dir_path.exists(), f"Directory for wildcard {doc_path_raw} missing"
            else:
                doc_path = Path(doc_path_raw)
                assert doc_path.exists(), f"Registered doc {doc_path} missing"
