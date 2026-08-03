# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | Yes                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue for security vulnerabilities
2. Instead, please contact the maintainer via GitHub Issues with a private report
3. Include a description of the vulnerability and steps to reproduce
4. Allow time for the issue to be fixed before public disclosure

## Scope

This project is an educational library for learning programming. Security concerns may include:

- Unsafe file operations
- Network request vulnerabilities
- Input validation issues

## Best Practices

When using this library:

- Do not use `Network` methods with untrusted URLs in production applications
- Validate user input before passing to file operations
- Be aware that this library is designed for educational purposes, not production use
