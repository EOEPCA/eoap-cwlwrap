cwlVersion: v1.0

class: Workflow
id: water-bodies-detection
label: Water bodies detection based on NDWI and the otsu threshold
doc: Water bodies detection based on NDWI and otsu threshold applied to a single Sentinel-2 COG STAC item
requirements: []
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
    type: Directory
outputs:
  - id: stac_catalog
    outputSource:
      - step/stac-catalog
    type: Directory
steps:
  step:
    run: clt.cwl
    in:
      item: item
      aoi: aoi
      epsg: epsg
      band: bands
    out:
      - stac-catalog
