# Contributing to SIL

Thank you for your interest in contributing to the Semantic Infrastructure Lab!

This document provides guidelines for contributing to SIL projects, documentation, and research.

---

## Ways to Contribute

### 1. Use and Report
- **Use SIL tools** (Reveal, TIA, Beth, Morphogen, etc.)
- **Report bugs** via GitHub Issues
- **Share feedback** on what works and what doesn't
- **Request features** that would help your workflow

### 2. Improve Documentation
- **Fix typos and errors** in documentation
- **Add examples** to existing docs
- **Improve clarity** where explanations are unclear
- **Create tutorials** for specific use cases
- **Add translations** (future)

### 3. Contribute Code
- **Fix bugs** in existing tools
- **Add features** aligned with SIL principles
- **Improve performance** or test coverage
- **Add new adapters** to Reveal (databases, config files, etc.)
- **Enhance tooling** (CLI improvements, error messages, etc.)

### 4. Research Contributions
- **Implement papers** from the [Research Agenda](docs/canonical/SIL_RESEARCH_AGENDA_YEAR1.md)
- **Propose new research** directions aligned with SIL's mission
- **Formalize concepts** with rigorous definitions
- **Write proofs** or verification of semantic contracts

---

## Before You Start

### Read the Foundation
1. **[Manifesto](docs/canonical/SIL_MANIFESTO.md)** — Understand SIL's mission
2. **[Principles](docs/canonical/SIL_PRINCIPLES.md)** — The 14 principles that guide all work
3. **[Technical Charter](docs/canonical/SIL_TECHNICAL_CHARTER.md)** — Formal invariants and guarantees

### Understand the Values
- **Clarity over cleverness** — Code should be obvious
- **Correctness over performance** — Get it right first, fast second
- **Simplicity over features** — Fewer primitives, more composition
- **Provenance everywhere** — Track where things come from
- **Verifiable by default** — Claims must be checkable

---

## Development Workflow

### 1. Setup

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/PROJECT_NAME
cd PROJECT_NAME

# Add upstream remote
git remote add upstream https://github.com/semantic-infrastructure-lab/PROJECT_NAME

# Create a feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

**Code Contributions:**
- Follow existing code style and patterns
- Write tests for new functionality
- Update documentation for changed behavior
- Ensure all tests pass before submitting

**Documentation Contributions:**
- Use clear, concise language
- Follow existing document structure
- Add examples where helpful
- Check all links work

### 3. Test Your Changes

```bash
# Run tests (varies by project)
pytest                    # Python projects
npm test                  # JavaScript projects
cargo test                # Rust projects

# Check code quality
ruff check .              # Python linting
mypy .                    # Python type checking

# Verify documentation builds
reveal docs/ --check      # Check for broken structure
```

### 4. Submit a Pull Request

```bash
# Commit with a clear message
git add .
git commit -m "Brief description of changes

Detailed explanation if needed:
- What changed
- Why it changed
- How it was tested"

# Push to your fork
git push origin feature/your-feature-name
```

Then:
1. Go to GitHub and create a Pull Request
2. Fill in the PR template with:
   - **What changed** — Clear description
   - **Why** — Motivation for the change
   - **How tested** — Evidence it works
   - **Related issues** — Link to issues addressed

---

## Code Style Guidelines

### General Principles
- **Readability first** — Code is read 10x more than written
- **Explicit over implicit** — No magic, no surprises
- **Minimal abstractions** — Only abstract when you have 3+ concrete cases
- **Self-documenting code** — Clear names reduce need for comments

### Python Projects
- Follow **PEP 8** style guide
- Use **type hints** for all functions
- Maximum line length: **100 characters**
- Prefer **composition over inheritance**
- Use **dataclasses** for structured data
- Run `ruff format` and `ruff check` before committing

### Documentation
- Use **Markdown** for all documentation
- Follow **semantic line breaks** (one sentence per line for diffs)
- Keep **paragraphs short** (2-4 sentences)
- Use **examples** to illustrate concepts
- Include **file paths** with line numbers when referencing code

---

## Testing Standards

### All Code Contributions Must:
1. **Pass existing tests** — `pytest` or equivalent
2. **Add new tests** for new functionality
3. **Maintain coverage** — Don't reduce test coverage
4. **Test edge cases** — Empty inputs, large inputs, invalid inputs

### Test Structure
```python
def test_feature_name():
    """Brief description of what's being tested."""
    # Arrange — Setup test data
    input_data = create_test_data()

    # Act — Execute the code under test
    result = function_under_test(input_data)

    # Assert — Verify expected behavior
    assert result == expected_output
    assert result.property == expected_value
```

---

## Documentation Standards

### Document Structure
- **One main heading** (`#`) per document
- **Clear hierarchy** with subheadings (`##`, `###`)
- **Examples after concepts** — Show, don't just tell
- **Links to related docs** at the bottom

### Writing Style
- **Active voice** — "Reveal parses code" not "Code is parsed"
- **Present tense** — "This function returns" not "This function will return"
- **Second person** — "You can use" not "One can use"
- **Short sentences** — Aim for clarity, avoid dense paragraphs
- **Technical precision** — Use exact terms from the [Glossary](docs/canonical/SIL_GLOSSARY.md)

---

## Pull Request Guidelines

### PR Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated for changed behavior
- [ ] Commit messages are clear and descriptive
- [ ] PR description explains what/why/how
- [ ] Links to related issues
- [ ] No merge conflicts with main branch

### Review Process
1. **Automated checks** run (tests, linting, type checking)
2. **Maintainer review** — May request changes
3. **Revisions** if needed — Address feedback
4. **Approval** — Maintainer approves PR
5. **Merge** — Maintainer merges when ready

**Timeline:** Most PRs reviewed within 3-5 business days.

---

## Project-Specific Guidelines

Each SIL project may have additional guidelines:

- **[Reveal](https://github.com/semantic-infrastructure-lab/reveal)** — Parser implementation patterns
- **[Morphogen](https://github.com/semantic-infrastructure-lab/morphogen)** — Test determinism requirements
- **[TIA](https://github.com/semantic-infrastructure-lab/tia)** — Domain registration patterns
- **[GenesisGraph](https://github.com/semantic-infrastructure-lab/genesisgraph)** — Cryptographic verification standards

Check each project's README for specific contribution guidelines.

---

## Communication

### GitHub Issues
- **Search first** — Check if issue already exists
- **Be specific** — Include reproduction steps, expected vs actual behavior
- **Provide context** — OS, version, environment details
- **Be respectful** — Assume good intent

### Questions & Discussion
- **GitHub Discussions** — For questions and design discussions
- **GitHub Issues** — For bugs and feature requests
- **Email** — For security issues: security@semanticinfrastructurelab.org

---

## Recognition

All contributors are recognized in:
- **CONTRIBUTORS.md** — In each project repository
- **Release notes** — For significant contributions
- **Documentation** — In acknowledgments sections

Significant research contributions may be invited to co-author papers.

---

## Code of Conduct

### Core Principles
- **Be respectful** — Treat everyone with dignity
- **Be constructive** — Critique ideas, not people
- **Be collaborative** — We're building together
- **Be patient** — Everyone is learning
- **Be open** — Assume good intent

### Unacceptable Behavior
- Harassment of any kind
- Discriminatory language or actions
- Personal attacks
- Trolling or deliberately disruptive behavior
- Violations of privacy

**Enforcement:** Violations may result in warning, temporary ban, or permanent ban depending on severity.

**Report issues to:** conduct@semanticinfrastructurelab.org

---

## License

By contributing, you agree that your contributions will be licensed under:
- **Code:** Apache 2.0 License
- **Documentation:** CC BY 4.0 License

See [LICENSE](LICENSE) and [CONTENT_LICENSE.md](CONTENT_LICENSE.md) for details.

---

## Questions?

- **[FAQ](docs/meta/FAQ.md)** — Common questions
- **[Reading Guide](docs/READING_GUIDE.md)** — Navigate the documentation
- **[GitHub Discussions](https://github.com/orgs/semantic-infrastructure-lab/discussions)** — Ask questions

---

**Thank you for contributing to the Semantic Infrastructure Lab!**

Together we're building the semantic substrate intelligent systems need.
