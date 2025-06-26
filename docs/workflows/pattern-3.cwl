cwlVersion: v1.2
$graph:
- id: main
  class: Workflow
  inputs:
  - id: another_input
    label: Another Input - my-asthonishing-stage-in/another_input
    doc: An additional input for demonstration purposes - This parameter is 
      derived from my-asthonishing-stage-in/another_input
    type: string
  - id: aoi
    label: area of interest - pattern-3/aoi
    doc: area of interest as a bounding box - This parameter is derived from 
      pattern-3/aoi
    type: string
  - id: epsg
    label: EPSG code - pattern-3/epsg
    doc: EPSG code - This parameter is derived from pattern-3/epsg
    default: EPSG:4326
    type: string
  - id: bands
    label: bands used for the NDWI - pattern-3/bands
    doc: bands used for the NDWI - This parameter is derived from 
      pattern-3/bands
    default:
    - green
    - nir08
    type:
      name: _:b4121726-fb93-4403-99a4-f7d951ea2e29
      items: string
      type: array
  - id: items
    label: STAC item reference - pattern-3/items
    doc: Reference to a STAC item - This parameter is derived from 
      pattern-3/items
    type:
      name: _:ad345fc9-5d4d-41cb-8ae2-e17dbb8a71e6
      items: https://raw.githubusercontent.com/eoap/schemas/main/url.yaml#URL
      type: array
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
  - id: stac_catalog
    outputSource:
    - stage_out_0/s3_catalog_output
    type:
      name: _:dd03f491-27ff-4778-9f82-d3b136470e51
      items: https://raw.githubusercontent.com/eoap/schemas/main/url.yaml#URL
      type: array
  requirements:
  - class: SubworkflowFeatureRequirement
  - class: SchemaDefRequirement
    types:
    - $import: https://raw.githubusercontent.com/eoap/schemas/main/url.yaml
  - class: ScatterFeatureRequirement
  steps:
  - id: stage_in_0
    in:
    - id: reference
      source: items
    - id: another_input
      source: another_input
    out:
    - staged
    run: '#my-asthonishing-stage-in'
    scatter: reference
    scatterMethod: dotproduct
  - id: app
    in:
    - id: aoi
      source: aoi
    - id: epsg
      source: epsg
    - id: bands
      source: bands
    - id: items
      source: stage_in_0/staged
    out:
    - stac_catalog
    run: '#pattern-3'
  - id: stage_out_0
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
      source: app/stac_catalog
    out:
    - s3_catalog_output
    run: '#my-super-stage-out'
    scatter: stac_catalog
    scatterMethod: dotproduct
- http://commonwl.org/cwltool#original_cwlVersion: v1.2
  id: my-asthonishing-stage-in
  class: CommandLineTool
  inputs:
  - id: reference
    label: STAC Item URL
    doc: A STAC Item to stage
    type: https://raw.githubusercontent.com/eoap/schemas/main/url.yaml#URL
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
  - class: SchemaDefRequirement
    types:
    - name: https://raw.githubusercontent.com/eoap/schemas/main/url.yaml#URL
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/url.yaml#URL/href
        type: string
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/url.yaml#URL/description
        type:
        - 'null'
        - string
      type: record
  - class: DockerRequirement
    dockerPull: ghcr.io/eoap/mastering-app-package/stage:1.0.0
  - class: InlineJavascriptRequirement
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

        cat = asyncio.run(main(href))
  cwlVersion: v1.2
  baseCommand:
  - python
  - stage.py
  arguments:
  - $( inputs.reference.href )
  - $( inputs.another_input )
- id: pattern-3
  class: Workflow
  label: Water bodies detection based on NDWI and the otsu threshold
  doc: Water bodies detection based on NDWI and otsu threshold applied to a 
    single Sentinel-2 COG STAC item
  inputs:
  - id: aoi
    label: area of interest
    doc: area of interest as a bounding box
    type: string
  - id: epsg
    label: EPSG code
    doc: EPSG code
    default: EPSG:4326
    type: string
  - id: bands
    label: bands used for the NDWI
    doc: bands used for the NDWI
    default:
    - green
    - nir08
    type:
      name: _:b4121726-fb93-4403-99a4-f7d951ea2e29
      items: string
      type: array
  - id: items
    label: STAC item reference
    doc: Reference to a STAC item
    type:
      name: _:34a6630a-e033-4c6c-a9ef-e2e0b461fb88
      items: Directory
      type: array
  outputs:
  - id: stac_catalog
    outputSource:
    - step/stac-catalog
    type:
      name: _:fe1d9739-6788-4025-b577-8b55aeea414a
      items: Directory
      type: array
  requirements:
  - class: ScatterFeatureRequirement
  cwlVersion: v1.2
  steps:
  - id: step
    in:
    - id: item
      source: items
    - id: aoi
      source: aoi
    - id: epsg
      source: epsg
    - id: band
      source: bands
    out:
    - stac-catalog
    run: '#clt'
    scatter: step/item
    scatterMethod: dotproduct
  $namespaces: &id001
    s: https://schema.org/
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
    - name: _:e7f52ca7-de77-4c42-9839-949e31ceb072
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
      envValue: $PATH:/app/envs/vegetation-index/bin
  - class: ResourceRequirement
    coresMax: 1
    ramMax: 512
  hints:
  - class: DockerRequirement
    dockerPull: docker.io/library/vegetation-indexes:latest
  cwlVersion: v1.2
  baseCommand:
  - vegetation-index
  arguments:
  - pattern-3
  $namespaces: *id001
- http://commonwl.org/cwltool#original_cwlVersion: v1.2
  id: my-super-stage-out
  class: CommandLineTool
  doc: Stage-out the results to S3
  inputs:
  - id: s3_bucket
    type: string
  - id: sub_path
    type: string
  - id: aws_access_key_id
    type: string
  - id: aws_secret_access_key
    type: string
  - id: region_name
    type: string
  - id: endpoint_url
    type: string
  - id: stac_catalog
    label: STAC Catalog folder
    doc: The folder containing the STAC catalog to stage out
    type: Directory
  outputs:
  - id: s3_catalog_output
    type: https://raw.githubusercontent.com/eoap/schemas/main/url.yaml#URL
    outputBinding:
      loadContents: true
      glob: catalog-uri.txt
      outputEval: |
        ${ 
          return { "href": self[0].contents };
        }
  requirements:
  - class: SchemaDefRequirement
    types:
    - name: https://raw.githubusercontent.com/eoap/schemas/main/url.yaml#URL
      fields:
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/url.yaml#URL/href
        type: string
      - name: 
          https://raw.githubusercontent.com/eoap/schemas/main/url.yaml#URL/description
        type:
        - 'null'
        - string
      type: record
  - class: DockerRequirement
    dockerPull: ghcr.io/eoap/mastering-app-package/stage:1.0.0
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
  - class: InitialWorkDirRequirement
    listing:
    - entryname: stage.py
      entry: |-
        import os
        import sys
        import pystac
        import botocore
        import boto3
        import shutil
        from loguru import logger
        from pystac.stac_io import DefaultStacIO, StacIO
        from urllib.parse import urlparse

        cat_url = sys.argv[1]
        logger.info(cat_url)
        bucket = sys.argv[2]
        subfolder = sys.argv[3]

        aws_access_key_id = os.environ["aws_access_key_id"]
        aws_secret_access_key = os.environ["aws_secret_access_key"]
        region_name = os.environ["aws_region_name"]
        endpoint_url = os.environ["aws_endpoint_url"]

        shutil.copytree(cat_url, "/tmp/catalog")
        cat = pystac.read_file(os.path.join("/tmp/catalog", "catalog.json"))

        class CustomStacIO(DefaultStacIO):
            """Custom STAC IO class that uses boto3 to read from S3."""

            def __init__(self):
                self.session = botocore.session.Session()
                self.s3_client = self.session.create_client(
                    service_name="s3",
                    use_ssl=True,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    endpoint_url=endpoint_url,
                    region_name=region_name,
                )

            def write_text(self, dest, txt, *args, **kwargs):
                parsed = urlparse(dest)
                if parsed.scheme == "s3":
                    self.s3_client.put_object(
                        Body=txt.encode("UTF-8"),
                        Bucket=parsed.netloc,
                        Key=parsed.path[1:],
                        ContentType="application/geo+json",
                    )
                else:
                    super().write_text(dest, txt, *args, **kwargs)


        client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=endpoint_url,
            region_name=region_name,
        )

        StacIO.set_default(CustomStacIO)

        for item in cat.get_items():
            for key, asset in item.get_assets().items():
                s3_path = os.path.normpath(
                    os.path.join(os.path.join(subfolder, item.id, asset.href))
                )
                print(f"upload {asset.href} to s3://{bucket}/{s3_path}",file=sys.stderr)
                client.upload_file(
                    asset.get_absolute_href(),
                    bucket,
                    s3_path,
                )
                asset.href = f"s3://{bucket}/{s3_path}"
                item.add_asset(key, asset)

        cat.normalize_hrefs(f"s3://{bucket}/{subfolder}")

        for item in cat.get_items():
            # upload item to S3
            print(f"upload {item.id} to s3://{bucket}/{subfolder}", file=sys.stderr)
            pystac.write_file(item, item.get_self_href())

        # upload catalog to S3
        print(f"upload catalog.json to s3://{bucket}/{subfolder}", file=sys.stderr)
        pystac.write_file(cat, cat.get_self_href())

        print(f"s3://{bucket}/{subfolder}/catalog.json", end="", file=sys.stdout)
  cwlVersion: v1.2
  baseCommand:
  - python
  - stage.py
  arguments:
  - $( inputs.stac_catalog.path )
  - $( inputs.s3_bucket )
  - ${ var firstPart = (Math.random() * 46656) | 0; var secondPart = 
    (Math.random() * 46656) | 0; firstPart = ("000" + 
    firstPart.toString(36)).slice(-3); secondPart = ("000" + 
    secondPart.toString(36)).slice(-3); return inputs.sub_path + "-" + firstPart
    + secondPart; }
  stdout: catalog-uri.txt
