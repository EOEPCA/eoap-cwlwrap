cwlVersion: v1.2

class: Workflow
id: _temp
label: Temporary workflow for packing 
doc: This workflow is used to pack the CWL files

inputs: 
  aoi:
    label: area of interest
    doc: area of interest as a bounding box
    type: string
  epsg:
    label: EPSG code
    doc: EPSG code
    type: string
    default: "EPSG:4326"
  bands:
    label: bands used for the NDWI
    doc: bands used for the NDWI
    type: string[]
    default: ["green", "nir08"]
  item:
    doc: Reference to a STAC item
    label: STAC item reference
    type: URL

outputs:
  stac_catalog:
    type: string
    outputSource: step/stage_out/s3_catalog_output

steps:

  stage_in:
    run: #expected/stage-in.cwl
    in:
      reference: item
    out:
      - staged

  app:
    run: #expected/pattern-1.cwl
    in:
      item: step/staged
      aoi: aoi
      epsg: epsg
      bands: bands
    out:
      - stac_catalog

  stage_out:
    run: #expected/stage-out.cwl
    in:
      s3_bucket: s3_bucket
      sub_path: sub_path
      aws_access_key_id: aws_access_key_id
      aws_secret_access_key: aws_secret_access_key
      region_name: region_name
      endpoint_url: endpoint_url
      stac_catalog: step/app/stac_catalog
    out:
      - s3_catalog_output
