# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- N/A

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

## [1.1.0] - 2025-06-08

### Added
- N/A

### Changed
- Simplified development toolchain by removing spell checking dependency

### Deprecated
- N/A

### Removed
- `typos` dependency and related spell checking functionality
- `type-check` Make target (was incorrectly named, was actually running spell check)
- Typos pre-commit hook

### Fixed
- N/A

### Security
- N/A

## [1.0.0] - 2025-06-08

### Added
- Initial project structure with modern Python development practices
- Core functionality with functional programming approach
- Comprehensive test suite with >85% coverage requirement (currently 87%)
- Development workflow with Make targets (20+ commands)
- Quality tooling: ruff (formatting/linting), pytest (testing)
- Pre-commit hooks for automated quality gates
- CLI interface using Click with --data and --debug options
- Configuration management with Pydantic Settings
- Structured logging with correlation support
- Complete documentation and development guidelines
- Comprehensive .gitignore file for Python projects
- Package management with uv (modern Python package manager)
- Environment variable support with PYTHON_TEMPLATE_ prefix
- Multiple execution methods (direct import and module execution)

### Changed
- N/A (initial major release)

### Deprecated
- N/A (initial major release)

### Removed
- N/A (initial major release)

### Fixed
- N/A (initial major release)

### Security
- N/A (initial major release)

## [0.1.0] - 2025-06-08

### Added
- Initial project setup
- Basic project structure
- Core application logic
- Test suite foundation
- Development tooling configuration
