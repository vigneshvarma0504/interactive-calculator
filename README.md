## Setup Instructions

### 1. Clone the repository
```powershell
git clone https://github.com/<your-username>/interactive-calculator.git
cd interactive-calculator


Make sure:
- It sits under **“Setup Instructions”**.
- Replace `<your-username>` with your actual GitHub username. Example:
  ```powershell
  git clone https://github.com/vigneshvarma/interactive-calculator.git
  cd interactive-calculator

# Interactive Calculator (CLI)

A simple, robust command-line calculator built in Python.  
Features a REPL (Read–Eval–Print Loop), proper error handling, 100% test coverage with `pytest`, and continuous integration via GitHub Actions.

---

## Features
- **REPL interface**: interactively run commands until you type `quit`
- **Arithmetic operations**: addition, subtraction, multiplication, division
- **User-friendly prompts and feedback**
- **Error handling**:
  - Invalid commands
  - Non-numeric inputs
  - Division by zero
- **Best practices**: DRY principle, modular code
- **Testing**:
  - Unit tests for all operations
  - Parameterized tests for multiple scenarios
  - 100% code coverage enforced
- **CI/CD**:
  - GitHub Actions workflow runs tests on each push/pull request
  - Build fails if coverage < 100%

---

## Project Structure
