# SIF Website

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**The official Semantic Infrastructure Foundation website - a clean Python web application demonstrating SIF architecture principles.**

## Overview

This is the public-facing website for the Semantic Infrastructure Foundation, built as a production-quality reference implementation of SIF's architectural principles:

- **Clarity**: Clean layered architecture
- **Simplicity**: Minimal dependencies, standard tools
- **Composability**: Small, reusable components
- **Correctness**: Type-safe, well-tested
- **Verifiability**: Structured logging, clear data flow

## Architecture

This project uses a clean layered architecture following SIL's development principles:

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

**Content Integration:**
- Loads canonical docs from SIF/SIL documentation
- Displays research and foundation information
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

- **/** - Home page
- **/about** - About the Semantic Infrastructure Foundation
- **/research** - Research and production systems
- **/funding** - Funding model and approach
- **/foundation** - Foundation governance and structure
- **/foundation/chief-steward** - Chief Steward role description
- **/foundation/executive-director** - Executive Director role description
- **/contact** - Contact information

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

**Primary Method:** Container-based deployment using TIA infrastructure.

### Quick Deploy

```bash
# Deploy to staging
./deploy/deploy-container.sh staging

# Deploy to production
./deploy/deploy-container.sh production
```

**What this does:**
1. Builds container image with SIF content baked in
2. Pushes to `registry.mytia.net`
3. Deploys to target server (tia-staging or tia-apps)
4. Runs health checks
5. Verifies deployment

### Infrastructure

| Environment | Server | URL |
|-------------|--------|-----|
| **Staging** | tia-staging | https://sif-staging.mytia.net |
| **Production** | tia-apps | https://semanticinfrastructurefoundation.org |

**Container Registry:** `registry.mytia.net/sif-website`

### Full Documentation

See [DEPLOYMENT.md](./DEPLOYMENT.md) for:
- Step-by-step deployment guide
- Container architecture
- Rollback procedures
- Troubleshooting
- Monitoring

### Alternative: Local Development Container

```bash
# Build and run locally
podman build -t sil-website:dev .
podman run -p 8000:8000 sil-website:dev
```

## Development Principles

This project demonstrates clean architectural principles in practice:

1. **Layer separation**: Domain → Services → UI → Routes
2. **Pure functions**: Domain and UI are pure (no side effects)
3. **Explicit dependencies**: Constructor injection, no globals
4. **Small functions**: 3-7 lines is ideal
5. **Type safety**: Full mypy coverage
6. **Structured logging**: All services use structlog
7. **Testability**: Pure functions are easy to test

## Contributing

1. Follow TIA Python guidelines
2. Keep functions small (3-7 lines)
3. Maintain layer separation
4. Add tests for new features
5. Run `ruff format` before committing

## License

Apache 2.0 - see [LICENSE](LICENSE) for details

Copyright 2025 Semantic Infrastructure Foundation Contributors

**Content License**: Documentation and written content are licensed under CC BY 4.0 - see [CONTENT_LICENSE.md](CONTENT_LICENSE.md)

## Links

- **Live Website**: https://semanticinfrastructurefoundation.org
- **Staging Website**: https://sif-staging.mytia.net
- **SIL Repository**: https://github.com/scottsen/sil
- **TIA System**: https://github.com/scottsen/tia

---

**Built with clarity, simplicity, and composability.**
