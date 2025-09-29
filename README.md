# Interactive Calculator (CLI)

A simple, robust command-line calculator built in Python.  
Features a REPL (Read–Eval–Print Loop), proper error handling, 100% test coverage with `pytest`, and continuous integration via GitHub Actions.
## Project Structure
interactive-calculator/
├── calc/
│   ├── __init__.py
│   ├── cli.py
│   └── operations.py
├── tests/
│   ├── conftest.py
│   ├── test_cli.py
│   └── test_operations.py
├── main.py
├── requirements.txt
├── pytest.ini
└── .github/
    └── workflows/
        └── ci.yml
## Setup Instructions

### 1. Clone the repository
```powershell
git clone https://github.com/<your-username>/interactive-calculator.git
cd interactive-calculator
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

---

## 5. Usage (how to run the app)  

```markdown
## Usage
Run the calculator REPL:

```powershell
py main.py

---

## 6. Testing  

```markdown
## Testing
Run all tests with coverage:
```powershell
pytest

---

## 7. Continuous Integration  

```markdown
## Continuous Integration
- GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push/pull request
- Uses Python 3.11
- Installs dependencies, runs `pytest`
- Build fails if coverage < 100%
## Contributing
1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes
4. Push to your fork
5. Open a Pull Request
