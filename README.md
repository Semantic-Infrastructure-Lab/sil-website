# SIL Website

**The official Semantic Infrastructure Lab website - a clean Python web application demonstrating SIL architecture principles.**

## Overview

This is the public-facing website for the Semantic Infrastructure Lab, built as a production-quality reference implementation of SIL's architectural principles:

- **Clarity**: Clean layered architecture
- **Simplicity**: Minimal dependencies, standard tools
- **Composability**: Small, reusable components
- **Correctness**: Type-safe, well-tested
- **Verifiability**: Structured logging, clear data flow

## Architecture

Following the [TIA Python Development Guide](../tia/docs/guides/TIA_PYTHON_DEVELOPMENT_GUIDE.md), this project uses a clean layered architecture:

```
src/sil_web/
├── domain/       # Pure models (Project, Document, Author)
├── services/     # Business logic (ContentService, GitHubService)
├── ui/           # Pure rendering (project_card, nav_bar)
├── routes/       # Thin handlers (/, /projects, /docs)
└── config/       # Settings and wiring
```

**Why this structure?**
- Domain layer is pure Python (no I/O, easily testable)
- Services handle all side effects (file I/O, HTTP calls)
- UI is pure rendering (no logic, just presentation)
- Routes are thin adapters (parse → call service → render)

## Tech Stack

**Core:**
- FastAPI - Modern Python web framework
- Jinja2 - Template engine
- uvicorn - ASGI server

**Tooling:**
- uv - Fast package management
- ruff - Fast linting and formatting
- pytest - Testing
- mypy - Type checking
- reveal - Code exploration

**SIL Integration:**
- Loads canonical docs from `../SIL/docs/canonical/`
- Displays production projects from SIL ecosystem
- Can fetch live GitHub stats (optional)

## Quick Start

### 1. Set up environment

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -e ".[dev]"
```

### 2. Run development server

```bash
# From project root
python src/sil_web/app.py

# Or using uvicorn directly
uvicorn sil_web.app:app --reload
```

Visit: http://localhost:8000

### 3. Development workflow

```bash
# Run tests
pytest

# Lint and format
ruff check .
ruff format .

# Type check
mypy src/

# Explore structure
reveal src/sil_web/
reveal src/sil_web/domain/models.py
```

## Project Structure

```
sil-website/
├── src/
│   └── sil_web/
│       ├── domain/
│       │   └── models.py          # Project, Document, Author
│       ├── services/
│       │   ├── content.py         # Load docs and projects
│       │   └── github.py          # Fetch GitHub stats
│       ├── ui/
│       │   └── components.py      # project_card, nav_bar
│       ├── routes/
│       │   └── pages.py           # Route handlers
│       ├── config/
│       │   └── settings.py        # Configuration
│       └── app.py                 # Main application
│
├── templates/                     # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── projects.html
│   ├── docs_index.html
│   └── document.html
│
├── static/                        # Static assets
│   ├── css/
│   │   └── style.css
│   ├── js/
│   └── images/
│
├── tests/                         # Test suite
│
├── pyproject.toml                 # Project configuration
└── README.md                      # This file
```

## Pages

- **/** - Founder's Letter (from `SIL/docs/canonical/FOUNDERS_LETTER.md`)
- **/projects** - All 5 production SIL projects with stats
- **/docs** - Documentation index (canonical documents)
- **/docs/{slug}** - Individual documents (manifesto, principles, etc.)

## Configuration

Edit `src/sil_web/config/settings.py`:

```python
# Path to SIL repository
SIL_REPO_PATH = BASE_DIR.parent / "SIL"

# Server settings
HOST = "0.0.0.0"
PORT = 8000
DEBUG = True

# Optional GitHub token for higher API rate limits
GITHUB_TOKEN = None  # or set via environment variable
```

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src tests/

# Specific test file
pytest tests/test_domain.py
```

## Deployment

### Option 1: Traditional Hosting

```bash
# Build for production
uv pip install build
python -m build

# Run with gunicorn
uv pip install gunicorn
gunicorn sil_web.app:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Option 2: Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["uvicorn", "sil_web.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Option 3: Static Build

For static hosting (GitHub Pages, Netlify):

```bash
# TODO: Add static site generator script
# Would pre-render all pages to static HTML
```

## Development Principles

This project demonstrates SIL's architectural principles in practice:

1. **Layer separation**: Domain → Services → UI → Routes
2. **Pure functions**: Domain and UI are pure (no side effects)
3. **Explicit dependencies**: Constructor injection, no globals
4. **Small functions**: 3-7 lines is ideal
5. **Type safety**: Full mypy coverage
6. **Structured logging**: All services use structlog
7. **Testability**: Pure functions are easy to test

See [TIA Python Development Guide](../tia/docs/guides/TIA_PYTHON_DEVELOPMENT_GUIDE.md) for full methodology.

## Contributing

1. Follow TIA Python guidelines
2. Keep functions small (3-7 lines)
3. Maintain layer separation
4. Add tests for new features
5. Run `ruff format` before committing

## License

MIT

## Links

- **SIL Repository**: https://github.com/scottsen/sil
- **Live Website**: https://semanticinfrastructurelab.org
- **TIA System**: https://github.com/scottsen/tia

---

**Built with clarity, simplicity, and composability.**
