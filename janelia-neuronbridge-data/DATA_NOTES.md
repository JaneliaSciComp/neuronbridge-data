## Data Version 3.1.1 (released on 2023-07-08)

### Color Depth Searches

**LM data**
* Added 43,393 additional Split GAL4 brain color depth MIPs

**EM data**
* Added 23,271 Male VNC neuron bodies from the [FlyEM MANC release](https://www.janelia.org/project-team/flyem/manc-connectome)
 and computed precomputed matches against all LM VNC images.

### PatchPerPix (PPP) searches
Added PPPM results for VNC:0.5 dataset against Gen1 MCFO VNC samples.


## Data Version 3.0.0 (released on 2023-02-01)

### Data Model
* Switched to new data model
* No new data was added (no new images, no new matches)
* Merged Brain and VNC data from 2.4.0 and 2.3.0-pre
* All paths are absolute, optionally using prefix variables from config.json
* Removed unused attributes: `maskImageURL`, `maskSampleRef`, `maskRelatedImageRefId`, `coverageScore`, 
  `aggregateCoverage`, `matchingRatio`, `gradientAreaGap`, `highExpressionArea`, `normalizedGapScore`.
* The data migration from 3.0.0 eliminated all LM to EM matches that actually did not have a gradient score. 
  Those matches were originally exported due to a bug in v2.x which inadvertently exported LM to EM match that did not have 
  a gradient score when the EM to LM gradient scores were updated for the corresponding LM to EM matches.


## Data Version 2.4.0 (released on 2022-02-25)

### Data Model
* 3D files are available for download for both Color Depth Searches and PatchPerPix (PPP) searches
* LM data: added aligned image stacks in the H5J format
* EM data: added skeletons in the SWC format

### Color Depth Searches

**LM data**
* Added 27,600 additional samples from the Annotator Gen1 MCFO data set, including 579 new lines. These samples were imaged with 20x and 63x objectives instead of 40x. 
* See the [FlyLight Gen1 MCFO website](https://gen1mcfo.janelia.org/cgi-bin/gen1mcfo.cgi) for all available images and citation guidance.


## Data Version 2.3.0 (released on 2021-10-26)

### Color Depth Searches

**LM data**
* Added MCFO phase 2 lines


## Data Version 2.2.1 (released on 2021-10-18)

### PatchPerPix (PPP) searches

**EM data**
* Hemibrain 1.2.1

**LM data**
* MCFO Phase 2

### Notes
* See [PatchPerPix website](https://github.com/Kainmueller-Lab/PatchPerPix) for information on the PPPM algorithm


## Data Version 2.2.0 (released on 2021-09-30)

### Data Model
* Added `neuronType` and `neuronInstance` attributes to EM results JSON
* Added `searchablePNG` attribute to results JSON

### Color Depth Searches

**EM data**
* Hemibrain 1.2.1

**LM data**
* MCFO GAL4 lines
* Stable split GAL4 lines

Parameters for pre-computed color-depth matches between LM and EM data:
* maskThreshold: 20
* targetThreshold: 20
* xyShift : 2
* mirrorMask: enabled
* pixColorFluctuation: 1.0
* pctPositivePixels: 1.0


### PatchPerPix (PPP) searches
**EM data**
* Hemibrain 1.2.0

**LM data**
* MCFO GAL4 lines


## Data Version 2.1.1 (released on 2020-11-03)

* Fixed the merge process. There was a bug which favored matches with higher pixel score while merging results from 
  EM-vs-MCFO with the results from EM-vs-SplitGal4 instead of the matches with a higher normalized gradient score. This 
  led to a wrong ranking of the final results.
 

## Data Version 2.1.0 (released on 2020-09-15)

### Data Model
* Data format change - removed the attributes map

### Color Depth Searches

**EM data**
* Hemibrain 1.1
    * 32,777 EM bodies

**LM data**
* MCFO GAL4 lines
   * 175,533 segmented MCFO CDM
   * 80,812 MCFO channels
   * 27,144 MCFO samples
   * 4,540 MCFO GAL4 lines

* Stable split GAL4 lines
   * 8,727 segmented SS CDM
   * 3,045 SS channels
   * 1,379 SS samples
   * 653 SS lines

### Notes
Parameters for pre-computed matches between LM and EM data:
* maskThreshold: 20
* targetThreshold: 20
* xyShift : 2
* mirrorMask: enabled
* pixColorFluctuation: 1.0
* pctPositivePixels: 1.0


## Data Version 1.1.0 (released on 2020-04-15)

* Precomputed matches between Flylight Split GAL4 and MCFO vs Hemibrain 1.0.1.
* Created the segmentation for Flylight Split GAL4 and MCFO libraries and the color depth search between Hemibrain 
  neurons and FlyLight images was actually run using the segmented MIPs.
* For Hemibrain neurons which cross the middle section also generated the flipped neuron by mirroring it and adding 
  the original and also compared this against all FlyLight MIPs.
* For calculating the negative scores - gradient area gap and the area of regions with high expression - we selected 
  the MIPs for the top 300 lines and we used precomnputed RGB masks generated with a radius of 20px.

