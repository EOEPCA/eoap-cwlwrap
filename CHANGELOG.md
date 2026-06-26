# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Add this Keep a Changelog-formatted changelog rebuilt from Git release tags
  and project history.
- Add Python 3.14 support to the package classifiers, Hatch test matrix, and
  GitHub Actions package workflow.
- Add CI matrix builds across Python 3.10 through Python 3.14 with Ruff checks
  before packaging.
- Add merging for auxiliary CWL schema imports when a wrapped workflow already
  defines a `SchemaDefRequirement`.

### Changed

- Bump runtime and development dependencies, including `click`, `cwl-loader`,
  `mypy`, `ruff`, `coverage`, and documentation tooling.
- Move package, PyPI, and container publication behind tag-gated release jobs.
- Format source and tests with Ruff.

### Fixed

- Remove the Polyfill.io script from the MkDocs configuration to avoid browser
  login prompts.
- Fix lint and format issues reported by CI.

## [0.28.0] - 2026-05-15

### Fixed

- Preserve `SchemaDefRequirement` definitions from the wrapped workflow when building
  the orchestrator workflow.

## [0.27.0] - 2026-05-05

### Added

- Add session-adapter based loading for application packages, including `file://`,
  `s3://`, and `oci://` locations.
- Add OCI authentication options to the CLI through `OCI_HOSTNAME`,
  `OCI_USERNAME`, and `OCI_PASSWORD`.
- Add separate Directory and File stage-out support, with dedicated
  `--directory-stage-out` and `--file-stage-out` CLI options.
- Add support for selecting a process from a CWL `$graph` with
  `<location>#<process-id>` references.
- Add MkDocs reference, how-to, tutorial, and explanation pages generated with
  `mkdocstrings`.
- Add the serialized `current.cwl` example artifact.

### Changed

- Refactor the wrapping API around a selected workflow `Process` and separate
  Directory/File stage-in and stage-out processes.
- Keep `--workflow-id` and `--stage-out` as deprecated compatibility CLI
  options while moving selection and stage-out configuration to the newer
  arguments.
- Rebuild `wrap_locations` so it loads every referenced CWL document with a
  shared `requests.Session`, assembles the wrapper graph, and orders it by
  dependencies.
- Pin runtime, test, type-checking, and documentation dependencies, including
  `click`, `cwl-loader`, `cwl-utils`, `cwltool`, `loguru`, `mypy`, `ruff`,
  `nose2`, and MkDocs packages.
- Drop Python 3.9 from the declared classifiers and test matrix.
- Replace local quality task definitions with the shared Taskfile quality
  include.
- Reorganize the documentation navigation around tutorials, how-to guides,
  reference, and explanation sections.

### Fixed

- Avoid redundant generated workflow graph entries and update the affected tests.
- Print the absolute path for the serialized workflow output.
- Fix the GitHub Actions documentation build regression from the release branch.

## [0.26.0] - 2026-02-18

This is the first tagged release in the repository. The entries below summarize
the project history up to `v0.26.0`.

### Added

- Add the initial EOAP CWL wrapper library and CLI for composing orchestrator
  workflows around application package stage-in, application, and stage-out
  components.
- Add CWL loading from raw mappings, local filesystem paths, and remote URLs.
- Add validation for stage-in and stage-out component contracts.
- Add CWL type helpers for nullable values, arrays, Directory/File compatibility,
  URI conversion, and `SchemaDefRequirement` handling.
- Add support for File inputs in stage-in data flow management.
- Add support for optional workflow outputs through CWL `when` conditions.
- Add support for scattering steps and multiple application package wrapping
  patterns, including pattern 10, pattern 11, and pattern 12 test coverage.
- Add PlantUML and `cwltool` based workflow visualization helpers.
- Add generated CWL examples, notebooks, and project documentation for the
  supported wrapping patterns.
- Add Docker and CI support, including container build automation and test tasks.

### Changed

- Rename and align the project as `eoap-cwlwrap`.
- Split CLI concerns from the Python API and refactor the original monolithic
  workflow builder into smaller modules.
- Replace custom CWL loading code with the `cwl-loader` package and update
  dependency versions across the project.
- Relicense the project and refresh dependency metadata.
- Simplify examples and point users to the EOAP application package pattern
  documentation for exhaustive pattern material.
- Update containers with supporting tools such as `yq`, `jq`, and Node.js.

### Fixed

- Correct the wiring from application outputs to stage-out inputs and from
  stage-in outputs to application inputs.
- Include auxiliary application outputs in the generated orchestrator workflow.
- Preserve and import schema definitions required by input workflows.
- Fix handling of nullable multi-types, arrays, scatter values, `$import` arrays,
  `run` references, and `outputSource` serialization.
- Prevent non-target workflows from being cut off in the resulting wrapped
  workflow graph.
- Fix validation errors involving embedded workflows and
  `SubworkflowFeatureRequirement`.
- Fix documentation, generated diagrams, CI configuration, and container builds.

[Unreleased]: https://github.com/EOEPCA/eoap-cwlwrap/compare/v0.28.0...HEAD
[0.28.0]: https://github.com/EOEPCA/eoap-cwlwrap/compare/v0.27.0...v0.28.0
[0.27.0]: https://github.com/EOEPCA/eoap-cwlwrap/compare/v0.26.0...v0.27.0
[0.26.0]: https://github.com/EOEPCA/eoap-cwlwrap/releases/tag/v0.26.0
