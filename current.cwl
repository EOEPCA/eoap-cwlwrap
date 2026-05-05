cwlVersion: v1.2
$graph:
- https://schema.org/softwareVersion: 1.0.4
  id: stage-out
  class: CommandLineTool
  doc: Stage-out the results to S3
  inputs:
  - id: s3_bucket
    label: S3 Bucket
    doc: The S3 bucket to stage out the results
    type: string
  - id: sub_path
    label: S3 Sub Path
    doc: The sub-path in the S3 bucket to stage out the results
    type: string
  - id: aws_access_key_id
    label: S3 Access Key ID
    doc: The S3 access key ID to use for staging out the results
    type: string
  - id: aws_secret_access_key
    label: S3 Secret Access Key
    doc: The S3 secret access key to use for staging out the results
    type: string
  - id: region_name
    label: S3 Region Name
    doc: The S3 region name to use for staging out the results
    type: string
  - id: endpoint_url
    label: S3 Endpoint URL
    doc: The S3 endpoint URL to use for staging out the results
    type: string
  - id: stac_catalog
    label: STAC Catalog folder
    doc: The folder containing the STAC catalog to stage out
    type: Directory
  - id: title
    label: Argo Workflow Title
    doc: The title of the Argo workflow
    type: string
  - id: description
    label: Argo Workflow Description
    doc: The description of the Argo workflow
    type: string
  - id: uid
    label: Argo Workflow UID
    doc: The unique identifier of the Argo workflow
    type: string
  - id: entry_point
    label: CWL Entry Point
    doc: The entry point of the CWL workflow
    type: string
  - id: label
    label: CWL Label
    doc: The label of the CWL workflow
    type: string
  - id: doc
    label: CWL Doc
    doc: The doc of the CWL workflow
    type: string
  - id: version
    label: CWL software version
    doc: The software version of the CWL workflow
    type: string
  - id: platform_name
    label: Platform Name
    doc: The platform name to use in the STAC collection
    type: string
  - id: thumbnail
    label: Thumbnail
    doc: The thumbnail to use in the STAC collection
    type: string
  - id: namespace
    label: Namespace
    doc: Workflow namespace
    type: string
  outputs:
  - id: s3_catalog_output
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
    outputBinding:
      loadContents: true
      glob: catalog-uri.txt
      outputEval: |
        ${ 
          return { "value": self[0].contents, "type": "https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI" };
        }
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
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time/value
        type: string
      type: record
  - class: DockerRequirement
    dockerPull: cr.terradue.com/calrimate/stage-out:0.1.11
  - class: InlineJavascriptRequirement
  - class: EnvVarRequirement
    envDef:
    - envName: aws_access_key_id
      envValue: $( inputs.aws_access_key_id )
    - envName: aws_secret_access_key
      envValue: $( inputs.aws_secret_access_key )
    - envName: aws_region_name
      envValue: $( inputs.region_name )
    - envName: aws_endpoint_url
      envValue: $( inputs.endpoint_url )
  - class: ResourceRequirement
    coresMin: 1
    coresMax: 2
    ramMin: 2048
    ramMax: 4096
  cwlVersion: v1.2
  baseCommand:
  - stage-out
  arguments:
  - prefix: --s3-bucket
    valueFrom: $(inputs.s3_bucket)
  - prefix: --out-path
    valueFrom: |
      ${
        var base = inputs.sub_path || "stage-out";
        if (inputs.s3_bucket) {
          var a = ((Math.random()*46656)|0).toString(36).padStart(3,"0");
          var b = ((Math.random()*46656)|0).toString(36).padStart(3,"0");
          return base + "-" + a + b;
        }
        return base;
      }
  - prefix: --stac-catalog
    valueFrom: $(inputs.stac_catalog.path)
  - prefix: --title
    valueFrom: $(inputs.title)
  - prefix: --description
    valueFrom: $(inputs.description)
  - prefix: --uid
    valueFrom: $(inputs.uid)
  - prefix: --entry-point
    valueFrom: $(inputs.entry_point)
  - prefix: --cwl-label
    valueFrom: $(inputs.label)
  - prefix: --cwl-doc
    valueFrom: $(inputs.doc)
  - prefix: --cwl-version
    valueFrom: $(inputs.version)
  - prefix: --platform-name
    valueFrom: $(inputs.platform_name)
  - prefix: --thumbnail
    valueFrom: $(inputs.thumbnail)
  - prefix: --namespace
    valueFrom: $(inputs.namespace)
  stdout: catalog-uri.txt
  $namespaces:
    s: https://schema.org/
  $schemas:
  - http://schema.org/version/9.0/schemaorg-current-http.rdf

- https://schema.org/softwareVersion: 1.0.1
  id: my-asthonishing-stage-in-directory
  class: CommandLineTool
  inputs:
  - id: reference
    label: STAC Item URL
    doc: A STAC Item to stage
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
  - id: another_input
    label: Another Input
    doc: An additional input for demonstration purposes
    type: string
  outputs:
  - id: staged
    type: Directory
    outputBinding:
      glob: .
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
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time/value
        type: string
      type: record
  - class: DockerRequirement
    dockerPull: ghcr.io/eoap/mastering-app-package/stage:1.0.0
  - class: InlineJavascriptRequirement
  - class: ResourceRequirement
    coresMin: 1
    coresMax: 2
    ramMin: 2048
    ramMax: 4096
  - class: InitialWorkDirRequirement
    listing:
    - entryname: stage.py
      entry: |-
        import pystac
        import stac_asset
        import asyncio
        import os
        import sys

        config = stac_asset.Config(warn=True)

        async def main(href: str):
            
            item = pystac.read_file(href)
            
            os.makedirs(item.id, exist_ok=True)
            cwd = os.getcwd()
            
            os.chdir(item.id)
            item = await stac_asset.download_item(item=item, directory=".", config=config)
            os.chdir(cwd)
            
            cat = pystac.Catalog(
                id="catalog",
                description=f"catalog with staged {item.id}",
                title=f"catalog with staged {item.id}",
            )
            cat.add_item(item)
            
            cat.normalize_hrefs("./")
            cat.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

            return cat

        href = sys.argv[1]
        empty_arg = sys.argv[2]

        cat = asyncio.run(main(href))
  cwlVersion: v1.2
  baseCommand:
  - python
  - stage.py
  arguments:
  - $( inputs.reference.value )
  - $( inputs.another_input )
  $namespaces:
    s: https://schema.org/
  $schemas:
  - http://schema.org/version/9.0/schemaorg-current-http.rdf

- id: otsu
  class: CommandLineTool
  inputs:
  - id: raster
    type: Directory
    inputBinding:
      prefix: --input-ndi
  - id: item
    type: Directory
    inputBinding:
      prefix: --item
  - id: collection
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
    inputBinding:
      valueFrom: |
        ${
          // parse the URI provided in the input
          var product_uri = inputs.collection.value;
          // Validate the URI format
          var uriPattern = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i;
          if (!uriPattern.test(product_uri)) {
            throw "Invalid URI format: " + product_uri;
          }
          // Return the URI as a string
          return ["--collection", product_uri];
        }
  outputs:
  - id: water_bodies
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
    coresMax: 1
    ramMax: 512
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
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time/value
        type: string
      type: record
  - class: NetworkAccess
    networkAccess: true
  hints:
  - class: DockerRequirement
    dockerPull: ghcr.io/eoap/application-package-patterns/runner:0.2.0
  cwlVersion: v1.2
  baseCommand:
  - runner
  arguments:
  - otsu-cli
  $namespaces: &id001
    s: https://schema.org/
    eoap: http://oeap.github.io/schema#
- id: norm_diff
  class: CommandLineTool
  inputs:
  - id: rasters
    type:
      name: _:1aab2436-3de6-49ba-888d-57b94c1c55e2
      items: Directory
      type: array
    inputBinding:
      valueFrom: |
        ${
          var args = [];
          for (var i = 0; i < inputs.rasters.length; i++) {
            args.push(`--item-${i + 1}`);
            args.push(inputs.rasters[i].path);
          }
          return args;
        }
  - id: item
    type: Directory
    inputBinding:
      prefix: --item
  - id: collection
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
    inputBinding:
      valueFrom: |
        ${
          // parse the URI provided in the input
          var product_uri = inputs.collection.value;
          // Validate the URI format
          var uriPattern = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i;
          if (!uriPattern.test(product_uri)) {
            throw "Invalid URI format: " + product_uri;
          }
          // Return the URI as a string
          return ["--collection", product_uri];
        }
  outputs:
  - id: ndwi
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
    coresMax: 1
    ramMax: 512
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
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time/value
        type: string
      type: record
  - class: NetworkAccess
    networkAccess: true
  hints:
  - class: DockerRequirement
    dockerPull: ghcr.io/eoap/application-package-patterns/runner:0.2.0
  cwlVersion: v1.2
  baseCommand:
  - runner
  arguments:
  - ndi-cli
  $namespaces: *id001
- id: pattern-12
  class: Workflow
  label: Water body detection based on NDWI and the otsu threshold
  doc: Water bodies detection based on NDWI and otsu threshold applied to 
    Sentinel-2 or Landsat-9 staged acquisitions
  inputs:
  - id: aoi
    label: area of interest
    doc: area of interest as a bounding box
    type: https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox
  - id: bands
    label: bands used for the NDWI
    doc: bands used for the NDWI
    default:
    - green
    - nir
    type:
      name: _:bdef7077-ff6d-4c98-8b91-a5fe00d1cd5e
      items: string
      type: array
  - id: item
    label: Landsat-8/9 acquisition reference
    doc: Landsat-8/9 acquisition reference
    type: Directory
  - id: cropped-collection
    label: cropped reflectances STAC Collection
    doc: STAC Collection URL for the cropped reflectances
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
  - id: ndwi-collection
    label: NDWI STAC Collection
    doc: STAC Collection URL for the NDWI
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
  - id: water-bodies-collection
    label: Water bodies STAC Collection
    doc: STAC Collection URL for the water bodies
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
  outputs:
  - id: cropped
    label: Cropped reflectances
    doc: Cropped reflectances
    outputSource:
    - node_crop/cropped
    type:
      name: _:4900e099-6024-48ae-a56c-45c8903b378d
      items: Directory
      type: array
  - id: ndwi
    label: Normalized Difference Water Index
    doc: Normalized Difference Water Index calculated from the input bands
    outputSource:
    - node_normalized_difference/ndwi
    type: Directory
  - id: water_bodies
    label: Water bodies detected
    doc: Water bodies detected based on the NDWI and otsu threshold
    outputSource:
    - node_otsu/water_bodies
    type: Directory
  requirements:
  - class: ScatterFeatureRequirement
  - class: SchemaDefRequirement
    types:
    - name: https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#CRS
      symbols:
      - 'http://www.opengis.net/def/crs/OGC/1.3/CRS84'
      - 'http://www.opengis.net/def/crs/OGC/0/CRS84h'
      type: enum
    - name: https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox/bbox
        type:
          name: _:ff6977d4-c03f-4b06-89d9-eabd72a9fcf0
          items: double
          type: array
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox/crs
        type: https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#CRS
      type: record
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
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time/value
        type: string
      type: record
  hints:
  - class: eoap:JSONSchemaHint
  cwlVersion: v1.2
  steps:
  - id: node_crop
    label: Crop reflectances
    doc: Crop the reflectances from the Landsat-8/9 acquisition based on the 
      area of interest and input bands
    in:
    - id: item
      source: item
    - id: aoi
      source: aoi
    - id: epsg
      source: aoi
    - id: band
      source: bands
    - id: collection
      source: cropped-collection
    out:
    - cropped
    run: '#crop'
    scatter: node_crop/band
    scatterMethod: dotproduct
  - id: node_normalized_difference
    label: Compute NDWI
    doc: Compute NDWI from the cropped reflectances
    in:
    - id: rasters
      source: node_crop/cropped
    - id: item
      source: item
    - id: collection
      source: ndwi-collection
    out:
    - ndwi
    run: '#norm_diff'
  - id: node_otsu
    label: Detect water bodies
    doc: Detect water bodies based on the otsu threshold from the NDWI
    in:
    - id: raster
      source: node_normalized_difference/ndwi
    - id: item
      source: item
    - id: collection
      source: water-bodies-collection
    out:
    - water_bodies
    run: '#otsu'
  $namespaces: *id001
- id: crop
  class: CommandLineTool
  inputs:
  - id: item
    type: Directory
    inputBinding:
      prefix: --input-item
  - id: aoi
    label: Area of interest
    doc: Area of interest defined as a bounding box
    type: https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox
    inputBinding:
      valueFrom: |
        ${
          // Validate the length of bbox to be either 4 or 6
          var bboxLength = inputs.aoi.bbox.length;
          if (bboxLength !== 4 && bboxLength !== 6) {
            throw "Invalid bbox length: bbox must have either 4 or 6 elements.";
          }
          // Convert bbox array to a space-separated string for echo
          return ["--aoi", inputs.aoi.bbox.join(",")];
        }
  - id: epsg
    type: https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox
    inputBinding:
      valueFrom: |
        ${
          const crs = inputs.epsg.crs;
          if (typeof crs !== "string") {
            throw "Invalid CRS: must be a string.";
          }
          if (["CRS84"].includes(crs)) {
            return ["--epsg", "EPSG:4326"];
          } else {
            throw "Unsupported CRS: only CRS84 is currently supported.";
          }
        }
  - id: band
    type: string
    inputBinding:
      prefix: --band
  - id: collection
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
    inputBinding:
      valueFrom: |
        ${
          // parse the URI provided in the input
          var product_uri = inputs.collection.value;
          // Validate the URI format
          var uriPattern = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i;
          if (!uriPattern.test(product_uri)) {
            throw "Invalid URI format: " + product_uri;
          }
          // Return the URI as a string
          return ["--collection", product_uri];
        }
  outputs:
  - id: cropped
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
    coresMax: 1
    ramMax: 512
  - class: SchemaDefRequirement
    types:
    - name: https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#CRS
      symbols:
      - 'http://www.opengis.net/def/crs/OGC/1.3/CRS84'
      - 'http://www.opengis.net/def/crs/OGC/0/CRS84h'
      type: enum
    - name: https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox/bbox
        type:
          name: _:ff6977d4-c03f-4b06-89d9-eabd72a9fcf0
          items: double
          type: array
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox/crs
        type: https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#CRS
      type: record
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
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time/value
        type: string
      type: record
  - class: NetworkAccess
    networkAccess: true
  hints:
  - class: DockerRequirement
    dockerPull: ghcr.io/eoap/application-package-patterns/runner:0.2.0
  cwlVersion: v1.2
  baseCommand:
  - runner
  arguments:
  - crop-cli
  $namespaces: *id001
- https://schema.org/softwareVersion: 1.0.1
  id: stage-in-file
  class: CommandLineTool
  inputs:
  - id: reference
    label: Reference URL
    doc: An URL to stage
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
  - id: aws_access_key_id
    label: S3 Access Key ID
    doc: Access Key ID for S3
    type: string
  - id: aws_secret_access_key
    label: S3 Secret Access Key
    doc: Secret Access Key for S3
    type: string
  - id: endpoint_url
    label: S3 Server URL
    doc: S3 Server URL
    type: string
  - id: region_name
    label: AWS Region
    doc: AWS Region
    type: string
  outputs:
  - id: staged
    type: File
    outputBinding:
      glob: ${ return inputs.reference.value.split('/').slice(-1)[0]; }
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
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URIReference/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URITemplate/value
        type: string
      type: record
    - name: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#Time/value
        type: string
      type: record
  - class: DockerRequirement
    dockerPull: cr.terradue.com/calrimate/obstore-file-stage:0.1.0
  - class: InlineJavascriptRequirement
  - class: ResourceRequirement
    coresMin: 1
    coresMax: 2
    ramMin: 2048
    ramMax: 4096
  - class: EnvVarRequirement
    envDef:
    - envName: AWS_ACCESS_KEY_ID
      envValue: $(inputs.aws_access_key_id)
    - envName: AWS_SECRET_ACCESS_KEY
      envValue: $(inputs.aws_secret_access_key)
    - envName: S3_SERVER_URL
      envValue: $(inputs.endpoint_url)
    - envName: AWS_REGION
      envValue: $(inputs.region_name)
  cwlVersion: v1.2
  baseCommand:
  - stage-file
  arguments:
  - $( inputs.reference.value )
  $namespaces:
    s: https://schema.org/
  $schemas:
  - http://schema.org/version/9.0/schemaorg-current-http.rdf

- id: main
  class: Workflow
  label: Workflow pattern-12 orchestrator
  doc: This Workflow is used to orchestrate the Workflow pattern-12
  inputs:
  - id: aoi
    label: area of interest - pattern-12/aoi
    doc: area of interest as a bounding box - This parameter is derived from 
      pattern-12/aoi
    type: https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml#BBox
  - id: bands
    label: bands used for the NDWI - pattern-12/bands
    doc: bands used for the NDWI - This parameter is derived from 
      pattern-12/bands
    default:
    - green
    - nir
    type:
      name: _:bdef7077-ff6d-4c98-8b91-a5fe00d1cd5e
      items: string
      type: array
  - id: another_input
    label: Another Input - my-asthonishing-stage-in-directory/another_input
    doc: An additional input for demonstration purposes - This parameter is 
      derived from my-asthonishing-stage-in-directory/another_input
    type: string
  - id: item
    label: Landsat-8/9 acquisition reference - pattern-12/item
    doc: Landsat-8/9 acquisition reference - This parameter is derived from 
      pattern-12/item
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
  - id: cropped-collection
    label: cropped reflectances STAC Collection - pattern-12/cropped-collection
    doc: STAC Collection URL for the cropped reflectances - This parameter is 
      derived from pattern-12/cropped-collection
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
  - id: ndwi-collection
    label: NDWI STAC Collection - pattern-12/ndwi-collection
    doc: STAC Collection URL for the NDWI - This parameter is derived from 
      pattern-12/ndwi-collection
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
  - id: water-bodies-collection
    label: Water bodies STAC Collection - pattern-12/water-bodies-collection
    doc: STAC Collection URL for the water bodies - This parameter is derived 
      from pattern-12/water-bodies-collection
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
  - id: s3_bucket
    label: S3 Bucket - stage-out/s3_bucket
    doc: The S3 bucket to stage out the results - This parameter is derived from
      stage-out/s3_bucket
    type: string
  - id: sub_path
    label: S3 Sub Path - stage-out/sub_path
    doc: The sub-path in the S3 bucket to stage out the results - This parameter
      is derived from stage-out/sub_path
    type: string
  - id: aws_access_key_id
    label: S3 Access Key ID - stage-out/aws_access_key_id
    doc: The S3 access key ID to use for staging out the results - This 
      parameter is derived from stage-out/aws_access_key_id
    type: string
  - id: aws_secret_access_key
    label: S3 Secret Access Key - stage-out/aws_secret_access_key
    doc: The S3 secret access key to use for staging out the results - This 
      parameter is derived from stage-out/aws_secret_access_key
    type: string
  - id: region_name
    label: S3 Region Name - stage-out/region_name
    doc: The S3 region name to use for staging out the results - This parameter 
      is derived from stage-out/region_name
    type: string
  - id: endpoint_url
    label: S3 Endpoint URL - stage-out/endpoint_url
    doc: The S3 endpoint URL to use for staging out the results - This parameter
      is derived from stage-out/endpoint_url
    type: string
  - id: title
    label: Argo Workflow Title - stage-out/title
    doc: The title of the Argo workflow - This parameter is derived from 
      stage-out/title
    type: string
  - id: description
    label: Argo Workflow Description - stage-out/description
    doc: The description of the Argo workflow - This parameter is derived from 
      stage-out/description
    type: string
  - id: uid
    label: Argo Workflow UID - stage-out/uid
    doc: The unique identifier of the Argo workflow - This parameter is derived 
      from stage-out/uid
    type: string
  - id: entry_point
    label: CWL Entry Point - stage-out/entry_point
    doc: The entry point of the CWL workflow - This parameter is derived from 
      stage-out/entry_point
    type: string
  - id: label
    label: CWL Label - stage-out/label
    doc: The label of the CWL workflow - This parameter is derived from 
      stage-out/label
    type: string
  - id: doc
    label: CWL Doc - stage-out/doc
    doc: The doc of the CWL workflow - This parameter is derived from 
      stage-out/doc
    type: string
  - id: version
    label: CWL software version - stage-out/version
    doc: The software version of the CWL workflow - This parameter is derived 
      from stage-out/version
    type: string
  - id: platform_name
    label: Platform Name - stage-out/platform_name
    doc: The platform name to use in the STAC collection - This parameter is 
      derived from stage-out/platform_name
    type: string
  - id: thumbnail
    label: Thumbnail - stage-out/thumbnail
    doc: The thumbnail to use in the STAC collection - This parameter is derived
      from stage-out/thumbnail
    type: string
  - id: namespace
    label: Namespace - stage-out/namespace
    doc: Workflow namespace - This parameter is derived from stage-out/namespace
    type: string
  - id: s3_bucket
    label: S3 Bucket - stage-out/s3_bucket
    doc: The S3 bucket to stage out the results - This parameter is derived from
      stage-out/s3_bucket
    type: string
  - id: sub_path
    label: S3 Sub Path - stage-out/sub_path
    doc: The sub-path in the S3 bucket to stage out the results - This parameter
      is derived from stage-out/sub_path
    type: string
  - id: aws_access_key_id
    label: S3 Access Key ID - stage-out/aws_access_key_id
    doc: The S3 access key ID to use for staging out the results - This 
      parameter is derived from stage-out/aws_access_key_id
    type: string
  - id: aws_secret_access_key
    label: S3 Secret Access Key - stage-out/aws_secret_access_key
    doc: The S3 secret access key to use for staging out the results - This 
      parameter is derived from stage-out/aws_secret_access_key
    type: string
  - id: region_name
    label: S3 Region Name - stage-out/region_name
    doc: The S3 region name to use for staging out the results - This parameter 
      is derived from stage-out/region_name
    type: string
  - id: endpoint_url
    label: S3 Endpoint URL - stage-out/endpoint_url
    doc: The S3 endpoint URL to use for staging out the results - This parameter
      is derived from stage-out/endpoint_url
    type: string
  - id: title
    label: Argo Workflow Title - stage-out/title
    doc: The title of the Argo workflow - This parameter is derived from 
      stage-out/title
    type: string
  - id: description
    label: Argo Workflow Description - stage-out/description
    doc: The description of the Argo workflow - This parameter is derived from 
      stage-out/description
    type: string
  - id: uid
    label: Argo Workflow UID - stage-out/uid
    doc: The unique identifier of the Argo workflow - This parameter is derived 
      from stage-out/uid
    type: string
  - id: entry_point
    label: CWL Entry Point - stage-out/entry_point
    doc: The entry point of the CWL workflow - This parameter is derived from 
      stage-out/entry_point
    type: string
  - id: label
    label: CWL Label - stage-out/label
    doc: The label of the CWL workflow - This parameter is derived from 
      stage-out/label
    type: string
  - id: doc
    label: CWL Doc - stage-out/doc
    doc: The doc of the CWL workflow - This parameter is derived from 
      stage-out/doc
    type: string
  - id: version
    label: CWL software version - stage-out/version
    doc: The software version of the CWL workflow - This parameter is derived 
      from stage-out/version
    type: string
  - id: platform_name
    label: Platform Name - stage-out/platform_name
    doc: The platform name to use in the STAC collection - This parameter is 
      derived from stage-out/platform_name
    type: string
  - id: thumbnail
    label: Thumbnail - stage-out/thumbnail
    doc: The thumbnail to use in the STAC collection - This parameter is derived
      from stage-out/thumbnail
    type: string
  - id: namespace
    label: Namespace - stage-out/namespace
    doc: Workflow namespace - This parameter is derived from stage-out/namespace
    type: string
  - id: s3_bucket
    label: S3 Bucket - stage-out/s3_bucket
    doc: The S3 bucket to stage out the results - This parameter is derived from
      stage-out/s3_bucket
    type: string
  - id: sub_path
    label: S3 Sub Path - stage-out/sub_path
    doc: The sub-path in the S3 bucket to stage out the results - This parameter
      is derived from stage-out/sub_path
    type: string
  - id: aws_access_key_id
    label: S3 Access Key ID - stage-out/aws_access_key_id
    doc: The S3 access key ID to use for staging out the results - This 
      parameter is derived from stage-out/aws_access_key_id
    type: string
  - id: aws_secret_access_key
    label: S3 Secret Access Key - stage-out/aws_secret_access_key
    doc: The S3 secret access key to use for staging out the results - This 
      parameter is derived from stage-out/aws_secret_access_key
    type: string
  - id: region_name
    label: S3 Region Name - stage-out/region_name
    doc: The S3 region name to use for staging out the results - This parameter 
      is derived from stage-out/region_name
    type: string
  - id: endpoint_url
    label: S3 Endpoint URL - stage-out/endpoint_url
    doc: The S3 endpoint URL to use for staging out the results - This parameter
      is derived from stage-out/endpoint_url
    type: string
  - id: title
    label: Argo Workflow Title - stage-out/title
    doc: The title of the Argo workflow - This parameter is derived from 
      stage-out/title
    type: string
  - id: description
    label: Argo Workflow Description - stage-out/description
    doc: The description of the Argo workflow - This parameter is derived from 
      stage-out/description
    type: string
  - id: uid
    label: Argo Workflow UID - stage-out/uid
    doc: The unique identifier of the Argo workflow - This parameter is derived 
      from stage-out/uid
    type: string
  - id: entry_point
    label: CWL Entry Point - stage-out/entry_point
    doc: The entry point of the CWL workflow - This parameter is derived from 
      stage-out/entry_point
    type: string
  - id: label
    label: CWL Label - stage-out/label
    doc: The label of the CWL workflow - This parameter is derived from 
      stage-out/label
    type: string
  - id: doc
    label: CWL Doc - stage-out/doc
    doc: The doc of the CWL workflow - This parameter is derived from 
      stage-out/doc
    type: string
  - id: version
    label: CWL software version - stage-out/version
    doc: The software version of the CWL workflow - This parameter is derived 
      from stage-out/version
    type: string
  - id: platform_name
    label: Platform Name - stage-out/platform_name
    doc: The platform name to use in the STAC collection - This parameter is 
      derived from stage-out/platform_name
    type: string
  - id: thumbnail
    label: Thumbnail - stage-out/thumbnail
    doc: The thumbnail to use in the STAC collection - This parameter is derived
      from stage-out/thumbnail
    type: string
  - id: namespace
    label: Namespace - stage-out/namespace
    doc: Workflow namespace - This parameter is derived from stage-out/namespace
    type: string
  outputs:
  - id: cropped
    label: Cropped reflectances
    doc: Cropped reflectances
    outputSource: stage_out_0/s3_catalog_output
    type:
      name: _:0864a2a5-3080-4666-bb21-c41f39c71229
      items: 
        https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
      type: array
  - id: ndwi
    label: Normalized Difference Water Index
    doc: Normalized Difference Water Index calculated from the input bands
    outputSource: stage_out_1/s3_catalog_output
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
  - id: water_bodies
    label: Water bodies detected
    doc: Water bodies detected based on the NDWI and otsu threshold
    outputSource: stage_out_2/s3_catalog_output
    type: 
      https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
  requirements:
  - class: SubworkflowFeatureRequirement
  - class: ScatterFeatureRequirement
  - class: SchemaDefRequirement
    types:
    - $import: https://raw.githubusercontent.com/eoap/schemas/main/ogc.yaml
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
    label: Water body detection based on NDWI and the otsu threshold
    doc: Water bodies detection based on NDWI and otsu threshold applied to 
      Sentinel-2 or Landsat-9 staged acquisitions
    in:
    - id: aoi
      source: aoi
    - id: bands
      source: bands
    - id: item
      source: directory_stage_in_0/staged
    - id: cropped-collection
      source: cropped-collection
    - id: ndwi-collection
      source: ndwi-collection
    - id: water-bodies-collection
      source: water-bodies-collection
    out:
    - cropped
    - ndwi
    - water_bodies
    run: '#pattern-12'
  - id: stage_out_0
    label: Stage-out 0
    doc: Stage-out Directory[] 0
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
      source: app/cropped
    - id: title
      source: title
    - id: description
      source: description
    - id: uid
      source: uid
    - id: entry_point
      source: entry_point
    - id: label
      source: label
    - id: doc
      source: doc
    - id: version
      source: version
    - id: platform_name
      source: platform_name
    - id: thumbnail
      source: thumbnail
    - id: namespace
      source: namespace
    out:
    - s3_catalog_output
    run: '#stage-out'
    scatter: stac_catalog
    scatterMethod: dotproduct
  - id: stage_out_2
    label: Stage-out 2
    doc: Stage-out Directory 2
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
    - id: title
      source: title
    - id: description
      source: description
    - id: uid
      source: uid
    - id: entry_point
      source: entry_point
    - id: label
      source: label
    - id: doc
      source: doc
    - id: version
      source: version
    - id: platform_name
      source: platform_name
    - id: thumbnail
      source: thumbnail
    - id: namespace
      source: namespace
    out:
    - s3_catalog_output
    run: '#stage-out'
  - id: stage_out_1
    label: Stage-out 1
    doc: Stage-out Directory 1
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
      source: app/ndwi
    - id: title
      source: title
    - id: description
      source: description
    - id: uid
      source: uid
    - id: entry_point
      source: entry_point
    - id: label
      source: label
    - id: doc
      source: doc
    - id: version
      source: version
    - id: platform_name
      source: platform_name
    - id: thumbnail
      source: thumbnail
    - id: namespace
      source: namespace
    out:
    - s3_catalog_output
    run: '#stage-out'
