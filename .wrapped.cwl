cwlVersion: v1.2
$namespaces:
  s: https://schema.org/

schemas:
- http://schema.org/version/9.0/schemaorg-current-http.rdf

s:softwareVersion: 1.0.0
s:applicationCategory: Earth Observation application package
s:keywords:
- '@type': s:DefinedTerm
  s:name: application-type
  s:description: delineation
- '@type': s:DefinedTerm
  s:name: domain
  s:description: hydrology

s:thumbnail:
  '@type': s:ImageObject
  s:contentUrl: https://s3.waw3-2.cloudferro.com/swift/v1/stac-png/S2_L2A.jpg
  s:caption: Water bodies detected based on the NDWI and otsu threshold
  s:encodingFormat: image/jpeg
  s:height: '360'
  s:width: '640'


s:license:
  '@type': s:CreativeWork
  s:name: License CC BY 4.0
  s:url: https://creativecommons.org/licenses/by/4.0/
  s:encodingFormat: text/html

s:softwareHelp:
- '@type': s:CreativeWork
  s:name: User Manual
  s:url: https://eoap.github.io/application-package-patterns/
  s:encodingFormat: text/html

s:author:
  '@type': s:Person
  s:givenName: John
  s:familyName: Doe
  s:affiliation:
    '@type': s:Organization
    s:name: Make EO Great Again Platform
  s:email: john.doe@meogap.org
$graph:
- id: clt
  class: CommandLineTool
  inputs:
  - id: item
    type: Directory
    inputBinding:
      prefix: --input-item
  - id: aoi
    type: string
    inputBinding:
      prefix: --aoi
  - id: epsg
    type: string
    inputBinding:
      prefix: --epsg
  - id: band
    type:
    - name: _:feb92bc2-bbd2-4abd-b4d3-9da3448995a8
      items: string
      type: array
      inputBinding:
        prefix: --band
  outputs:
  - id: stac-catalog
    type: Directory
    outputBinding:
      glob: .
  requirements:
  - class: InlineJavascriptRequirement
  - class: EnvVarRequirement
    envDef:
    - envName: PATH
      envValue: /app/envs/runner/bin
  - class: ResourceRequirement
    coresMin: 1
    coresMax: 1
    ramMin: 512
    ramMax: 512
  hints:
  - class: DockerRequirement
    dockerPull: ghcr.io/eoap/application-package-patterns/runner:0.2.0
  cwlVersion: v1.2
  baseCommand:
  - runner
  arguments:
  - pattern-1
- id: main
  class: Workflow
  label: Workflow pattern-1 orchestrator
  doc: This Workflow is used to orchestrate the Workflow pattern-1
  inputs:
  - id: aoi
    label: area of interest - pattern-1/aoi
    doc: area of interest as a bounding box - This parameter is derived from 
      pattern-1/aoi
    default: -118.985,38.432,-118.183,38.938
    type: string
  - id: epsg
    label: EPSG code - pattern-1/epsg
    doc: EPSG code - This parameter is derived from pattern-1/epsg
    default: EPSG:4326
    type: string
  - id: bands
    label: bands used for the NDWI - pattern-1/bands
    doc: bands used for the NDWI - This parameter is derived from 
      pattern-1/bands
    default:
    - green
    - nir08
    type:
      name: _:7fc9b940-08b6-4b0e-bcb8-f7ad6269f6b4
      items: string
      type: array
  - id: another_input
    label: Another Input - my-asthonishing-stage-in-directory/another_input
    doc: An additional input for demonstration purposes - This parameter is 
      derived from my-asthonishing-stage-in-directory/another_input
    type: string
  - id: item
    label: Landsat-8/9 acquisition reference - pattern-1/item
    doc: Landsat-8/9 acquisition reference - This parameter is derived from 
      pattern-1/item
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
  - id: s3_bucket
    label: my-super-stage-out/s3_bucket
    doc: 'This parameter is derived from: my-super-stage-out/s3_bucket'
    type: string
  - id: sub_path
    label: my-super-stage-out/sub_path
    doc: 'This parameter is derived from: my-super-stage-out/sub_path'
    type: string
  - id: aws_access_key_id
    label: my-super-stage-out/aws_access_key_id
    doc: 'This parameter is derived from: my-super-stage-out/aws_access_key_id'
    type: string
  - id: aws_secret_access_key
    label: my-super-stage-out/aws_secret_access_key
    doc: 'This parameter is derived from: my-super-stage-out/aws_secret_access_key'
    type: string
  - id: region_name
    label: my-super-stage-out/region_name
    doc: 'This parameter is derived from: my-super-stage-out/region_name'
    type: string
  - id: endpoint_url
    label: my-super-stage-out/endpoint_url
    doc: 'This parameter is derived from: my-super-stage-out/endpoint_url'
    type: string
  outputs:
  - id: water_bodies
    label: Water bodies detected
    doc: Water bodies detected based on the NDWI and otsu threshold
    outputSource: stage_out_0/s3_catalog_output
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
  requirements:
  - class: SubworkflowFeatureRequirement
  - class: SchemaDefRequirement
    types:
    - $import: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml
  steps:
  - id: directory_stage_in_0
    label: Stage-in 0
    doc: Stage-in Directory 0
    in:
    - id: reference
      source: item
    - id: another_input
      source: another_input
    out:
    - staged
    run: '#my-asthonishing-stage-in-directory'
  - id: app
    label: Water bodies detection based on NDWI and the otsu threshold
    doc: Water bodies detection based on NDWI and otsu threshold applied to a 
      single Landsat-8/9 acquisition
    in:
    - id: aoi
      source: aoi
    - id: epsg
      source: epsg
    - id: bands
      source: bands
    - id: item
      source: directory_stage_in_0/staged
    out:
    - water_bodies
    run: '#pattern-1'
  - id: stage_out_0
    label: Stage-out 0
    doc: Stage-out Directory 0
    in:
    - id: s3_bucket
      source: s3_bucket
    - id: sub_path
      source: sub_path
    - id: aws_access_key_id
      source: aws_access_key_id
    - id: aws_secret_access_key
      source: aws_secret_access_key
    - id: region_name
      source: region_name
    - id: endpoint_url
      source: endpoint_url
    - id: stac_catalog
      source: app/water_bodies
    out:
    - s3_catalog_output
    run: '#my-super-stage-out'
- id: my-asthonishing-stage-in-file
  class: CommandLineTool
  inputs:
  - id: reference
    label: Reference URL
    doc: An URL to stage
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
  - id: another_input
    label: Another Input
    doc: An additional input for demonstration purposes
    type: string
  outputs:
  - id: staged
    type: File
    outputBinding:
      glob: staged
  requirements:
  - class: NetworkAccess
    networkAccess: true
  - class: SchemaDefRequirement
    types:
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Date
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Date/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#DateTime
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#DateTime/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Duration
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Duration/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Email
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Email/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Hostname
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Hostname/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IDNEmail
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IDNEmail/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IDNHostname
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IDNHostname/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IPv4
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IPv4/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IPv6
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IPv6/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IRI
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IRI/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IRIReference
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#IRIReference/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#JsonPointer
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#JsonPointer/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Password
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Password/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#RelativeJsonPointer
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#RelativeJsonPointer/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#UUID
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#UUID/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI/value
        type: string
      type: