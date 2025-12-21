# Implementation Plan: Code Monkeys Dash MVP (v0.1)

**Feature**: `000-dash-mvp`
**Spec**: [spec.md](./spec.md)

## Goal
Create a minimal, local-only dashboard that visualizes product status and evidence packs from structured JSON artifacts.

## Architecture
- **Tech Stack**: Vanilla HTML/JS/CSS (Bootstrap mode). No build step required.
- **Data Source**: Local filesystem JSON files (`dash/products.json`, `dash/runs/...`).
- **Serving**: Simple HTTP server (e.g., `python -m http.server`).

## Proposed Changes

### 1. Data Layer (Fixtures)
#### [NEW] `dash/products.json`
- Registry of products.
#### [NEW] `dash/runs/codemonkeys-dash/last_run.json`
- Sample run report for the dashboard itself.

### 2. UI Layer
#### [NEW] `dash/index.html`
- Main entry point.
- Layout: Header (Code Monkeys Dash), Product Grid/List.
#### [NEW] `dash/js/app.js`
- Logic to fetch `products.json`.
- Logic to fetch `last_run.json` for each product.
- Rendering logic (DOM manipulation).
- Error handling (missing files, invalid JSON).
#### [NEW] `dash/css/style.css`
- Basic styling (Dark mode/Premium aesthetic preference).

### 3. Verification Layer
#### [NEW] `tests/dash/test_schemas.py`
- Python script to validate JSON fixtures against a defined schema (using `jsonschema`).
- Ensures contract compliance.

## Verification Plan
### Automated
- Run `pytest tests/dash/test_schemas.py` to verify fixtures.
### Manual
- Start server: `cd dash && python -m http.server 8000`
- Open `http://localhost:8000`
- Verify Product List renders.
- Verify Details render (Status, Evidence Links, Economy).
- Verify Error States (temporarily rename a json file).
- Capture screenshot as `EV-001`.
