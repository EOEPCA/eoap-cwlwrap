# CWL Component Contracts

`eoap-cwlwrap` validates the stage-in and stage-out components before building the orchestrator workflow. The application workflow is inspected to decide which components are needed.

## Stage-In for Directory Inputs

A Directory stage-in process must have:

- one input parameter compatible with [`URI`](https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml)
- one output parameter compatible with [`Directory`](https://www.commonwl.org/v1.2/CommandLineTool.html#Directory)

## Stage-In for File Inputs

A File stage-in process must have:

- one input parameter compatible with [`URI`](https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml)
- one output parameter compatible with [`File`](https://www.commonwl.org/v1.2/CommandLineTool.html#File)

## Stage-Out for Directory Outputs

A Directory stage-out process must have:

- one input parameter compatible with [`Directory`](https://www.commonwl.org/v1.2/CommandLineTool.html#Directory)
- one output parameter compatible with [`URI`](https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml)

## Stage-Out for File Outputs

A File stage-out process must have:

- one input parameter compatible with [`File`](https://www.commonwl.org/v1.2/CommandLineTool.html#File)
- one output parameter compatible with [`URI`](https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml)

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
