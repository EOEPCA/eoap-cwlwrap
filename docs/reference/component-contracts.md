# CWL Component Contracts

`eoap-cwlwrap` validates the stage-in and stage-out components before building the orchestrator workflow. The application workflow is inspected to decide which components are needed.

## Stage-In for Directory Inputs

A Directory stage-in process must contain:

- one input parameter compatible with [`URI`](https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml)
- one output parameter compatible with [`Directory`](https://www.commonwl.org/v1.2/CommandLineTool.html#Directory)

Only one input may be URI-compatible, and only one output may be `Directory`-compatible.

## Stage-In for File Inputs

A File stage-in process must contain:

- one input parameter compatible with [`URI`](https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml)
- one output parameter compatible with [`File`](https://www.commonwl.org/v1.2/CommandLineTool.html#File)

Only one input may be URI-compatible, and only one output may be `File`-compatible.

Stage-in processes may define additional non-URI inputs for configuration or credentials. The wrapper exposes those additional inputs on the generated `main` workflow and wires them into generated stage-in steps. The same additional stage-in input is exposed once per stage-in component type, even when multiple workflow inputs use that component.

## Stage-Out for Directory Outputs

A Directory stage-out process must contain:

- one input parameter compatible with [`Directory`](https://www.commonwl.org/v1.2/CommandLineTool.html#Directory)
- one output parameter compatible with [`URI`](https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml)

Only one input may be `Directory`-compatible, and only one output may be URI-compatible.

## Stage-Out for File Outputs

A File stage-out process must contain:

- one input parameter compatible with [`File`](https://www.commonwl.org/v1.2/CommandLineTool.html#File)
- one output parameter compatible with [`URI`](https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml)

Only one input may be `File`-compatible, and only one output may be URI-compatible.

Stage-out processes may define additional inputs such as bucket names, subpaths, endpoints, or credentials. The wrapper exposes those additional inputs on the generated `main` workflow and wires them into generated stage-out steps.

Additional stage-in and stage-out input ids are copied onto the generated workflow unchanged. Keep those ids unique across the application workflow and the selected stage components so the generated workflow interface is unambiguous.

## Application Workflow Inputs

Application workflow inputs compatible with `Directory` or `File` are exposed on the orchestrator workflow as URI-compatible inputs. Nullable values and arrays are preserved:

- `Directory` becomes `URI`
- `File` becomes `URI`
- `Directory[]` becomes `URI[]`
- `File[]` becomes `URI[]`
- `Directory?` becomes `URI?`
- `File?` becomes `URI?`

Inputs that are not compatible with `Directory` or `File` are forwarded unchanged.

## Application Workflow Outputs

Application workflow outputs compatible with `Directory` or `File` are connected to the matching stage-out process and exposed as URI-compatible outputs. Outputs with other types are forwarded from the application workflow unchanged.
