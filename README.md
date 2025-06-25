# EOAP CWL wrap

`eoap-cwlwrap` is a command-line utility that composes a CWL `Workflow` from a series of `Workflow`/`CommandLineTool` steps, defined according to [Application package patterns based on data stage-in and stage-out behaviors commonly used in EO workflows](https://github.com/eoap/application-package-patterns), and **packs** it into a single self-contained CWL document.

It ensures:
- **Type-safe chaining** of step outputs to the next step's inputs.
- **Reusable, modular design** by keeping each step in its own file.
- **Packed output** ready for execution or distribution.

---

## 🧠 Prerequisites

### stage-in

- _One_ input parameter of type [URL](https://raw.githubusercontent.com/eoap/schemas/main/url.yaml);
- _One_ output of type [Directory](https://www.commonwl.org/v1.0/CommandLineTool.html#Directory).

### stage-out 

- _One_ input parameter of type [Directory](https://www.commonwl.org/v1.0/CommandLineTool.html#Directory);
- _One_ output of type [URL](https://raw.githubusercontent.com/eoap/schemas/main/url.yaml).

### app

Inputs:

- has one or more parameter of type [Directory](https://www.commonwl.org/v1.0/CommandLineTool.html#Directory)
  * it can be nullable `?`;
  * it can be an array `[]`.

Outputs:

- has one or more parameter of type [Directory](https://www.commonwl.org/v1.0/CommandLineTool.html#Directory)
  * it can be an array `[]`.

### main

- `inputs` coming from `app`:
  * if type is assignable to [Directory](https://www.commonwl.org/v1.0/CommandLineTool.html#Directory) it is converted to [URL](https://raw.githubusercontent.com/eoap/schemas/main/url.yaml) input in `main`;
  * any other kind of input won't be transformed;
- `outpus` coming from `app`:
  * if type is assignable to [Directory](https://www.commonwl.org/v1.0/CommandLineTool.html#Directory) it is converted to [URL](https://raw.githubusercontent.com/eoap/schemas/main/url.yaml) output in `main`;
  * any other kind of output won't be transformed, but referenced to the related `app` output;

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
eoap-cwlwrap \
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

### Dependendies

Package installation will automatically install the following dependencies:

- [cwltool](https://cwltool.readthedocs.io/en/latest/)
- [cwl-utils](https://cwl-utils.readthedocs.io/en/latest/)
- [ruamel.yaml](https://yaml.dev/doc/ruamel.yaml/)
- [Jinja2](https://jinja.palletsprojects.com/en/stable/)
- [click](https://click.palletsprojects.com/en/stable/)
