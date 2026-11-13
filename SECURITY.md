# Security Policy

The Battery Alert team takes the security and privacy of our users seriously. Because Battery Alert operates as a local background system utility with access to OS telemetry, we enforce strict local-first and zero-telemetry architecture principles.

---

## Supported Versions

Only the latest release versions receive security updates and bug fixes:

| Version | Supported          |
| :---    | :---               |
| 1.4.x   | :white_check_mark: |
| 1.3.x   | :white_check_mark: |
| < 1.3.0 | :x:                |

---

## Security & Privacy Guarantees

Battery Alert is engineered with privacy as a foundational requirement:

1. **100% Local Execution**: All battery telemetry is polled directly from hardware sensors via native operating system APIs (`psutil.sensors_battery()`).
2. **Zero Telemetry & Tracking**: The application contains no analytics engines, trackers, user identifiers, or telemetry beacons.
3. **No External Network Dependencies**: Aside from optional asynchronous GitHub release version checks, no network connections are initiated.
4. **Subprocess Isolation**: Audio playback and native notifications run in sandboxed local threads without elevated privileges.

---

## Reporting a Vulnerability

If you discover a security vulnerability or potential privacy issue in Battery Alert, please disclose it responsibly:

1. **Do NOT open a public GitHub issue** for undisclosed security vulnerabilities.
2. Email the maintainer directly at: **admin@codingsart.com**
3. Please include:
   - Description of the vulnerability and potential impact.
   - Operating system and version (macOS / Windows).
   - Step-by-step reproduction steps or Proof of Concept (PoC).

### Our Commitment
- We will acknowledge receipt of your vulnerability report within **48 hours**.
- We will provide a status update and coordinate a patch release.
- Legitimate security reporters will be credited in our release notes and changelog (unless requested otherwise).
