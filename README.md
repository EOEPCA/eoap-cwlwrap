# CWL Chain Builder

`cwl-chain-builder` is a command-line utility that composes a CWL `Workflow` from a series of `CommandLineTool` steps and **packs** it into a single self-contained CWL document.

It ensures:
- **Type-safe chaining** of step outputs to the next step's inputs.
- **Reusable, modular design** by keeping each step in its own file.
- **Packed output** ready for execution or distribution.

---

## 🚀 Features

- 🧱 Chain multiple `CommandLineTool` CWLs into a `Workflow`
- 🧪 Validate type compatibility between steps
- 📦 Pack the entire workflow and dependencies into one file using `cwltool.pack`
- 🆔 Automatically assign or customize a workflow ID
- 💾 Output to any location, with automatic directory creation

---

## 🛠 Installation

```bash
pip install .
```

---

## 🧑‍💻 Usage

```bash
cwl-chain-builder [OPTIONS] STEP1.cwl STEP2.cwl ... --output OUTFILE.cwl
```

### 🔧 Options

| Option           | Description                                                             |
|------------------|-------------------------------------------------------------------------|
| `--output`, `-o` | Output file path. Intermediate directories are created if not existing.     |
| `--workflow-id`  | Sets a custom workflow ID (default: auto-generated UUID)                |
| `--output`, `-o` | Output file path. Intermediate directories are created if not existing. |

---

## 🧪 Examples

### 🧬 Generate a fully packed CWL workflow

```bash
cwl-chain-builder steps/step1.cwl steps/step2.cwl -o dist/workflow-packed.cwl
```

### 🔍 Inspect raw workflow (no packing)

```bash
cwl-chain-builder steps/step1.cwl steps/step2.cwl --dry-run -o out/raw-workflow.cwl
```

### 🆔 Assign a specific workflow ID

```bash
cwl-chain-builder steps/*.cwl --workflow-id=my-custom-id -o out/final.cwl
```

---

## 🧪 Run Tests

```bash
pytest
```

---

## 🧠 Requirements

- Python ≥ 3.8
- `cwl-utils`
- `cwltool`
- `ruamel.yaml`
- `click`
