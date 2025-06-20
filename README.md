# CWL Chain Builder

`cwl-chain-builder` is a command-line utility that composes a CWL `Workflow` from a series of `Workflow`/`CommandLineTool` steps and **packs** it into a single self-contained CWL document.

It ensures:
- **Type-safe chaining** of step outputs to the next step's inputs.
- **Reusable, modular design** by keeping each step in its own file.
- **Packed output** ready for execution or distribution.

---

## 🚀 Features

- 🧱 Chain multiple `Workflow`/`CommandLineTool` CWLs into a `Workflow`;
- 🧪 Validate type compatibility between steps;
- 📦 Pack the entire workflow and dependencies into one file;
- 💾 Output to any location, with automatic directory creation.

---

## 🛠 Installation

```bash
pip install -e .
```

---

## 🧑‍💻 Usage

```bash
cwl-chain-builder \
--stage-in ./stage-in.cwl \
--workflow ./workflow.cwl \
--workflow-id water-bodies-detection \
--stage-out ./stage-out.cwl \
--output ./current.cwl
```

### 🔧 Options

| Option          | Description                                                                                      |
|-----------------|--------------------------------------------------------------------------------------------------|
| `--stage-in`    | The CWL `stage-in` file path.                                                                    |
| `--workflow`    | The CWL `app` file path.                                                                         |
| `--workflow-id` | The ID of the `Workflow` chained as `app`                                                        |
| `--stage_out`   | The CWL `stage-out` file path.                                                                   |
| `--output`      | The target CWL output file path. Intermediate directories are created if not existing.           |
| `--puml`        | Enable the generation of the [PlantUML](https://plantuml.com/) diagram of the generated Workflow |

---

## 🧠 Requirements

- Python ≥ 3.8

### Depenendies

Package installation will automatically install the following dependencies:

- [cwltool](https://cwltool.readthedocs.io/en/latest/)
- [cwl-utils](https://cwl-utils.readthedocs.io/en/latest/)
- [ruamel.yaml](https://yaml.dev/doc/ruamel.yaml/)
- [Jinja2](https://jinja.palletsprojects.com/en/stable/)
- [click](https://click.palletsprojects.com/en/stable/)
