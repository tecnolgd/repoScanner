
## Contributing to repoScanner

Thank you for your interest in contributing to repoScanner! We aim to build a powerful, flexible repository analysis tool that scales efficiently.

Whether you're fixing a bug, adding support for a new language, improving reports, or optimizing performance, your help is welcome.

### Development Setup

To set up your local development environment and build the project, please follow the Installation Instructions in the [README.md](README.md#build-instructions).

*Additional Dev Note: Ensure you have Python 3.8+ and pip installed, as our project relies on standard Python tooling*.

### Development Workflow

- **Code Style:** Keep it clean and readable. 

- **Performance:** repoScanner's core goal is efficient repository analysis. Any new feature should have minimal overhead on scan time and memory usage.

- **Testing:** If you add a new analyzer or scanner feature (e.g., new language support or metrics), please ensure it is modular and doesn't break existing functionality.

## The Required Contribution Workflow

To keep the codebase stable and ensure your time isn't wasted, all contributors **must** follow this exact workflow. Pull Requests that skip these steps will be closed without code review.

### 1. Find or Open an Issue First

* Do not write code or open a Pull Request out of nowhere.
* Look at our [Open Issues](https://github.com/tecnolgd/repoScanner/issues) tab. If you find a bug or a feature you want to tackle, comment on that specific issue stating your intent to fix it.
* If you have a new idea, open a new issue first to discuss the architectural impact with the maintainers.

### 2. Wait to be Officially Assigned

* **Do not start working until a maintainer officially assigns the issue to you.**
* We will not accept PRs from unassigned contributors. This prevents multiple people from accidentally working on the exact same file at the same time.

### 3. One Branch, One Pull Request

* When you are ready to submit, use standard keywords in your PR description to link your work (e.g., `Closes #30` or `Fixes #30`).
* **Do not open duplicate Pull Requests.** If you need to fix your code, update your existing branch and push the new commits to your fork. The original Pull Request thread will update automatically.

### 4. Code and Communication Standards

* **Language:** All source code, terminal logs, pull request descriptions, and in-line code comments **must be written in English**.
* Keep pull request descriptions clean, formatted, and focused entirely on the issue layout.

### Make Changes & Submit PR

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit your changes: `git commit -m "feat: description"`
3. Push to your fork: `git push origin feature/your-feature`
4. Open a Pull Request with a clear description linking to the issue

### Current Priorities

Looking for a place to start?
Check:

- [Roadmap](assets/docs/roadmap.md) for planned ideas
- [Open Issues](https://github.com/tecnolgd/repoScanner/issues) to find bugs and features you can contribute to

### Ideas for Contribution

- Add language support (JavaScript, Go, Rust, TypeScript, etc.)
- Add HTML report generation
- Add circular dependency detection
- Write comprehensive tests
- Improve documentation
- Optimize scan time and memory usage