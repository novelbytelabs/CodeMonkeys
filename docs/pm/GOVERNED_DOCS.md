# Governed Documents Registry

**Doc ID**: GOV-001  
**Status**: Active  
**Validator**: Silverback  

## Intent
This registry defines the documents that are considered "Law" or "Contract" within the Code Monkeys factory. Modification of these documents requires explicit approval and adheres to strict headers.

## Canonical Documents

| Document | Type | Owner | Approval | Silverback Logic |
|---|---|---|---|---|
| `constitution.md` | Supreme Law | Human | Manual | Must exist, must contain Preamble |
| `docs/pm/00_VISION_STRATEGY.md` | Strategy | Human | Manual | Must exist, check pilllrs |
| `docs/pm/AUTONOMY_GOVERNANCE.md` | Governance | Human | Manual | Must exist, check rules |
| `docs/pm/GOVERNED_DOCS.md` | Registry | Nexus | Human | Start here |
| `specs/**/*.md` | Contract | Nexus | Auto/Human | Must follow templates |
| `nexus/schemas/*.json` | Schema | Nexus | Auto | JSON Schema validation |
| `dash/schemas/*.json` | Schema | Nexus | Auto | JSON Schema validation |

## Header Requirements

All governed markdown documents must start with a metadata block:

```markdown
**Doc ID**: <ID>
**Status**: <Status>
**Owner**: <Owner>
```

## Approval Levels

1.  **Manual**: Requires explicit human override or PR approval.
2.  **Auto/Human**: Can be updated by agents if verified by tests, otherwise human.
3.  **Auto**: Can be updated by agents if schema valid.
