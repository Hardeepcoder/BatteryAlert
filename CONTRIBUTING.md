# Contributing to Battery Alert

Thank you for your interest in contributing to Battery Alert! As an open-source utility maintaining battery health across platforms, we welcome community contributions, bug reports, and optimizations.

---

## Code of Conduct
We are committed to providing a welcoming, productive, and harassment-free environment for everyone. Please be respectful and constructive in all issues and pull requests.

---

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Hardeepcoder/BatteryAlert.git
   cd BatteryAlert
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the test suite:**
   ```bash
   python3 -m unittest discover tests -v
   ```

5. **Run the application locally:**
   ```bash
   python3 app.py
   ```

---

## Submitting Pull Requests

1. Fork the repository and create your branch from `main`:
   ```bash
   git checkout -b feature/my-cool-feature
   ```
2. Keep PRs focused on a single topic, bug, or feature.
3. Ensure all existing and new unit tests pass before submitting.
4. Open a Pull Request referencing any relevant issues.
