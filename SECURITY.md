# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅        |

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **Do NOT** open a public issue
2. Email security@novelbyte.io with details
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you on disclosure.

## Security Considerations

ArqonShip handles:
- Source code parsing
- Local AI model inference
- Git repository access
- GitHub API credentials

Always:
- Keep `GITHUB_TOKEN` secure
- Run in trusted environments
- Review generated code before committing
