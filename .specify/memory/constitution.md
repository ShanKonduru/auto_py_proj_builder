<!--
Sync Impact Report:
- Version change: none → 1.0.0
- Added principles: I. Object-Oriented Design, II. Test-Driven Development, III. Unit Testing Excellence, IV. Console Application Standards, V. Code Quality Gates
- Added sections: Quality Standards, Development Workflow  
- Templates requiring updates: ✅ plan-template.md, ✅ spec-template.md, ✅ tasks-template.md
- No follow-up TODOs
-->

# Auto Py Proj Builder Constitution

## Core Principles

### I. Object-Oriented Design (NON-NEGOTIABLE)

Every component MUST be designed with proper object-oriented principles: encapsulation, inheritance, and polymorphism. Classes MUST have single responsibility, clear interfaces, and proper separation of concerns. No procedural code in business logic layers - all functionality MUST be encapsulated in well-designed classes with clear contracts.

### II. Test-Driven Development (NON-NEGOTIABLE)

TDD MUST be strictly followed: Tests written first → Tests MUST fail → User approval → Then implement. Red-Green-Refactor cycle is mandatory for all business logic. No implementation code without failing tests. Test coverage MUST be validated before any code integration.

### III. Unit Testing Excellence

All business logic MUST have comprehensive unit tests with minimum 90% code coverage. External dependencies MUST be mocked using unittest.mock or pytest-mock. Tests MUST be fast (<1s each), isolated, and deterministic. Integration tests are separate from unit tests.

### IV. Console Application Standards

All console applications MUST use proper CLI frameworks (argparse, click, or typer). Error handling MUST be graceful with user-friendly messages. Output MUST support both human-readable and JSON formats. Logging MUST be structured and configurable.

### V. Code Quality Gates

Static analysis MUST pass: type checking (mypy), linting (ruff or pylint), and formatting (black). All quality gates MUST be automated in CI/CD. Code complexity MUST be justified if exceeding standard thresholds. Dependencies MUST be pinned and security-scanned.

## Quality Standards

Python version MUST be 3.9+ with type hints mandatory for all public interfaces. Documentation MUST include docstrings for all public methods following Google or NumPy style. Performance requirements: CLI commands MUST respond within 2 seconds for typical use cases.

## Development Workflow

All code changes MUST go through pull request review. Branch naming MUST follow pattern: `feature/###-description` or `bugfix/###-description`. Commit messages MUST be descriptive and reference issue numbers. Pre-commit hooks MUST run all quality gates locally.

## Governance

This constitution supersedes all other development practices and guidelines. Amendments require documentation of impact, team approval, and migration plan for existing code. All pull requests MUST verify constitutional compliance. Complexity violations MUST be justified with technical debt tracking.

**Version**: 1.0.0 | **Ratified**: 2025-09-21 | **Last Amended**: 2025-09-21