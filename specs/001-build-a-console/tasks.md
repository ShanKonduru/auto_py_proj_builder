# Tasks: Python Framework Generator

**Input**: Design documents from `/specs/001-build-a-console/`  
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)

```text
1. Load plan.md from feature directory
   → Extract: Python 3.9+, Click CLI framework, Jinja2 templating, pytest testing
2. Load design documents:
   → data-model.md: 4 entities (ProjectTemplate, TemplateFile, ProjectMetadata, ConfigurationProfile)
   → contracts/: generate-command.md CLI contract
   → quickstart.md: 3 test scenarios
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: template loading, file generation
   → Polish: unit tests, performance, docs
4. Apply TDD: Tests before implementation
5. Number tasks sequentially (T001, T002...)
6. Create parallel execution examples
```

## Format: `[ID] [P?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Phase 3.1: Setup

- [x] T001 Create project structure with src/, tests/, templates/ directories
- [x] T002 Initialize Python project with Click, Jinja2, pytest dependencies in requirements.txt
- [x] T003 [P] Configure linting with ruff and formatting tools in pyproject.toml
- [x] T004 [P] Setup pytest configuration with markers in pytest.ini

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3

### CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation

- [x] T005 [P] Contract test for generate command CLI interface in tests/contract/test_generate_command.py
- [x] T006 [P] Integration test for basic project generation in tests/integration/test_basic_generation.py
- [x] T007 [P] Integration test for CLI project generation in tests/integration/test_cli_generation.py
- [x] T008 [P] Integration test for installation verification in tests/integration/test_installation.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)

- [x] T009 [P] ProjectTemplate model in src/models/project_template.py
- [x] T010 [P] TemplateFile model in src/models/template_file.py
- [x] T011 [P] ProjectMetadata model in src/models/project_metadata.py
- [x] T012 [P] ConfigurationProfile model in src/models/configuration_profile.py
- [x] T013 [P] TemplateLoader service in src/services/template_loader.py
- [x] T014 [P] ProjectGenerator service in src/services/project_generator.py
- [x] T015 [P] FileSystemService for file operations in src/services/filesystem_service.py
- [x] T016 CLI generate command in src/cli/generate_command.py
- [x] T017 Main CLI entry point in src/cli/main.py
- [x] T018 Input validation and error handling in src/utils/validation.py
- [x] T019 Template processing logic in src/utils/template_processor.py

## Phase 3.4: Integration

- [ ] T020 Connect TemplateLoader to file system templates in templates/
- [ ] T021 Wire ProjectGenerator with all model dependencies
- [ ] T022 Integrate CLI commands with service layer
- [ ] T023 Setup logging and error reporting configuration
- [ ] T024 Create default project templates (basic, web, cli, library)

## Phase 3.5: Polish

- [ ] T025 [P] Unit tests for ProjectTemplate validation in tests/unit/test_project_template.py
- [ ] T026 [P] Unit tests for TemplateFile processing in tests/unit/test_template_file.py
- [ ] T027 [P] Unit tests for CLI parameter validation in tests/unit/test_validation.py
- [ ] T028 [P] Performance tests for project generation (<5 seconds) in tests/performance/test_generation_speed.py
- [ ] T029 [P] Update README.md with installation and usage instructions
- [ ] T030 [P] Create setup.py for package distribution
- [ ] T031 Remove code duplication and refactor
- [ ] T032 Run manual testing scenarios from quickstart.md

## Dependencies

- Setup (T001-T004) before all other tasks
- Tests (T005-T008) before implementation (T009-T024)
- Models (T009-T012) before services (T013-T015)
- Services before CLI (T016-T017)
- Core implementation before integration (T020-T024)
- Integration before polish (T025-T032)

## Parallel Example

```bash
# Launch T005-T008 together (Test Phase):
Task: "Contract test for generate command CLI interface in tests/contract/test_generate_command.py"
Task: "Integration test for basic project generation in tests/integration/test_basic_generation.py"
Task: "Integration test for CLI project generation in tests/integration/test_cli_generation.py"
Task: "Integration test for installation verification in tests/integration/test_installation.py"

# Launch T009-T012 together (Model Phase):
Task: "ProjectTemplate model in src/models/project_template.py"
Task: "TemplateFile model in src/models/template_file.py"
Task: "ProjectMetadata model in src/models/project_metadata.py"
Task: "ConfigurationProfile model in src/models/configuration_profile.py"

# Launch T013-T015 together (Service Phase):
Task: "TemplateLoader service in src/services/template_loader.py"
Task: "ProjectGenerator service in src/services/project_generator.py"
Task: "FileSystemService for file operations in src/services/filesystem_service.py"
```

## Task Details

### T001: Create project structure

- Create `src/` directory with subdirectories: `models/`, `services/`, `cli/`, `utils/`
- Create `tests/` directory with subdirectories: `unit/`, `integration/`, `contract/`, `performance/`
- Create `templates/` directory for project templates
- Create root files: `README.md`, `requirements.txt`, `setup.py`, `pytest.ini`, `pyproject.toml`

### T005: Contract test for generate command

- Test CLI interface matches contract specification
- Verify all required parameters and options
- Test parameter validation rules
- Test success and error response formats

### T009: ProjectTemplate model

- Implement ProjectTemplate class with all attributes
- Add validation for project name (Python identifier)
- Add validation for Python version (>= 3.9)
- Add validation for email format
- Implement state transitions (Created → Validated → Generated → Completed)

### T016: CLI generate command

- Implement Click command with all parameters from contract
- Wire command to ProjectGenerator service
- Handle all validation errors gracefully
- Provide user-friendly success/error messages

## Notes

- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Follow TDD: Red → Green → Refactor
- Maintain 90% test coverage throughout

## Validation Checklist

- [x] All contracts have corresponding tests (T005 covers generate-command.md)
- [x] All entities have model tasks (T009-T012 cover all 4 entities)
- [x] All tests come before implementation (T005-T008 before T009+)
- [x] Parallel tasks truly independent (different files, no shared dependencies)
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task
- [x] TDD workflow enforced (tests must fail first)
- [x] Constitutional compliance maintained (OOP design, comprehensive testing)
