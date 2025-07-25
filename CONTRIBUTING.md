# Contributing to Skylos

## How Can I Contribute?

### Reporting Bugs
- If you find a bug, please open an issue on GitHub.
- Include a clear title and description.
- Describe the steps to reproduce the bug.
- Include details about your environment (OS, Python version, Skylos version).
- Provide any relevant error messages or logs.

### Suggesting Enhancements
- Open an issue on GitHub to discuss your ideas.
- Clearly describe the feature and why it would be useful.

### Pull Requests

1.  **Fork the repo:** Click the "Fork" button at the top right of the [Promptvc GitHub page](https://github.com/duriantaco/promptvc).
2.  **Clone your fork:** `git clone https://github.com/YOUR_USERNAME/promptvc.git`
3.  **Create a separate branch:** `git checkout -b feature/your-changes` or `bugfix/the-bug-you-fixed`
4.  **Set Up Development Environment:**
    * Please ensure that you have at least Python (>=3.9) installed.
    * Build promptvc in development mode: `pip install -e .`

5.  **Make Your Changes:**
6.  **Add Tests:**
    * For Python integration tests: `pytest tests/` from the project root.
    * Ensure your changes are covered by new or existing tests

7.  **Update Docs:** If your changes affect user facing features or the API, please update `README.md` or other relevant docs.
8.  **Commit Your Changes:** `git commit -am 'your changes'`
9.  **Push to Your Branch:** `git push origin feature/your changes`
10. **Open a Pull Request:** Go to the promptvc repo and open a pull request from your forked branch
    * Provide clear description of your changes.
    * Reference any related issues.

## Code Style
- You can look at our code and just follow it accordingly. Try your best to follow best practices. 

## Getting Help
If you have questions or need help, feel free to open an issue with the "question" label.

Thank you for contributing!