cwlVersion: v1.2
class: CommandLineTool
id: clt
requirements:
    InlineJavascriptRequirement: {}
    EnvVarRequirement:
      envDef:
        PATH: $PATH:/app/envs/vegetation-index/bin
    ResourceRequirement:
      coresMax: 1
      ramMax: 512
hints:
  DockerRequirement:
    dockerPull: docker.io/library/vegetation-indexes:latest
baseCommand: 
- vegetation-index
arguments:
- pattern-1
inputs:
  item:
    type: Directory
    inputBinding:
        prefix: --input-item
  aoi:
    type: string
    inputBinding:
        prefix: --aoi
  epsg:
    type: string
    inputBinding:
        prefix: --epsg
  band:
    type:
      - type: array
        items: string
        inputBinding:
          prefix: '--band'

outputs:
  stac-catalog:
    outputBinding:
        glob: .
    type: Directory